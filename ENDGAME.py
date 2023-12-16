import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import requests

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.recognizer = sr.Recognizer()
        self.notes_path = "C:\\Users\\Arijeet Deb Roy\\Documents\\notes.txt"
        self.reminders_path = "C:\\Users\\Arijeet Deb Roy\\Documents\\reminders.txt"
        self.news_api_key = '669b85155b2446078f6a443f35ce98c8' 
        self.news_api_url = 'https://newsapi.org/v2/top-headlines'
        self.thesportsdb_api_key = '3'
        self.thesportsdb_api = TheSportsDBAPI(self.thesportsdb_api_key)

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")

        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")

        else:
            self.speak("Good Evening!")

        self.speak('I am Smile. Please tell me how may I help you')

    def take_command(self):
        with sr.Microphone() as source:
            print('Listening...')
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()

        except sr.UnknownValueError:
            print("Sorry, I did not hear your request. Please try again.")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "None"

    def send_email(self, to, content):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('youremail@gmail.com', 'your-password')
            server.sendmail('youremail@gmail.com', to, content)
            server.close()
            self.speak("Email has been sent!")

        except Exception as e:
            print(e)
            self.speak("Sorry, I am not able to send this email")

    def tell_joke(self):
        joke = pyjokes.get_joke()
        print(joke)
        self.speak(joke)

    def get_weather(self, city):
        api_key = '628bfa4f47edd1021cec74e13878c346'
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'appid': api_key, 'units': 'metric'}

        try:
            response = requests.get(base_url, params=params)
            weather_data = response.json()

            if response.status_code == 200:
                main_weather = weather_data['weather'][0]['main']
                description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']

                weather_info = f"The weather in {city} is {main_weather} ({description}) with a temperature of {temperature} degrees Celsius."
                return weather_info
            else:
                return "Unable to fetch weather information."

        except Exception as e:
            print(f"Error fetching weather information: {e}")
            return "Error fetching weather information."

    def set_reminder(self, reminder_text, time):
        with open(self.reminders_path, 'a') as reminders_file:
            reminders_file.write(f"{time}: {reminder_text}\n")

    def check_reminders(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        with open(self.reminders_path, 'r') as reminders_file:
            reminders = reminders_file.readlines()

        for reminder in reminders:
            reminder_time = reminder.split(': ')[0]
            if reminder_time == current_time:
                self.speak("Reminder: " + reminder.split(': ')[1].strip())

    def take_notes(self):
        self.speak("Opening Notepad for taking notes. You can start dictating now.")

        # Using speech recognition to transcribe speech to text
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            notes = self.recognizer.recognize_google(audio)
            print("You said: " + notes)

            # Save the notes to the specified file
            with open(self.notes_path, 'a') as notes_file:
                notes_file.write(notes + '\n')

            self.speak("Notes saved successfully.")

        except sr.UnknownValueError:
            print("Sorry, I could not understand your speech.")
            self.speak("Sorry, I could not understand your speech.")

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            self.speak("Sorry, there was an error with the speech recognition service.")

    def get_live_scores(self, sport):
        self.speak(f"Fetching live scores for {sport}")
        self.thesportsdb_api.get_live_scores(sport)

    def get_latest_news(self):
        self.speak("Fetching the latest news")
        params = {
            'apiKey': self.news_api_key,
            'country': 'us',  # You can change the country code if needed
        }

        try:
            response = requests.get(self.news_api_url, params=params)
            news_data = response.json()

            if response.status_code == 200:
                articles = news_data['articles'][:5]  # Displaying the top 5 articles
                for i, article in enumerate(articles, 1):
                    title = article['title']
                    self.speak(f"News {i}: {title}")

            else:
                self.speak("Unable to fetch the latest news.")

        except Exception as e:
            print(f"Error fetching the latest news: {e}")
            self.speak("Error fetching the latest news.")

class TheSportsDBAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://www.thesportsdb.com/api/v1/json/'

    def get_live_scores(self, sport):
        endpoint = f'1/latest/{sport}.php'
        params = {'apikey': self.api_key}

        try:
            response = requests.get(f'{self.base_url}/{endpoint}', params=params)
            data = response.json()

            # Process and display the live scores data as needed
            print(data)

        except Exception as e:
            print(f"Error retrieving live scores: {e}")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.wish_me()

    if 1:
        query = assistant.take_command()

        if 'wikipedia' in query:
            assistant.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            assistant.speak("According to Wikipedia")
            print(results)
            assistant.speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "open instagram" in query:
            webbrowser.open("instagram.com") 

        elif "open whatsapp" in query:
            webbrowser.open("web.whatsapp.com")

        elif "open spotify" in query:
            webbrowser.open("open.spotify.com")

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            assistant.speak(f"The time is {str_time}")

        elif 'open code' in query:
            code_path = "C:\\Users\\Arijeet Deb Roy\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)

        elif 'email' in query:
            assistant.speak("What should I say?")
            email_content = assistant.take_command()
            to_address = "your-email@gmail.com"  # Replace with the recipient's email address
            assistant.send_email(to_address, email_content)

        elif 'take notes' in query:
            assistant.take_notes()

        elif 'tell a joke' in query:
            assistant.tell_joke()

        elif 'weather' in query:
            assistant.speak("Please specify the city.")
            city = assistant.take_command()
            weather_info = assistant.get_weather(city)
            assistant.speak(weather_info)
            print(weather_info)

        elif 'set a reminder' in query:
            assistant.speak("What should I remind you?")
            reminder_text = assistant.take_command()
            assistant.speak("When should I remind you? Please specify the time.")
            reminder_time = assistant.take_command()

            # Validate the time format (you may need a more robust validation)
            if ':' in reminder_time and len(reminder_time.split(':')) == 2:
                assistant.set_reminder(reminder_text, reminder_time)
                assistant.speak("Reminder set successfully.")
            else:
                assistant.speak("Invalid time format. Please specify the time as HH:MM.")

        elif 'check reminders' in query:
            assistant.check_reminders()

        elif 'get live scores' in query:
            sport = query.replace("get live scores", "").strip()
            assistant.get_live_scores(sport)

        elif 'latest news' in query:
            assistant.get_latest_news()


