import speech_recognition as sr
import os
import pyttsx3
import wikipedia
import pyjokes
import requests
import datetime
import google.generativeai as genai
import subprocess

genai.configure(api_key="AIzaSyCImJfYRetBPqLOAJz1guox1Do7SAvCLP8")

def takeCommand():
    print("Listening...")
    os.system("arecord -d 5 -f cd -t wav output.wav")
    with sr.AudioFile('output.wav') as source:
        r = sr.Recognizer()
        r.pause_threshold = 1
        try:
            audio = r.record(source)
            print("Recognizing...")    
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            print("Unable to Recognizing your voice.")  
            return "repeat after me! \'I was not able to hear what you say!, can you please repeat?\'"
    return query


def speak(text):
    os.system(f"gtts-cli \"{text}\" --output speech.mp3")
    os.system("ffplay -v 0 -nodisp -autoexit speech.mp3")

if __name__ == '__main__':
    subprocess.Popen(['aplay','prompt.wav'])
    query = takeCommand().lower()
    if 'lpc ps' in query or 'lp cps' in query:
        query = query.replace('lpc ps', 'lpcps')
        query = query.replace('lp cps', 'lpcps')
        print(query)
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=3)
        speak("Answer From Wikipedia")
        print(results)
        speak(results)

    elif "good morning" in query:
        speak("A warm" +query)
        speak("How are you Mister")

    elif "wikipedia" in query and "hindi" in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        query = query.replace("hindi", "")
        results = wikipedia.summary(query, sentences=3)
        speak("According to Wikipedia")
        r = sr.Recognizer()
        results = r.recognize_google(results, language='hi')
        print(results)
        speak(results)  

    elif 'play music' in query or "play song" in query or "gaana"in query or "song" in query:
        #music_dir = "G:\\Song"
        username = getpass.getuser()
        music_dir = "C:\\Users\\"+username+"\\Music"
        songs = os.listdir(music_dir)
        print(songs)    
        random=os.startfile(os.path.join(music_dir, songs[1]))

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"Sir, the time is {strTime}")

    elif "samay" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"samaye hai {strTime}")

    elif 'how are you' in query:
        speak("I am fine , Thank you")
        speak("How are you, Sir")

    elif "what's your name" in query or "what is your name" in query or "what ise your name" in query:
        speak("My friends call me, Vidushi")
        print("My friends call me Vidushi")

    elif "who made you" in query or "who created you" in query: 
        speak("I have been created by Students of Lucknow Public College of Professional Studies.")


    elif "who i am" in query:
        speak("If you talk then definately you are human.")

    elif "why you came to world" in query:
        speak("Thanks to LPCPS. further It's a secret")

    elif 'is love' in query:
        speak("It is 7th sense that destroy all other senses")

    elif "who are you" in query:
        speak("I am your Humanoid Robot Developed in LPCPS")

    elif "don't listen" in query or "stop listening" in query:
        speak("for how much time you want to stop me from listening commands")
        a=int(takeCommand())
        time.sleep(a)
        print(a)

    elif "vidushi" in query:
        speak("Vidushi 1 point o is here.")
        # speak(assname)

    elif "will you be my gf" in query or "will you be my bf" in query:   #most asked question from google Assistant
        speak("I'm not sure about , may be you should give me some time")

    elif "how are you" in query or "how r u" in query:
        speak("I'm fine, glad you asked me that")

    elif "i love you" in query:
        speak("It's hard to understand")
    elif "lpc" in query or 'lps' in query or 'cps' in query or 'lucknow public college' in query:
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content("""LPCPS is one of the most coveted colleges for admission for Degree Programs in the Northern India. The institute brings together knowledge, research and industry experience in one place and confers upon its graduates, professional degrees which are recognized globally. 
            The college offers a wide variety of courses and unique research opportunities related to one's academic and co-curricular interests for achieving their goals.
            The college’s approach is towards holistic development of its students, creation of global knowledge eco-system through innovations, research and development, substantial industry exposure, good placement opportunities and great infrastructure and fantastic results makes one opt for this institution.
            College also runs language courses for international students which results in global exposure to our students and develops a sense of commonness and belongingness.
            Strength of the Institution that makes LPCPS the first choice among students and aspirants.
            LPCPS has 14+ Year of Legacy, 350+ Placed Students, 1,850+ Alumni, 40+ Faculty Strength
            LPCPS is one of the most coveted colleges for admission for Degree Programs in the Northern India. The institute brings together knowledge, research and industry experience in one place and confers upon its graduates, professional degrees which are recognized globally.
            The professional degrees offered after the successful completion of the undergraduate programs are certified by UGC, the statutory body overseeing the running of universities and colleges in India. The degrees are affiliated to the University of Lucknow, one of the oldest government owned institutions of Indian higher education.
            LPCPS boasts of having eminent personalities from Industry background as well as academia background among its board. Their experience and expertise in their respective domains was one of the main reasons why LPCPS attained its professional reputation in a short time.
            Commitment to excellence is the top most priority of all the domains in the college – academia, training and skill development, placement cell, research wing, consultancy division are the most prominent among them.
            The spectacular success achieved by the college in such a short time is the result of the foresight, exceptionally dynamic leadership and the able guidance of the visionary founder manager.
            The highly talented and motivated team of professional educators and facilitators have made it their mission to make LPCPS one of the top most institutions in the field of professional education in the Asian continent.
            LPCPS is established and managed by Lucknow Public Educational Society at Rajajipuram in the city of Lucknow. The society has made its name in the Indian subcontinent as a brand ambassador and a stalwart in the field of education. The strategic decision by the society to establish LPCPS as a sprawling campus in the posh and fast developed zone of Gomtinagar made sure that, the teachers and students are able to enjoy the huge lush green setting and a panoramic location in a peaceful and conducive environment.
            Vision of lpcps: Excellence for all, Excellence from all is the epitome of our academic eco-system. In a caring and positive environment, the college provides education to enrich its students to manifest their full potential, to achieve high standards of excellence in academic society, research and hands on projects as well as in supportive areas of physical, cultural and social development, inculcating civic and human values.
            mission: To nurture individual talent to optimize their full potential and to inculcate professional, social and cultural values through holistic approach by providing world class education.
            general manager of lpcps: Mr. S. P. Singh,
            Dean academics: Dr. Laxmi Shankar Awasthi,
            director: Ms. garima Singh. Ms. Neha Singh and Mr. Arpit Singh
             {}
        """.format(query+", provide only short answer upto one or two sentence"))
        print(response.text)
        answer=response.text.replace('*'," ")
        answer=answer.replace('"'," ")
        answer=answer.replace("'"," ")
        answer=answer.replace('-'," ")
        speak(answer)
    elif ('umaga' in query) or ('omega' in query) or ('umang' in query) or ('umada' in query) or ('a technologies' in query):
        query = query.replace('omega', 'umaga')
        query = query.replace('umang', 'umaga')
        query = query.replace('umada', 'umaga')
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content("""Umaga technologies is a company empowering Students with AI, IoT, and Robotics Education.
        Umaga technologies partner with schools to open a BrainPi Lab in their institution. Umaga' BrainPi Lab for Schools in this digital era applying practical curriculum with technological skill disciplines like Coding, Artificial Intelligence, Robotics, and Machine Learning!
        By partnering with Umaga Technologies, prestigious institutions will be positioned clearly above other schools. Our commitment to establishing and executing Robotics and Innovation Labs ensures that your students receive a unique educational experience that sets them apart in the competitive world.
        Umaga Technologies Private Limited is a leading provider of Robotics and Innovation Labs for educational institutions with a mission to position institutes above others by offering students the platform to develop skills for their bright future.
        Founded in 2019, Umaga Technologies is a privately-owned company based in India that has established a significant reputation for providing a platform as Umaga Labs (Umaga Robotics and Innovation Lab / Umaga Center of Excellence) where students can turn an innovative idea into reality and practice industry demanding skills in the field of Artificial Intelligence (AI) and Internet of Things (IoT) based Robotics. 
        Our mission is to position education institutions above others by offering students the opportunity to develop skills in high demand in the industry.
        Robotics education fosters an environment of innovation, encouraging students to think outside the box and develop novel solutions to complex problems.
        We strive for excellence in providing robotics education to students, equipping them with the skills needed to thrive in the industry.
        We empower students to become future innovators by fostering creativity, critical thinking, and problem-solving abilities.
        We are at the forefront of technological advancements, constantly pushing boundaries and embracing innovation.
        founder and ceo: Mr. Prabhat Mishra
        Co-founder: Mr. Prashant Mishra
        Cheif Technical Officer: Mr. Zuhaib Khan
        Cheif Managing Officer: Mr. Ravi Tiwari
        Cheif Operations Officer: Mr. Prashant Shukla
        Operations Head: Mr. Abhishant Bajpai
        General Manager: Mr. Sudhakar Soni
        Advising Member: Mr. Amod Pandey (Quantum Computing expert, DRDO).
        {}
        """.format(query+", provide only short answer upto one or two sentence"))
        answer=response.text.replace('*'," ")
        answer=answer.replace('"'," ")
        answer=answer.replace("'"," ")
        answer=answer.replace('-'," ")
        print(response.text)
        speak(answer)
    else:
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content("Your name is Vidushi, and your are a humanoid robot made in Lucknow Public College of Professional Studies. "+query+", provide only short answer upto one or two sentence")
        answer=response.text.replace('*'," ")
        answer=answer.replace('"'," ")
        answer=answer.replace("'"," ")
        answer=answer.replace('-'," ")
        print(response.text)
        speak(answer)
