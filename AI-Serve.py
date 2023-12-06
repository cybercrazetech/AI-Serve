'''
image-m
response-m
insert-m
enter button-b
record button-b
'''
import os

#num of words recorded
x=[0]

#tts
from gtts import gTTS
def tts(mytext,language):
    lang='en'
    if language=='zh-cn':lang='zh-cn'
    myobj = gTTS(text=mytext, lang=lang, slow=False)
    myobj.save("voice.mp3")
    sound = AudioSegment.from_mp3("voice.mp3")
    play(sound)
    os.remove("voice.mp3")

#stt
import speech_recognition as sr
r = sr.Recognizer()

#google translate
from langdetect import detect
from googletrans import Translator
translator = Translator()

#emotion model
import pickle
import nltk
import re, string
f = open(r'finalemotiondetector.pickle', 'rb')
classifier = pickle.load(f)
f.close()

def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in nltk.tag.pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def lemmatize_sentence(tokens):
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in nltk.tag.pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

def analyse(custom_tweet):  #emotion analyse
    custom_tokens = remove_noise(nltk.tokenize.word_tokenize(custom_tweet))
    return classifier.classify(dict([token, True] for token in custom_tokens))

#chatterbot
import wikipedia
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response

BankBot = ChatBot(name = 'BankBot',
                  read_only = True,                  
                  logic_adapters = [
        {
            "import_path": "chatterbot.logic.BestMatch",
            'response_selection_method': get_random_response,
        },
            "chatterbot.logic.MathematicalEvaluation"],                 
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")

corpus_trainer = ChatterBotCorpusTrainer(BankBot)

def respond(text):
    return BankBot.get_response(text)

def wikisearch(query):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about "+query

#tkinter
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
import tkinter as tk
from PIL import ImageTk,Image
import threading
import wave

class App():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100  
   
    frames = []  
    def __init__(self, master):
        self.isrecording = False
        self.button1 = tk.Button(window, text='rec',command=self.startrecording)
        self.button2 = tk.Button(window, text='stop',command=self.stoprecording)
     
        self.button1.grid(row=5,column=0,sticky='NESW')
        self.button2.grid(row=5,column=1,sticky='NESW')

        self.button3 = tk.Button(window,text='Enter', command=press_enter).grid(row=4,columnspan=2,sticky='NESW')

        self.initialise_recorder()

    def initialise_recorder(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True
       
        t = threading.Thread(target=self.record)
        t.start()

        self.isrecording = False
        print('Recorder status: GOOD')
        self.filename='testvoice.wav'
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def startrecording(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True
       
        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        print('Recording complete')
        self.filename='testvoice.wav'
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        mainai(x)
        
    def record(self):
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

def mainai(x):
    text=''
    with sr.AudioFile('testvoice.wav') as source: audio=r.record(source)
    current=r.recognize_google(audio)
    try:current=current.split()
    except:current=[current]
    os.remove('testvoice.wav') 
    for i in range(x[0]):
        del current[0]
    x[0]+=len(current)
    text=' '.join(current)

    if (text == 'quit'):
        window.destroy()
        return
    elif (text == ''):
        print("Voice recognization failed. Please type or retry.")
        response.configure(text="Voice recognization failed. Please type or retry.")
        return
    elif text[0:4]=='wiki':
        restext=wikisearch(text.lstrip('wiki '))
    else: restext = respond(str(translator.translate(str(text), dest='en').text))

    restext=str(translator.translate(str(restext), dest='en').text)
    lang=detect(text)
    print("You say: "+text)
    print("Language detected: "+lang)

    emotion=analyse(restext)
    print("Bot's emotion: "+emotion)
    img = ImageTk.PhotoImage(Image.open("emotions/"+emotion+".png"))
    image.configure(image=img)
    image.image=img
    print('AI-Serve says: '+restext)
    response.configure(text=restext)
       
    tts(restext,lang)
           
def press_enter():
    text=entry.get()
    if (text == 'quit'):
        window.destroy()
        return
    elif (text == ''):
        print("Voice recognization failed. Please type or retry.")
        response.configure(text="Voice recognization failed. Please type or retry.")
        return
    elif text[0:4]=='wiki':
        restext=wikisearch(text.lstrip('wiki '))
    else: restext = respond(str(translator.translate(str(text), dest='en').text))

    restext=str(translator.translate(str(restext), dest='en').text)
    lang=detect(text)
    print("You say: "+text)
    print("Language detected: "+lang)

    emotion=analyse(restext)
    print("Bot's emotion: "+emotion)
    img = ImageTk.PhotoImage(Image.open("emotions/"+emotion+".png"))
    image.configure(image=img)
    image.image=img
    print('AI-Serve says: '+restext)
    response.configure(text=restext)
       
    tts(restext,lang)

print("initialising...")

#start tkinter window
window=tk.Tk()
window.title("AI_Serve the Companion Bot")

img = ImageTk.PhotoImage(Image.open("emotions/normal.png"))
image = tk.Label(window, image=img)
image.grid(row=1,columnspan=2,sticky='NESW')

response = tk.Label(window, text="Type Something to Chat")
response.grid(row=2,columnspan=2,sticky='NESW')

entry = tk.Entry(window)
entry.grid(row=3,columnspan=2,sticky='NESW')

App(window)
window.mainloop()