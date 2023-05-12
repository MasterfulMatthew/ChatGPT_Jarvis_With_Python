'''
Coded by Masterful Matthew
Inspiration from AI Austin's ChatGPT Voice Assistant tutorial
12/5/2023
'''

import openai, pyttsx3, time
import speech_recognition as sr

openai.api_key = "enter-your-chatGPT-token-here"

#sets up the voice
engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
engine.setProperty('voice', 'en-us')
engine.setProperty('rate', 170)

#converts speech to text
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error") #prevents errors from crashing the program
      
#generates response
def generate_response(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000, #max response length is 4000 characters (this is changable)
        n = 1,
        stop = None,
        temperature = 0.7, #changes how creative the response is
    )
    return response["choices"][0]["text"]

#says everthing in "text"
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
def main():
    while True:
        #initializes the microphone to start listening
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                #print(transcription) #prints out was it thinks you said
                if transcription.lower() == "hey jarvis": #the activation call is "hey Jarvis"
                    filename = "input.wav" #creates a file to store what you say
                    print("Greetings sir.") #prints out a greeting, meaning it's ready to listen to you
                    engine.say("Greetings sir.") #says "Greetings sir."
                    engine.runAndWait()
                    #initializes the microphone to listen to your question
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 2 #if nothing is said for more than 2 seconds, it will respond
                        audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)
                        #writes to the input file
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    text = transcribe_audio_to_text(filename) #transcribes what you said
                    if text:
                        print(f"You said: {text}")
                        engine.say(f"You said: {text}, am I correct?")
                        engine.runAndWait()
                        #initializes microphone for an answer of "yes" or "no"
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            audio = recognizer.listen(source)
                            try:
                                transcription = recognizer.recognize_google(audio)
                                if transcription.lower() == "yes":
                                    #responds to you
                                    response = generate_response(text)
                                    if len(response) < 1000: #max response length is 1000 characters (this is changable)
                                        print(response) #prints out the response
                                        speak_text(response) #speaks out the response
                                        
                                    #if the response is too long, it won't print or say it
                                    else:
                                        print("The response was too long.")
                                        engine.say("The response was too long.")
                                        engine.runAndWait()   
                                
                                elif transcription.lower() == "no":
                                    print("Sorry. Please repeat your question.")
                                    engine.say("Sorry. Please repeat your question.")
                                    engine.runAndWait()
                                    try:
                                        #initializes microphone to rehear your question
                                        with sr.Microphone() as source:
                                            recognizer = sr.Recognizer()
                                            source.pause_threshold = 5 ##if nothing is said for more than 5 seconds, it will respond
                                            audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)
                                            #writes to the input file
                                            with open(filename, "wb") as f:
                                                f.write(audio.get_wav_data())
                                                text = transcribe_audio_to_text(filename)
                                                response = generate_response(text)
                                                if len(response) < 300: #max response length is 1000 characters (this is changable)
                                                    print(response) #prints out the response
                                                    speak_text(response) #speaks out the response
                                        
                                                #if the response is too long, it won't print or say it
                                                else:
                                                    print("The response was too long.")
                                                    engine.say("The response was too long.")
                                                    engine.runAndWait()
                                     
                                    #prevents errors from crashing the program
                                    except Exception as e:
                                        #print("An error occured: {}".format(e))
                                        pass
                        
                            #prevents errors from crashing the program
                            except Exception as e:
                                #print("An error occured: {}".format(e))
                                pass
                     
            #prevents errors from crashing the program
            except Exception as e:
                #print("An error occured: {}".format(e))
                pass
             
#starts the program
if __name__ == "__main__":
    main()