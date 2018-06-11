# simple-speech-to-text
this is a simple speech to text program using the speech_recognition module and the google speech to text API

Accepts a .mp3 or a .wav file and performs speech to text using google's speech recognition api and get's the transcription.

REQUIREMENTS:
____________

> Python3
https://www.python.org/downloads/

> Speech Recognition python module [ google could speech to text ]
pip install google
pip install --upgrade google-cloud-speech
pip install speech_recognition	

> ffmpeg python module [ needed for audio conversion, ie; for pydub to work ]
https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg

> PyDub python module [ needed for audio conversion (.mp3 to .wav we can calculate the duration and pass the .wav to the google speech recognition api) ]
pip install pydub

> please remember to set the environment path [ needed to make the google api locate the credentials .json file]
Linux or MacOS: export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
Windows: set GOOGLE_APPLICATION_CREDENTIALS=[PATH]
where [PATH] = path of json (Credentials .json file to use with google's cloud API.)

#####      Please note: max 45 hits per day as per google api setings. ( for free )    #####

____________
