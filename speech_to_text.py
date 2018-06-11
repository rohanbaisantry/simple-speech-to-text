
"""

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

"""


# imports
import urllib.request
import speech_recognition as sr
import os.path
import re
from pydub import AudioSegment
import wave
import contextlib
import io

# function to find if there are url's in the string
def url(string):

    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    if len(url) > 0:
    	return True
    else:
    	return False

# Speech-To-Text Class
class STT:


	# initialization function
	def __init__(self, url = "no url", file_name = "no file"):

		self.duration = 0.0
		if url != "no url":
			self.url = url
			print("\n\n \t STT CLASS Object created using the file from the url:\n \t ",url)
		else:
			self.url = None
		if file_name != "no file":
			self.file_name = file_name
			print("\n\n  STT CLASS Object created using the file: ",file_name)
		else:
			self.file_name = None


	# loading function
	def load(self):

		if self.file_name != None:
			self.audio_file = "audio_files\\" + str(self.file_name)
		else:
			urllib.request.urlretrieve(self.url, "audio_files\\download.mp3")
			self.audio_file = "audio_files\\download.mp3"
		extension = os.path.splitext(self.audio_file)[1]
		if extension == ".mp3":
			AudioSegment.from_file(self.audio_file).export("audio_files\\file.wav", format="wav")
			del self.audio_file
			self.audio_file = 'audio_files\\file.wav'
		with contextlib.closing(wave.open(self.audio_file,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			self.duration = frames / float(rate)
			print("\n\n Duration of the audio file is: ", self.duration, " seconds.\n")


	# speech to text function
	def speech_to_text(self):

		f = open("results.txt", "w+")
		print("\n using google's cloud's speech recognition...")
		f.write("\nOUTPUT OF SPEECT TO TEXT PYTHON FILE USING GOOGLE'S SPEECH RECOGNITION")
		f.write("\n\nGoogle thinks you said: \n\n\"\n\n")
		r = sr.Recognizer()
		with sr.AudioFile(self.audio_file) as source:
			audio = r.record(source)
		try:
			self.text = r.recognize_google(audio)  # self.text = r.Recognize_google(audio) -> Less Accurate
			f.write(self.text+"\n\n\"")
			f.write("")
			print("\n Text from the audio you provided is stored in results.txt")
			f.close()
		except sr.UnknownValueError:
			print("\n google could not understand the the speech in the audio file, please retry using a diffrent audio source!")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service;{0}".format(e))
		print("\n\n")


# main function
def main():

	file_input = input("\n> only .mp3 files to be provided if you are using a link \n> only .mp3 or .wav files to be provided if you are using a file name \n\n Enter a url or a file name in the audio_files folder: ")
	if url(file_input):
		test_object = STT(url = file_input)
	else:
		test_object = STT(file_name = file_input)
	test_object.load()
	test_object.speech_to_text()

	""" 
	test examples:

	1) test_1.mp3, test_2.wav or test_3.mp3 file in the audio_files folder
	2) url which provides an mp3 file: https://s3.us-east-2.amazonaws.com/rohanbaisantrymp3klenty/test_3.mp3 [ public amazon s3 bucket which holds an mp3 file]

	once the file is downloaded it will store it as download.mp3 in the audio_files folder. 
	file.wav in the audio_files folder is the .wav file created if the input file was a .mp3 file.

	"""

# run
main()


"""

EXTRAS:

# if you want to use the google cloud api directly.

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# function to transcribe the given audio file directly using google's api for synchronous speech recognition 
def transcribe_file(speech_file, f):
    client = speech.SpeechClient()
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig( encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=16000, language_code='en-US')
    response = client.recognize(config, audio)
    for result in response.results:
        f.write("\n"+str(result.alternatives[0].transcript))

[ Synchronous speech recognition is usually used for small audio files, for large audio files ansynchronous speech recognition is used. ]

"""