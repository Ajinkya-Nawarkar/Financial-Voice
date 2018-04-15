# Stock_Analyzer-Speech_Recognition
Application for Stock Analysis based on ML algorithm for Expense budget enabled with Speech recognition assistant for the User Itnerface

# Dependencies instructions for Speech Recognition Interface: (Could be installed on both Windows as well as Linux) 

First, ugrade pip with `pip install --upgrade pip`

Use `pip install -r requirements.txt` to install all the dependencies
- flask
- gtts
- openpyxl
- pandas/pandas-datareader
- pyaudio
- pyglet
- scikit-image/scikit-learn
- scipy
- SpeechRecognition
- waitress (for windows)
- gunicorn (for linux)
- You might also need AVbin5 or AVbin10 dlls (dependencies for microphone and pyaudio packages). 
   Download AVbin10 from https://avbin.github.io/AVbin/Download.html and execute the install script. 
   If the errors are still not resolved, try moving the ddl in the folder of all py files

# Start the Backend
1. Call `waitress-serve --listen=*:8000 app:app` from within `backend\budget-backend\src\budget_backend`
- If on linux, call `gunicorn app:app` from within the same directory
2. Go to localhost:8000


# Miscellaneous: 
1. Stay connected to the internet for the gtts API to work, you can substitute it with pttysx package for offline usage
