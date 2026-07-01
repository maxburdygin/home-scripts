#!/usr/bin/env python3
"""Генератор ежемесячной бюджетной заметки для Obsidian.

Запускается launchd 1-го числа каждого месяца (см. com.maximburdygin.obsidian-budget.plist).
Можно дёрнуть руками: `python3 budget_generator.py` (для текущего месяца)
                     `python3 budget_generator.py 2026-07` (для конкретного месяца).

Логика:
  1. Целевой месяц = аргумент или текущий.
  2. Ищем предыдущую заметку в Base/ — берём ту, что строго до 1-го числа целевого месяца.
  3. Если у неё есть frontmatter type: budget → переносим активы, накопления, план как стартовые
     значения. Суммы по счетам копируются как есть (юзер просто отредактирует то, что изменилось),
     this_month взносы и income/expenses обнуляются.
  4. Если frontmatter нет — генерируем дефолтный пресет (старые заметки на legacy-формате
     остаются как есть, новый формат стартует со следующего раза).
  5. Пишем YYYYMM01 Бюджет.md в Base/. Если уже существует — выходим без перезаписи
     (если не передан --force).
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    sys.stderr.write(
        "Нужен PyYAML. Установи:  /usr/bin/python3 -m pip install --user pyyaml\n"
    )
    sys.exit(2)


VAULT = Path.home() / "Yandex.Disk.localized/Obsidian vault"
BASE_DIR = VAULT / "Base"
TEMPLATE_PATH = VAULT / "Templates/Бюджет.md"

NOTE_RE = re.compile(r"^(\d{4})(\d{2})(\d{2}) Бюджет(?: \(\d+\))?\.md$")
FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


# ---------- helpers ----------

def first_of(year: int, month: int) -> dt.date:
    return dt.date(year, month, 1)


def prev_month(d: dt.date) -> tuple[int, int]:
    y, m = d.year, d.month - 1
    if m == 0:
        m = 12
        y -= 1
    return y, m


def parse_target(arg: str | None) -> dt.date:
    if not arg:
        today = dt.date.today()
        return first_of(today.year, today.month)
    if not re.match(r"^\d{4}-\d{2}$", arg):
        sys.exit(f"Ожидаю YYYY-MM, получил: {arg!r}")
    y, m = map(int, arg.split("-"))
    return first_of(y, m)


def find_prev_note(target: dt.date) -> Path | None:
    """Самая свежая Бюджет-заметка с датой < target."""
    candidates: list[tuple[dt.date, Path]] = []
    for f in BASE_DIR.iterdir():
        m = NOTE_RE.match(f.name)
        if not m:
            continue
        try:
            d = dt.date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError:
            continue
        if d < target:
            candidates.append((d, f))
    if not candidates:
        return None
    candidates.sort()
    return candidates[-1][1]


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    m = FM_RE.match(text)
    if not m:
        return None, text
    try:
        data = yaml.safe_load(m[1]) or {}
    except yaml.YAMLError:
        return None, text
    return data, m[2]


# ---------- legacy parser (для старых заметок без frontmatter) ----------

_NUM_RE = re.compile(r"^-?[\d.,\s ]+$")


def _parse_num(s: str) -> int | None:
    """'2.060.000' → 2060000, '-100 000' → -100000, '1.844.000' → 1844000, '6600' → 6600."""
    if s is None:
        return None
    raw = s.strip().strip("*").replace("**", "").replace(" ", "").replace(" ", "")
    if not raw or raw == "—":
        return None
    if not re.match(r"^-?[\d.,]+$", raw):
        return None
    # точки и запятые — разделители тысяч в этих заметках
    neg = raw.startswith("-")
    if neg:
        raw = raw[1:]
    raw = raw.replace(".", "").replace(",", "")
    try:
        v = int(raw)
    except ValueError:
        return None
    return -v if neg else v


def _classify(name: str, currency: str) -> str:
    n = name.lower()
    # debt — по имени всегда первично
    if any(k in n for k in ["долг", "dept"]):
        return "debt"
    # crypto — только явные крипто-площадки/тикеры
    if any(k in n for k in ["binance", "bybit", "telegram", "usdt", "btc", "eth"]):
        return "crypto"
    # investment — брокерский, ИИС, инвест-счета, банковские вклады
    if any(k in n for k in ["брок", "иис", "инвест", "вклад", "вкл"]):
        return "investment"
    # liquidity — накопительные, ликвидные ETF, LQDT
    if any(k in n for k in ["ликвид", "накоп", "lqdt"]):
        return "liquidity"
    # cash — карты, кеш, расчётные счета, наличные
    if any(k in n for k in ["карт", "cash", "баланс", "raif", "tbc", "wb"]):
        return "cash"
    # дефолт — cash (USD-валюта не делает счёт криптой)
    return "cash"


# Каноничные алиасы для invested_deposits — старые названия → новые
_DEPOSIT_ALIASES = {
    "Т Брокерский": "Т Брокер",
    "Тинькоф Брокер": "Т Брокер",
    "Тинькофф Брокер": "Т Брокер",
    "Т Брокер": "Т Брокер",
    "Т ИИС": "Т ИИС",
    "Тинькоф ИИС": "Т ИИС",
    "Весь Ликвид": "Весь Ликвид",
    "Весь Ликвид*": "Весь Ликвид",
}


def parse_legacy(text: str) -> dict | None:
    """Достаёт активы и накопления из legacy-заметки (markdown-таблицы).

    Возвращает dict, совместимый с frontmatter, чтобы carry_over мог использовать.
    None — если совсем ничего не нашлось.
    """
    assets: list[dict] = []
    deposits: list[dict] = []
    seen_assets: set[str] = set()

    # Простой проход по строкам — таблицы определяем по началу с '|'
    lines = text.splitlines()
    # Первая таблица — активы (нам нужны строки вида '| name | num | $|₽ |')
    in_table = False
    table_idx = 0
    for line in lines:
        s = line.strip()
        if s.startswith("|"):
            if not in_table:
                in_table = True
                table_idx += 1
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not cells or all(c.startswith("---") or c == "" for c in cells):
                continue
            # пропускаем заголовок (Asset/Amount/Currency)
            joined = " | ".join(cells).lower()
            if any(h in joined for h in ["asset", "amount", "currency", "счет", "счёт", "категория", "сумма", "коммент"]):
                continue

            # --- активы (3 столбца: name, amount, currency)
            if table_idx == 1 and len(cells) >= 3:
                name = cells[0].strip("*").strip()
                amount = _parse_num(cells[1])
                cur_cell = cells[2].replace("*", "").strip()
                if not name or amount is None:
                    continue
                if name.lower().startswith(("summary", "total", "ru assets", "1$")):
                    continue
                currency = "USD" if "$" in cur_cell else "RUB"
                if name in seen_assets:
                    continue
                seen_assets.add(name)
                assets.append({
                    "name": name,
                    "amount": amount,
                    "currency": currency,
                    "kind": _classify(name, currency),
                })

            # --- накопления (4 столбца: name, prev_month, this_month, cumulative)
            elif table_idx == 2 and len(cells) >= 4:
                name = cells[0].strip("*").strip()
                cum = _parse_num(cells[3])
                this_m = _parse_num(cells[2])
                if not name or cum is None:
                    continue
                if name.lower().startswith(("total", "summary")):
                    continue
                canon = _DEPOSIT_ALIASES.get(name, name)
                deposits.append({
                    "name": canon,
                    "cumulative": cum,
                    "this_month": this_m if this_m is not None else 0,
                })
        else:
            in_table = False

    if not assets and not deposits:
        return None

    fm: dict = {"_legacy": True}
    if assets:
        fm["assets"] = assets
    if deposits:
        # дедуп по name
        seen: dict[str, dict] = {}
        for d in deposits:
            seen.setdefault(d["name"], d)
        fm["invested_deposits"] = list(seen.values())
    return fm


# ---------- carry-over: prev frontmatter -> next frontmatter ----------

DEFAULT_ASSETS = [
    {"name": "Т Брокер",        "amount": 0, "currency": "RUB", "kind": "investment"},
    {"name": "Т ИИС",           "amount": 0, "currency": "RUB", "kind": "investment"},
    {"name": "Т Ликвид",        "amount": 0, "currency": "RUB", "kind": "liquidity"},
    {"name": "Т Карта + Накоп", "amount": 0, "currency": "RUB", "kind": "cash"},
    {"name": "ВТБ Карта",       "amount": 0, "currency": "RUB", "kind": "cash"},
    {"name": "ВТБ Брокер",      "amount": 0, "currency": "RUB", "kind": "investment"},
    {"name": "Binance",         "amount": 0, "currency": "USD", "kind": "crypto"},
    {"name": "Bybit USDT",      "amount": 0, "currency": "USD", "kind": "crypto"},
    {"name": "Telegram",        "amount": 0, "currency": "USD", "kind": "crypto"},
    {"name": "Долг Мама",       "amount": 0, "currency": "RUB", "kind": "debt"},
]

DEFAULT_DEPOSITS = [
    {"name": "Т Брокер",    "cumulative": 0, "this_month": 0, "kind": "investment"},
    {"name": "Т ИИС",       "cumulative": 0, "this_month": 0, "kind": "investment"},
    {"name": "Весь Ликвид", "cumulative": 0, "this_month": 0, "kind": "liquidity"},
]

DEFAULT_INCOME = {
    "Зарплата": 0, "Аванс": 0, "Премия/бонус": 0, "Хабар/бейдж": 0,
    "Возврат долга": 0, "Дивиденды/купоны": 0, "Прочее": 0,
}

DEFAULT_EXPENSES = {
    "Квартира": 0, "Коммуналка": 0, "Супермаркеты": 0, "Рестораны/кафе": 0,
    "Фастфуд/доставка": 0, "Транспорт": 0, "Каршеринг/такси": 0, "Спорт": 0,
    "Красота/здоровье": 0, "Подарки": 0, "Путешествия": 0,
    "Подписки/связь": 0, "Алкоголь": 0, "Прочее": 0,
}

DEFAULT_PLAN = {
    "invest_target": 70000,
    "liquidity_target": 30000,
    "expenses_target": 200000,
    "savings_rate_target": 0.4,
    "nav_target": 0,
}


def carry_over(prev_fm: dict | None, target: dt.date, prev_note_basename: str | None) -> dict:
    new = {
        "type": "budget",
        "period": target.strftime("%Y-%m"),
        "date": target.strftime("%Y-%m-%d"),
        "created": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "prev": f"[[{prev_note_basename}]]" if prev_note_basename else "",
        "usd_rub": 81.4,
        "fx_note": "курс на 1-е число (можно перебить вручную)",
        "assets": [dict(a) for a in DEFAULT_ASSETS],
        "invested_deposits": [dict(d) for d in DEFAULT_DEPOSITS],
        "income": dict(DEFAULT_INCOME),
        "expenses": dict(DEFAULT_EXPENSES),
        "plan": dict(DEFAULT_PLAN),
        "tags": ["budget", "finance"],
    }

    if not prev_fm:
        return new

    # курс — переносим как есть
    if prev_fm.get("usd_rub"):
        new["usd_rub"] = prev_fm["usd_rub"]

    # активы — копируем целиком, суммы остаются как у прошлого месяца (юзер просто
    # перебивает изменившиеся; это надёжнее обнуления — не потерять забытый счёт)
    if isinstance(prev_fm.get("assets"), list) and prev_fm["assets"]:
        new["assets"] = [dict(a) for a in prev_fm["assets"]]

    # накопления — cumulative переносится, this_month обнуляется, kind сохраняется
    if isinstance(prev_fm.get("invested_deposits"), list) and prev_fm["invested_deposits"]:
        new["invested_deposits"] = [
            {
                "name": d.get("name", ""),
                "cumulative": int(d.get("cumulative", 0) or 0),
                "this_month": 0,
                "kind": d.get("kind", "investment"),
            }
            for d in prev_fm["invested_deposits"]
        ]

    # план — переносим как старт; nav_target поднимаем на +100к, если был задан
    if isinstance(prev_fm.get("plan"), dict):
        new["plan"] = dict(DEFAULT_PLAN)
        new["plan"].update({k: v for k, v in prev_fm["plan"].items() if v is not None})
        if new["plan"].get("nav_target"):
            new["plan"]["nav_target"] = int(new["plan"]["nav_target"]) + 100_000

    return new


# ---------- YAML dumping with stable, compact list-of-dicts formatting ----------

class _Dumper(yaml.SafeDumper):
    pass


def _repr_str(dumper, data):
    """строки выводим без кавычек, кроме случаев, когда они нужны"""
    if "\n" in data or data.startswith(("[", "{", "&", "*", "!", "|", ">", "'", '"', "%", "@", "`")):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_Dumper.add_representer(str, _repr_str)


def dump_frontmatter(fm: dict) -> str:
    """Дампим аккуратно: для assets / invested_deposits — flow-style (одна строка на запись)."""
    # YAML 'flow' для маленьких словарей в списках — компактнее, ближе к шаблону
    def to_flow(d):
        # сохраняет порядок ключей
        parts = []
        for k, v in d.items():
            if isinstance(v, str):
                parts.append(f'{k}: "{v}"')
            else:
                parts.append(f"{k}: {v}")
        return "{" + ", ".join(parts) + "}"

    lines = []
    for key in ["type", "period", "date", "created", "prev", "usd_rub", "fx_note"]:
        v = fm.get(key)
        if v is None or v == "":
            if key == "prev":
                lines.append('prev: ""')
                continue
            continue
        if isinstance(v, str):
            if v == "":
                lines.append(f'{key}: ""')
            else:
                lines.append(f"{key}: {v}")
        else:
            lines.append(f"{key}: {v}")

    lines.append("")
    lines.append("# === АКТИВЫ ===")
    lines.append("assets:")
    for a in fm.get("assets", []):
        lines.append(f"  - {to_flow(a)}")

    lines.append("")
    lines.append("# === ВНЕСЕНО (накопительно) ===")
    lines.append("invested_deposits:")
    for d in fm.get("invested_deposits", []):
        lines.append(f"  - {to_flow(d)}")

    def dump_map(name: str, mapping: dict):
        lines.append("")
        lines.append(f"{name}:")
        for k, v in mapping.items():
            lines.append(f"  {k}: {v}")

    dump_map("income",   fm.get("income",   {}))
    dump_map("expenses", fm.get("expenses", {}))
    dump_map("plan",     fm.get("plan",     {}))

    lines.append("")
    lines.append("tags:")
    for t in fm.get("tags", []):
        lines.append(f"  - {t}")

    return "\n".join(lines) + "\n"


# ---------- body ----------

BODY = r"""# Бюджет — __MONTH_RU__

> Все числа меняются в YAML‑frontmatter сверху. Таблицы и графики ниже считаются автоматически.

## 📊 Сводка

```dataviewjs
const fm = dv.current();
const rate = Number(fm.usd_rub) || 81.4;
const toRub = a => (a.currency === "USD" ? a.amount * rate : Number(a.amount || 0));

const assets = fm.assets || [];
const totalNAV     = assets.reduce((s, a) => s + toRub(a), 0);
const investAssets = assets.filter(a => a.kind === "investment").reduce((s, a) => s + toRub(a), 0);
const crypto       = assets.filter(a => a.kind === "crypto"    ).reduce((s, a) => s + toRub(a), 0);
const liquidity    = assets.filter(a => a.kind === "liquidity" ).reduce((s, a) => s + toRub(a), 0);
const cash         = assets.filter(a => a.kind === "cash"      ).reduce((s, a) => s + toRub(a), 0);
const debts        = assets.filter(a => a.kind === "debt"      ).reduce((s, a) => s + toRub(a), 0);

// дефолт kind для обратной совместимости — старые записи без kind считаются инвестиционными
const isInvestDep = d => (d.kind || "investment") === "investment";
const isLiquidDep = d => d.kind === "liquidity";
const sumCum   = pred => (fm.invested_deposits || []).filter(pred).reduce((s, d) => s + Number(d.cumulative||0), 0);
const sumMonth = pred => (fm.invested_deposits || []).filter(pred).reduce((s, d) => s + Number(d.this_month||0), 0);

const investedDeposits     = sumCum(isInvestDep);
const liquidityDeposits    = sumCum(isLiquidDep);
const depositedInvestMonth = sumMonth(isInvestDep);
const depositedLiquidMonth = sumMonth(isLiquidDep);

const incomeTotal  = Object.values(fm.income   || {}).reduce((s, v) => s + Number(v||0), 0);
const expenseTotal = Object.values(fm.expenses || {}).reduce((s, v) => s + Number(v||0), 0);
const savings      = incomeTotal - expenseTotal;
const savingsRate  = incomeTotal > 0 ? (savings / incomeTotal) : null;

const history = dv.pages('"Base"')
  .where(p => p.type === "budget" && p.period)
  .sort(p => p.period, "asc")
  .map(p => {
    const r = Number(p.usd_rub) || 81.4;
    const isInvP = d => (d.kind || "investment") === "investment";
    return {
      period: p.period,
      total:    (p.assets || []).reduce((s,x) => s + (x.currency === "USD" ? x.amount*r : Number(x.amount||0)), 0),
      invested: (p.invested_deposits || []).filter(isInvP).reduce((s,x) => s + Number(x.cumulative||0), 0),
    };
  });

const maxTotal    = history.length ? Math.max(...history.map(h => h.total), totalNAV) : totalNAV;
const prevTotal   = history.length >= 2 ? history[history.length - 2].total    : null;
const prevInvested= history.length >= 2 ? history[history.length - 2].invested : null;

const expHist = dv.pages('"Base"')
  .where(p => p.type === "budget" && p.expenses)
  .sort(p => p.period, "desc").limit(6)
  .map(p => Object.values(p.expenses || {}).reduce((s,v) => s + Number(v||0), 0))
  .array().filter(v => v > 0);
const avgExpense = expHist.length ? expHist.reduce((s,v) => s+v, 0) / expHist.length : expenseTotal;
const liquidityMonths = avgExpense > 0 ? (liquidity / avgExpense) : null;

const fmt = v => v == null ? "—" : Math.round(v).toLocaleString("ru-RU") + " ₽";
const fmtP= v => v == null ? "—" : (v*100).toFixed(1) + " %";
const fmtX= v => v == null ? "—" : v.toFixed(1) + " мес.";
const dlt = (c, p) => p == null ? "—" : (c-p>=0 ? "+" : "") + Math.round(c-p).toLocaleString("ru-RU") + " ₽";

dv.table(["", ""], [
  ["**СЧА total**",                       `**${fmt(totalNAV)}**`],
  ["   Δ к прошлому месяцу",             dlt(totalNAV, prevTotal)],
  ["   Δ к денежному максимуму",         dlt(totalNAV, maxTotal)],
  ["СЧА инвест-активов (рынок)",          fmt(investAssets)],
  ["СЧА инвестированных средств",         fmt(investedDeposits)],
  ["   Δ внесено vs прошлый",            dlt(investedDeposits, prevInvested)],
  ["   Маржа (рынок − внесено)",         dlt(investAssets, investedDeposits)],
  ["Крипто",                              fmt(crypto)],
  ["Ликвидность (рынок)",                 fmt(liquidity)],
  ["Внесено в ликвидность (накоп)",       fmt(liquidityDeposits)],
  ["Наличность",                          fmt(cash)],
  ["Долги",                               fmt(debts)],
  ["Доход за месяц",                      fmt(incomeTotal)],
  ["Расход за месяц",                     fmt(expenseTotal)],
  ["Сбережения за месяц",                 fmt(savings)],
  ["Сберегательный коэффициент",          fmtP(savingsRate)],
  ["Подушка ликвидности",                 fmtX(liquidityMonths)],
  ["Внесено в инвест за месяц",           fmt(depositedInvestMonth)],
  ["Внесено в ликвидность за месяц",      fmt(depositedLiquidMonth)],
]);
```

## 💼 Активы

```dataviewjs
const fm = dv.current();
const rate = Number(fm.usd_rub) || 81.4;
const toRub = a => (a.currency === "USD" ? a.amount * rate : Number(a.amount || 0));
const a = (fm.assets || []).slice().sort((x,y) => toRub(y) - toRub(x));
const fmtAmt = (x) => `${Number(x.amount).toLocaleString("ru-RU")} ${x.currency === "USD" ? "$" : "₽"}`;
dv.table(["Счёт", "Сумма", "В ₽", "Тип"],
  a.map(x => [x.name, fmtAmt(x), Math.round(toRub(x)).toLocaleString("ru-RU") + " ₽", x.kind])
);
```

## 💰 Внесённое в инвест-счета (накопительно)

```dataviewjs
const d = dv.current().invested_deposits || [];
const fmt = v => Number(v||0).toLocaleString("ru-RU") + " ₽";
const isInvest = x => (x.kind || "investment") === "investment";
const isLiquid = x => x.kind === "liquidity";

const renderSection = (title, items) => {
  if (!items.length) return;
  const sumCum   = items.reduce((s,x) => s + Number(x.cumulative||0), 0);
  const sumMonth = items.reduce((s,x) => s + Number(x.this_month||0), 0);
  const rows = items.map(x => [x.name, fmt(x.this_month), fmt(x.cumulative)]);
  rows.push([`**ИТОГО ${title}**`, `**${fmt(sumMonth)}**`, `**${fmt(sumCum)}**`]);
  dv.header(4, title);
  dv.table(["Счёт", "За месяц", "Накопительно"], rows);
};

renderSection("Инвестиции",  d.filter(isInvest));
renderSection("Ликвидность", d.filter(isLiquid));
```

## 💵 Доходы / Расходы

```dataviewjs
const inc = dv.current().income   || {};
const exp = dv.current().expenses || {};
const fmt = v => Number(v||0).toLocaleString("ru-RU") + " ₽";

const incRows = Object.entries(inc).filter(([,v]) => v > 0).sort((a,b) => b[1]-a[1]).map(([k,v]) => [k, fmt(v)]);
const expRows = Object.entries(exp).filter(([,v]) => v > 0).sort((a,b) => b[1]-a[1]).map(([k,v]) => [k, fmt(v)]);
const totalInc = Object.values(inc).reduce((s,v) => s + Number(v||0), 0);
const totalExp = Object.values(exp).reduce((s,v) => s + Number(v||0), 0);

dv.header(3, "Доходы");
dv.table(["Категория", "Сумма"], incRows.length ? incRows.concat([["**ИТОГО**", `**${fmt(totalInc)}**`]]) : [["—","—"]]);
dv.header(3, "Расходы");
dv.table(["Категория", "Сумма"], expRows.length ? expRows.concat([["**ИТОГО**", `**${fmt(totalExp)}**`]]) : [["—","—"]]);

const target = Number(dv.current().plan?.expenses_target || 0);
if (target > 0) {
  const diff = totalExp - target;
  dv.paragraph(`> Лимит расходов: **${fmt(target)}**. ${
    diff <= 0 ? `Уложился, экономия **${fmt(-diff)}** ✅` : `Перерасход на **${fmt(diff)}** ⚠️`
  }`);
}
```

## 🎯 План vs Факт

```dataviewjs
const fm = dv.current();
const plan = fm.plan || {};
const isInvestDep = d => (d.kind || "investment") === "investment";
const isLiquidDep = d => d.kind === "liquidity";
const depositedInvestMonth = (fm.invested_deposits || []).filter(isInvestDep).reduce((s, d) => s + Number(d.this_month || 0), 0);
const depositedLiquidMonth = (fm.invested_deposits || []).filter(isLiquidDep).reduce((s, d) => s + Number(d.this_month || 0), 0);
const totalExp = Object.values(fm.expenses || {}).reduce((s,v)=>s+Number(v||0),0);
const totalInc = Object.values(fm.income   || {}).reduce((s,v)=>s+Number(v||0),0);
const sr = totalInc > 0 ? (totalInc - totalExp) / totalInc : null;
const rate = Number(fm.usd_rub) || 81.4;
const totalNAV = (fm.assets || []).reduce((s,a) => s + (a.currency==="USD" ? a.amount*rate : Number(a.amount||0)), 0);

const fmt = v => v == null ? "—" : Math.round(v).toLocaleString("ru-RU") + " ₽";
const fmtP= v => v == null ? "—" : (v*100).toFixed(1) + " %";
const ok = (a, t, lessIsBetter=false) => {
  if (t == null || !t) return "—";
  return (lessIsBetter ? (a <= t) : (a >= t)) ? "✅" : "⚠️";
};

dv.table(["Метрика", "План", "Факт", "Δ", "OK"], [
  ["Внести в инвест",     fmt(plan.invest_target), fmt(depositedInvestMonth),
    fmt(depositedInvestMonth - (plan.invest_target||0)),
    ok(depositedInvestMonth, plan.invest_target)],
  ["Внести в ликвидность", fmt(plan.liquidity_target), fmt(depositedLiquidMonth),
    fmt(depositedLiquidMonth - (plan.liquidity_target||0)),
    ok(depositedLiquidMonth, plan.liquidity_target)],
  ["Расходы (лимит)",     fmt(plan.expenses_target), fmt(totalExp),
    fmt(totalExp - (plan.expenses_target||0)),
    ok(totalExp, plan.expenses_target, true)],
  ["Savings rate",        fmtP(plan.savings_rate_target), fmtP(sr),
    (sr != null && plan.savings_rate_target ? fmtP(sr - plan.savings_rate_target) : "—"),
    ok(sr, plan.savings_rate_target)],
  ["Целевое СЧА",     fmt(plan.nav_target), fmt(totalNAV),
    fmt(totalNAV - (plan.nav_target||0)),
    ok(totalNAV, plan.nav_target)],
]);
```

## 🔁 Retro Highlights

-

## 🔮 Sprint Forecast

-

## 🌅 Global Goals

-

## 📈 Графики

```dataviewjs
const rate = (p) => Number(p.usd_rub) || 81.4;
const toRub = (a, r) => a.currency === "USD" ? a.amount * r : Number(a.amount || 0);

const hist = dv.pages('"Base"')
  .where(p => p.type === "budget" && p.period)
  .sort(p => p.period, "asc")
  .array();

if (hist.length === 0) {
  dv.paragraph("_Ещё нет заметок с frontmatter — графики появятся, как только наберётся история._");
} else {
  const isInvestDep = d => (d.kind || "investment") === "investment";

  const labels  = hist.map(p => p.period);
  const total   = hist.map(p => Math.round((p.assets || []).reduce((s,a) => s + toRub(a, rate(p)), 0)));
  const invest  = hist.map(p => Math.round((p.assets || []).filter(a => a.kind === "investment")
                                          .reduce((s,a) => s + toRub(a, rate(p)), 0)));
  const deposit = hist.map(p => Math.round((p.invested_deposits || []).filter(isInvestDep)
                                          .reduce((s,d) => s + Number(d.cumulative||0), 0)));
  const liquid  = hist.map(p => Math.round((p.assets || []).filter(a => a.kind === "liquidity")
                                          .reduce((s,a) => s + toRub(a, rate(p)), 0)));
  const planned = hist.map(p => p.plan?.nav_target ? Math.round(Number(p.plan.nav_target)) : null);

  const palette = { total:"#00E5FF", invest:"#FF4081", deposit:"#00E676", liquid:"#FFAB00", planned:"#B388FF" };
  const line = (color, dashed=false) => ({
    borderColor: color, backgroundColor: color + "26",
    pointBackgroundColor: color, pointBorderColor: color,
    pointRadius: 4, pointHoverRadius: 6,
    borderWidth: 3, fill: false, tension: 0.25,
    ...(dashed ? {borderDash: [6,4]} : {}),
  });
  const config = {
    type: "line",
    data: {
      labels,
      datasets: [
        {label: "СЧА план, ₽",           data: planned, ...line(palette.planned, true)},
        {label: "СЧА total, ₽",          data: total,   ...line(palette.total)},
        {label: "СЧА инвест-активы, ₽",  data: invest,  ...line(palette.invest)},
        {label: "СЧА внесено, ₽",        data: deposit, ...line(palette.deposit)},
        {label: "Ликвидность, ₽",        data: liquid,  ...line(palette.liquid)},
      ],
    },
    options: { scales: { x: { type: "category" } } },
  };
  if (window.renderChart) {
    window.renderChart(config, this.container);
  } else {
    dv.paragraph("_Плагин obsidian-charts не найден; данные ниже:_");
    dv.table(["Период","СЧА","Инвест","Внесено","Ликвид","План"],
      labels.map((l,i) => [l, total[i], invest[i], deposit[i], liquid[i], planned[i] ?? "—"]));
  }
}
```

```dataviewjs
const hist = dv.pages('"Base"')
  .where(p => p.type === "budget" && p.period)
  .sort(p => p.period, "asc")
  .array();

if (hist.length >= 2) {
  const isInvestDep = d => (d.kind || "investment") === "investment";
  const isLiquidDep = d => d.kind === "liquidity";
  const labels = hist.map(p => p.period);
  const investMo = hist.map(p => Math.round((p.invested_deposits || []).filter(isInvestDep).reduce((s,d) => s + Number(d.this_month||0), 0)));
  const liquidMo = hist.map(p => Math.round((p.invested_deposits || []).filter(isLiquidDep).reduce((s,d) => s + Number(d.this_month||0), 0)));
  const rate = (p) => Number(p.usd_rub) || 81.4;
  const investNAV = hist.map(p => Math.round((p.assets || [])
    .filter(a => a.kind === "investment")
    .reduce((s,a) => s + (a.currency === "USD" ? a.amount*rate(p) : Number(a.amount||0)), 0)));
  const netGain = investNAV.map((v,i) => i === 0 ? 0 : v - investNAV[i-1] - investMo[i]);

  const config = {
    type: "bar",
    data: {
      labels,
      datasets: [
        {label: "Внесено в инвест, ₽",      data: investMo, backgroundColor: "#00E676", borderColor: "#00E676", borderWidth: 1, stack: "s1"},
        {label: "Внесено в ликвидность, ₽", data: liquidMo, backgroundColor: "#FFAB00", borderColor: "#FFAB00", borderWidth: 1, stack: "s1"},
        {label: "Прирост рынка, ₽",         data: netGain,  backgroundColor: "#FFEB3B", borderColor: "#FFEB3B", borderWidth: 1, stack: "s1"},
      ],
    },
    options: { scales: { x: { type: "category" } } },
  };
  if (window.renderChart) {
    window.renderChart(config, this.container);
  } else {
    dv.table(["Период","Инвест","Ликвид","Рынок"], labels.map((l,i) => [l, investMo[i], liquidMo[i], netGain[i]]));
  }
}
```

## 🗂 Архив

- __PREV_LINK__
- [[Финансы - Finances - Investment - Broker - Инвестиции - Вики -Wiki]]
- [[Бюджет Пилотный Проект визуала]]
"""


MONTHS_RU = {
    1: "январь",   2: "февраль", 3: "март",     4: "апрель",
    5: "май",      6: "июнь",    7: "июль",     8: "август",
    9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь",
}


def render_note(fm: dict, target: dt.date, prev_note_basename: str | None) -> str:
    month_ru = f"{MONTHS_RU[target.month]} {target.year}".capitalize()
    prev_link = f"[[{prev_note_basename}|⬅ Прошлый месяц]]" if prev_note_basename else "_(прошлый месяц не найден)_"
    body = BODY.replace("__MONTH_RU__", month_ru).replace("__PREV_LINK__", prev_link)
    return "---\n" + dump_frontmatter(fm) + "---\n\n" + body


# ---------- backfill старых legacy-заметок ----------

def _minimal_frontmatter(period: str, parsed: dict, file_date: dt.date) -> dict:
    """Минимальный валидный frontmatter из распарсенных legacy-таблиц."""
    fm = {
        "type": "budget",
        "period": period,
        "date": file_date.strftime("%Y-%m-%d"),
        "created": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "prev": "",
        "usd_rub": 81.4,
        "fx_note": "backfill из legacy-текста",
        "assets": parsed.get("assets", []) or [a.copy() for a in DEFAULT_ASSETS],
        "invested_deposits": [],
        "income":   dict(DEFAULT_INCOME),
        "expenses": dict(DEFAULT_EXPENSES),
        "plan":     dict(DEFAULT_PLAN),
        "tags": ["budget", "finance"],
    }
    # invested_deposits: классифицируем kind по названию (legacy не различал)
    for d in parsed.get("invested_deposits", []):
        name = d.get("name", "")
        kind = "liquidity" if any(k in name.lower() for k in ("ликвид", "накоп", "lqdt")) else "investment"
        fm["invested_deposits"].append({
            "name": name,
            "cumulative": int(d.get("cumulative", 0) or 0),
            "this_month": int(d.get("this_month", 0) or 0),
            "kind": kind,
        })
    if not fm["invested_deposits"]:
        fm["invested_deposits"] = [dict(d) for d in DEFAULT_DEPOSITS]
    return fm


def backfill_legacy(dry_run: bool = False, force: bool = False) -> int:
    """Прогон по всем YYYYMMDD Бюджет.md в Base/: для каждого месяца берём самую
    свежую по дате заметку, и если у неё нет frontmatter — допишем минимальный
    из parse_legacy. С --force перезаписывает уже существующий frontmatter
    (полезно когда правится логика _classify / parse_legacy)."""
    by_month: dict[str, tuple[dt.date, Path]] = {}
    for f in BASE_DIR.iterdir():
        m = NOTE_RE.match(f.name)
        if not m:
            continue
        try:
            d = dt.date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError:
            continue
        key = d.strftime("%Y-%m")
        if key not in by_month or d > by_month[key][0]:
            by_month[key] = (d, f)

    touched, skipped, failed = 0, 0, 0
    for key in sorted(by_month):
        d, f = by_month[key]
        text = f.read_text(encoding="utf-8")
        existing_fm, body_after_fm = split_frontmatter(text)
        if existing_fm and existing_fm.get("type") == "budget":
            if not force:
                skipped += 1
                continue
            # с --force переразбираем тело (без старого frontmatter)
            text_for_parse = body_after_fm
        else:
            text_for_parse = text
        parsed = parse_legacy(text_for_parse)
        if not parsed:
            if existing_fm and existing_fm.get("type") == "budget":
                print(f"[keep]  {f.name}  — уже в новом формате, legacy-тела нет")
                skipped += 1
            else:
                print(f"[fail]  {f.name}  — не удалось распарсить")
                failed += 1
            continue
        fm = _minimal_frontmatter(key, parsed, d)
        new_text = "---\n" + dump_frontmatter(fm) + "---\n\n" + text_for_parse
        if dry_run:
            print(f"[dry]   {f.name}  → frontmatter "
                  f"({len(fm['assets'])} активов, {len(fm['invested_deposits'])} депозитов)")
        else:
            f.write_text(new_text, encoding="utf-8")
            print(f"[ok]    {f.name}  → frontmatter period={key} "
                  f"({len(fm['assets'])} активов, {len(fm['invested_deposits'])} депозитов)")
        touched += 1

    print(f"\nИтого: {'переписано' if force else 'добавлено'} {touched}, "
          f"пропущено (уже есть FM) {skipped}, не распарсилось {failed}")
    return 0


# ---------- main ----------

def main() -> int:
    ap = argparse.ArgumentParser(description="Создать ежемесячную бюджетную заметку.")
    ap.add_argument("month", nargs="?", help="Целевой месяц YYYY-MM (по умолчанию — текущий)")
    ap.add_argument("--force", action="store_true", help="перезаписать, если файл уже есть")
    ap.add_argument("--dry-run", action="store_true", help="не писать, только показать путь и кусок результата")
    ap.add_argument("--backfill-legacy", action="store_true",
                    help="разовый прогон: добавить frontmatter всем старым заметкам без него")
    args = ap.parse_args()

    if not BASE_DIR.is_dir():
        sys.exit(f"Не найдено {BASE_DIR}")

    if args.backfill_legacy:
        return backfill_legacy(dry_run=args.dry_run, force=args.force)

    target = parse_target(args.month)
    fname = f"{target.strftime('%Y%m%d')} Бюджет.md"
    out_path = BASE_DIR / fname

    if out_path.exists() and not args.force:
        print(f"[skip] {out_path} уже существует. --force чтобы перезаписать.")
        return 0

    prev_note = find_prev_note(target)
    prev_fm = None
    prev_basename = None
    if prev_note:
        prev_basename = prev_note.stem  # без .md
        prev_text = prev_note.read_text(encoding="utf-8")
        prev_fm, _ = split_frontmatter(prev_text)
        if prev_fm:
            print(f"[prev] {prev_note.name}  frontmatter: есть")
        else:
            prev_fm = parse_legacy(prev_text)
            if prev_fm:
                print(f"[prev] {prev_note.name}  frontmatter: нет → распарсил legacy "
                      f"({len(prev_fm.get('assets', []))} активов, "
                      f"{len(prev_fm.get('invested_deposits', []))} накоплений)")
            else:
                print(f"[prev] {prev_note.name}  не удалось распарсить, стартую с дефолтов")
    else:
        print("[prev] не найдено")

    fm = carry_over(prev_fm, target, prev_basename)
    note = render_note(fm, target, prev_basename)

    if args.dry_run:
        print(f"[dry-run] would write {out_path}")
        print(note[:1500] + ("\n... (truncated)" if len(note) > 1500 else ""))
        return 0

    out_path.write_text(note, encoding="utf-8")
    print(f"[ok] {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
