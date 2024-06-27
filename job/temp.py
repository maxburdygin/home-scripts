import subprocess
import datetime

today = datetime.date.today().strftime("%Y-%m-%d")

subprocess.run(["python3", "/Users/user/IdeaProjects/home-pets/job/mover.py", "--today", today])
