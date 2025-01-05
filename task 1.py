#Project by Tanmay Manish Patil
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def respond_to_greeting(command):
    if "hello" in command or "hi" in command:
        speak("Hello! How can I assist you today?")
    elif "bye" in command:
        speak("Goodbye!")
        exit()

def tell_time_or_date(command):
    if "time" in command:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%H:%M:%S')}.")
    elif "date" in command:
        now = datetime.datetime.now()
        speak(f"Today's date is {now.strftime('%B %d, %Y')}.")
def search_web(command):
    if "search" in command or "find" in command or "look up" in command:
        query = command.split("search",1)[1] if "search" in command else \
                command.split("find",1)[1] if "find" in command else \
                command.split("look up",1)[1]
        speak(f"Searching the web for {query}...")
        webbrowser.open(f"https://www.google.com/search?q={query}")

def search_wikipedia(command):
    if "wikipedia" in command:
        query = command.split("wikipedia",1)[1].strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)  # Speak out the Wikipedia summary
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Could you be more specific?")
            # Optionally, print the list of disambiguation options
            print(e.options)  
        except wikipedia.exceptions.HTTPTimeoutError:
            speak("Sorry, I am unable to fetch data from Wikipedia at the moment.")
        except wikipedia.exceptions.RedirectError:
            speak("The query seems to be a redirect. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any page for your query.")

def handle_general_queries(command):
    # Check if the user wants to ask a general question
    if "who" in command or "what" in command or "where" in command or "why" in command or "how" in command:
        search_wikipedia(command)
def main():
    speak("Hello! How can I assist you today?")
    
    while True:
        command = recognize_speech()
        if command:
            print(f"Command: {command}")
            respond_to_greeting(command)
            tell_time_or_date(command)
            search_web(command)
            handle_general_queries(command)

if __name__ == "__main__":
    main()
