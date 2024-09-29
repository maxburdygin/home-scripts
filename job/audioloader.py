import os
import pickle
from pytube import YouTube
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Определяем области доступа, которые нам нужны
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube():
    creds = None
    # Проверяем, существует ли файл с сохраненными учетными данными пользователя
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # Если учетные данные недействительны или отсутствуют, то выполняем авторизацию
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=57316)  # Указываем порт 57316
        # Сохраняем учетные данные для последующего использования
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds

def download_audio_from_youtube(url):
    yt = YouTube(url)
    yt.bypass_age_gate()  # Попытка обхода возрастных ограничений
    audio_stream = yt.streams.filter(only_audio=True).order_by('-abr').first()
    output_file = audio_stream.download()
    base, ext = os.path.splitext(output_file)
    new_file = base + '.mp3'
    os.rename(output_file, new_file)
    print(f'Аудио сохранено как {new_file}')

def main():
    # Выполняем аутентификацию
    creds = authenticate_youtube()

    # Пример использования
    url = 'https://www.youtube.com/watch?v=Kbk9BiPhm7o'  # Замените на вашу ссылку
    download_audio_from_youtube(url)

if __name__ == "__main__":
    main()
