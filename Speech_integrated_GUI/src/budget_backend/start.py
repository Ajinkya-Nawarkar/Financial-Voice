import webbrowser as wb
import os

#Setup and dependencies

os.system("cmd <path> {pip install -r requirements.txt}")
os.system("cmd <path> {waitress-serve --listen:*:8000 app:app}")

text = "localhost:8000"

wb.open(text)
