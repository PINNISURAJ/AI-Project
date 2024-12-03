import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("I am Jarvis Sir. Please tell me how may I help you")       

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5  # Increase pause threshold to give more time between words
        r.adjust_for_ambient_noise(source)  # Adjust to handle background noise
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand audio. Say that again please...")
        speak("I couldn't catch that. Could you say that again?")
        return "None"
    except sr.RequestError:
        speak("Sorry, there is an issue with the speech service.")
        return "None"
    return query


def createSchedule(topics, time_available):
    # Assuming we divide the time evenly for each topic
    time_per_topic = time_available / topics
    schedule = ""
    for i in range(1, topics + 1):
        schedule += f"Topic {i}: Study for {time_per_topic:.2f} hours.\n"
    return schedule

def saveNote(schedule):
    filename = "study_schedule.txt"
    with open(filename, "w") as file:
        file.write(schedule)
    speak(f"Your study schedule has been saved as {filename}")
    print(f"Study schedule saved as {filename}")

def getNumericInput(prompt):
    retries = 3
    speak(prompt)
    while retries > 0:
        input_value = takeCommand()
        try:
            if input_value == "None":
                retries -= 1
                continue
            number = float(input_value)
            return number
        except ValueError:
            retries -= 1
            speak("I didn't catch that. Please say a number.")
            if retries == 0:
                speak("I wasn't able to understand the number. Please try again later.")
                return None

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif 'play music' in query:
            try:
                speak("Which song would you like to listen to?")
                song_name = takeCommand().lower()
                
                if song_name != "none":
                    speak(f"Searching for {song_name} on YouTube Music")
                    search_url = f"https://music.youtube.com/search?q={song_name.replace(' ', '+')}"
                    webbrowser.open(search_url)
                else:
                    speak("Sorry, I didn't catch the song name.")
            except Exception as e:
                print(f"Error: {e}")
                speak("Sorry, I am unable to search for the song.")


        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'make a study schedule' in query:
            try:
                num_topics = getNumericInput("How many topics do you want to study?")
                if num_topics is None:
                    break

                hours = getNumericInput("How many hours do you have?")
                if hours is None:
                    break

                schedule = createSchedule(int(num_topics), hours)
                print(schedule)
                speak("Here is your study schedule")
                speak(schedule)
                saveNote(schedule)
            except Exception as e:
                print(f"Error: {e}")
                speak("Sorry, I couldn't create the schedule.")

        elif 'stop' in query or 'quit' in query:
            speak("Goodbye Sir!")
            break
