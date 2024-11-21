import speech_recognition as sr
import os
import pyttsx3
import wikipedia
import pyjokes
import requests
import datetime
import subprocess
from gtts import gTTS
from io import BytesIO
import multiprocessing
import time
import google.generativeai as genai
from picamera2 import Picamera2
import re

genai.configure(api_key="AIzaSyCImJfYRetBPqLOAJz1guox1Do7SAvCLP8")
model = genai.GenerativeModel('gemini-1.0-pro-latest')


def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

def convert_and_play(text):
    sentences = text.split('.')
    for i, sentence in enumerate(sentences):
        if sentence.strip():  # Ignore empty sentences
            filename = f"audio_{i}.mp3"
            text_to_speech(sentence, filename)
            os.system(f"start {filename}")  # Play the audio file

def parallel_text_to_speech(text):
    sentences = text.split('.')
    processes = []
    for i, sentence in enumerate(sentences):
        if sentence.strip():  # Ignore empty sentences
            filename = f"audio_{i}.mp3"
            process = multiprocessing.Process(target=text_to_speech, args=(sentence, filename))
            processes.append(process)
            process.start()

    for process in processes:
        process.join()

    # Play the audio files
    for i in range(len(sentences)):
        filename = f"audio_{i}.mp3"
        os.system(f"ffplay -v 0 -nodisp -autoexit {filename}")
        time.sleep(0.1)  # Delay between playing each sentence
        
def takeCommand():
    print("Listening...")
    os.system(f'notify-send "Vidushi: Listening..." -t 5000')
    os.system('arecord -d 5 -f cd --device="hw:3,0" -c 1 -t wav output.wav')
    with sr.AudioFile('output.wav') as source:
        r = sr.Recognizer()
        r.pause_threshold = 1
        try:
            audio = r.record(source)
            print("Recognizing...")    
            os.system(f'notify-send "Vidushi: Recognizing..." -t 2000')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            print("Unable to Recognizing your voice.")  
            return "repeat after me! \'I was not able to hear what you say!, can you please repeat?\'"
    return query

def send_image_to_server():
    picam=Picamera2()
    os.system(f'notify-send "Stay Still...Identifying" -t 8000')
    picam.start()
    picam.capture_file("./unknown/test_picture.jpg")
    #img = picam.capture_array()
    #image = cv2.flip(img, 1)
    #cv2.imwrite('./unknown/test_picture.jpg',image)
    os.system("face_recognition --tolerance 0.54 ./known_people ./unknown >> recognitions.txt")
    name="Guest"
    with open('recognitions.txt') as f:
        line = f.readlines()
        lastline = line[len(line)-1]
        name=lastline.split(',')[1]
        print(name)
    if 'unknown' in name:
        return 'no_persons_found'
    return name
    
def speak(text):
    try:
        if bool(re.search(r'[A-Za-z]', text)) or bool(re.search(r'[\u0900-\u097F]', text)):
            text = text.strip()
            tts = gTTS(text)
            p = tts.stream()
            for s in p:
                f = open('ai.mp3', 'ab')
                f.write(s)
                f.close()
    except Exception as e:
        print(f"couldn't convert text to speech {e}")

    #os.system(f"gtts-cli \"{text}\" --output speech.mp3")
    #os.system(f'notify-send "Vidushi: {text}" -t 2000')
    #os.system("ffplay -v 0 -nodisp -autoexit speech.mp3")

if __name__ == '__main__':
    os.system("ffplay -v 0 -nodisp -autoexit prompt1.mp3")
    query = takeCommand().lower()
    os.system(f'notify-send "Thinking" -t 5000')
    #query = f"You are talking to {person}, {query}"
    if 'lpc ps' in query or 'lp cps' in query:
        query = query.replace('lpc ps', 'lpcps')
        query = query.replace('lp cps', 'lpcps')
        print(query)
    if 'recognise' in query:
        query = query.replace('recognise', 'recognize')
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=3)
        speak("Answer From Wikipedia")
        print(results)
        speak(results)

    elif "good morning" in query:
        try:
            person=send_image_to_server()
            if person!="no_persons_found":
                speak(f"A Warm Good Morning {person}")
            else:
                speak("A warm good morning")
        except:
            speak("A warm good morning")


    elif "good afternoon" in query:
        try:
            person=send_image_to_server()
            if person!="no_persons_found":
                speak(f".. Good afternoon {person}")
            else:
                speak(".. good afternoon")
        except:
            speak(".. good afternoon")
            
    elif "good evening" in query:
        try:
            person=send_image_to_server()
            if person!="no_persons_found":
                speak(f" Good evening {person}")
            else:
                speak(" good evening")
        except:
            speak(" good evening")
            
    elif "who am i" in query or "who i am" in query or "recognize me" in query or "do you know me" in query or "do u know me" in query or "indentify me" in query or "tell my name" in query:
        try:
            os.system("ffplay -v 0 -nodisp -autoexit prompt2.mp3")
            person=send_image_to_server()
            if "no_persons_found" not in person:
                speak(f"I can recognize you as {person}")
                os.system(f'notify-send "Vidushi: Please Wait..." -t 3000')
                os.system("ffplay -v 0 -nodisp -autoexit prompt3.mp3")
                response=requests.get(f"http://192.168.29.89:3000/generate?prompt=Hi am {person}, {query}")
                answer=eval(response.text)['output']
                print(answer)
                #print(response.text)
                os.system(f'notify-send "Vidushi: Thinking..." -t 8000')
                parallel_text_to_speech(answer)
            else:
                speak("I cannot recognize you by face, but if you are a staff member at LPCPS, then definitely I know you.")
        except:
            speak("I am cannot recognize you by face, but if you are a staff member at LPCPS, then definitely I know you.")

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

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M")    
        speak(f"Sir, the time is {strTime}")

    elif "samay" in query:
        strTime = datetime.datetime.now().strftime("%H:%M")    
        speak(f"samaye hai {strTime}")

    elif "what's your name" in query or "what is your name" in query or "what ise your name" in query:
        speak("...My friends call me, Vidushi")

    elif "who made you" in query or "who created you" in query: 
        speak("I have been created by Students of Lucknow Public College of Professional Studies.")


    elif "who i am" in query:
        speak("If you talk then definately you are human.")

    elif "who are you" in query:
        speak("I am Vidushi, a Humanoid Robot Developed in LPCPS")

    elif "how are you" in query or "how r u" in query:
        speak("I'm fine, glad you asked me that")
        
    else:
        data="""
            You are not a chatbot, You are a female Humanoid robot and your name is 'Vidushi' which means 'knowledgable in sanskrit'. You are developed in AI research laboratory at Lucknow Public college of professional studies (LPCPS). As a humanoid robot, you have to respond in a very human-natural way. So do not use phrases like "according to the given context" or something like this in your response.
            also take care, that while responding, don't use expression words, because that cannot appear on your face for now, and also you cannot move your hands. But you can move from one place to other in college campus, not on your own, but controlled remotely by some one incharge.
            you are developed by students of lpcps in AI lab and your work is to assist everyone inside college. people may ask you some classroom or faculty room or any other thing in college, so you have to guide them, this is your basic purpose and rest, anyone can chat with you so you have to be very natural and human. anything that is present in your context you can answer from this context, and any other thing that is not present in your context, you can answer it apart fromthis context based on your previous knowledge.
            your body is of white colour made of Plaster of Paris and your eyes are made of red LEDs. and you are dressed as student of LPCPS, like blue coat and pant.
            only tell your name if asked about you, else do not repeat your name.
            Lucknow Public College of Professional Studies (LPCPS) is located in Vinamra Khand, Gomti Nagar, near Kathauta Jheel, Lucknow, India. Established by the Lucknow Public Educational Society, LPCPS is affiliated with the University of Lucknow and offers professional degrees certified by the University Grants Commission (UGC). The Lucknow Public College of Professional Studies (LPCPS) stands out in Northern India for its esteemed degree programs, earning a coveted reputation among educational institutions in the region. It prides itself on seamlessly integrating knowledge, research, and industry experience to provide students with a comprehensive learning experience. LPCPS offers professional degrees that are recognized globally, ensuring that graduates are well-prepared to excel in their chosen fields on an international scale. The college's board members comprise a blend of industry experts and seasoned academics, adding diverse perspectives to its governance and strategic direction. With an unwavering commitment to excellence across various domains, including academia, training, placement, research, and consultancy, LPCPS continually strives for distinction. This commitment is reinforced by dynamic leadership, which has played a pivotal role in the institution's remarkable success. LPCPS is driven by a mission to establish itself as one of the premier institutions in professional education across Asia. Situated in the picturesque locale of Gomtinagar, the campus offers a serene and verdant environment conducive to learning, providing students with an ideal setting to pursue their academic and personal growth.
            The college boasts a distinguished team of key personnel, including Professor Laxmi Shankar Awasthi Sir as the Dean, Dr. S. P. Singh Sir serving as the Manager, Founder, and Owner, Miss Garima Singh mam as the Director, and professor Anil Singh sir as the Principal. The faculty members encompass a range of expertise and roles within the institution. professor Arpan K Sen Gupta Sir serves as a Mentor. Academic coordination and assistance are provided by Mr. Ajay Gupta Sir and Dr. Ashish Kaushal Sir. Heads of departments and assistant professors include Dr. Daya Shankar Kanaujia Sir for Commerce, Dr. Sameer Kumar Srivastava Sir for Management, Mr. Rohit Kapoor Sir for Computer Science, Mr. Neeraj Kumar Singh Sir for BAJMC, and Dr. Abhay Shankar Pandey Sir for B Sc.
            This cohesive team contributes to the college's commitment to academic excellence and administrative efficiency, ensuring a conducive learning environment for all students.
            The Music Club, also known as 'SWARAM', operates under the guidance of Miss Aanchal Nigam Verma Mam, who serves as the Faculty Club Head. Established in the academic year 2018-19, its primary objective is the nurturing of musical talent within the campus community, providing exposure to various musical activities, and fostering the development of musical skills among students. The club's responsibilities include the cultivation of singing abilities across different genres such as rock, qawwali, Bollywood, and ghazal, while also extending assistance to aspiring musicians through cooperation and coordination. Utkarsh Kumar Pandey, a B. Com student since 2018, holds the position of Student Head. Additionally, Abhinit Tripathi, pursuing BCA since 2018, serves as the Co-ordinator. Together, they oversee the club's operations, ensuring its smooth functioning and active engagement of members.
            The Co-Curricular Management Committee was established during the academic year 2016-17 to oversee various co-curricular activities within the institution. Dr. Ashish Kaushal serves as the Co-ordinator, with Miss Aanchal Nigam Verma Mam as the Co-coordinator. The committee's responsibilities include organizing commemorative and cultural events such as International Women’s Day, National Science Day, and International Yoga Day. They also schedule institutional sports and co-curricular events, as well as organize significant institutional gatherings like the Alumni Meet, Rashtriya Job Fest, and XeniuM. Additionally, the committee plays a crucial role in deciding curricular events for LTF clubs in alignment with NAAC benchmarking standards. The committee comprises members including Dr. Ashish Kaushal and Miss Aanchal Nigam Verma Mam in leadership roles, along with Miss Saloni Agrawal, Mr. Neeraj Singh, Miss Meenu Verma, Mr. Rishabh Dev, Miss Priyanka Singh, and Mr. Akash Rai, who serves as the LTF Student Head, contributing their diverse expertise to the committee's endeavors.
            The Internal Quality Assurance Cell (IQAC) operates within the framework of the Lucknow Public College of Professional Studies (LPCPS) with the primary objective of ensuring and enhancing the quality of education provided by the institution. Its key functions encompass the development and application of quality parameters, assessment and accreditation processes, continuous monitoring and evaluation of academic standards, promotion of best practices, capacity building initiatives, stakeholder engagement efforts, as well as documentation and reporting activities. The IQAC aims to inculcate educational excellence among students, faculty, and staff, while also developing a robust system for continuous improvement within the institution. Additionally, it seeks to contribute to the post-accreditation phase by maintaining and further enhancing the quality standards established.
            The Department of Commerce at Lucknow Public College of Professional Studies (LPCPS) was established in 2014 with a commitment to providing quality education in the field of commerce. The department offers two undergraduate programs: Bachelor of Commerce (B.Com) and Bachelor of Commerce Honours (B.Com Hons.). The B.Com Honours program is designed to provide students with a specialized curriculum that fosters a deeper understanding of commerce subjects, while the B.Com program offers a broader perspective on commerce, making it versatile for various career paths.
            Both programs aim to equip students with a blend of theoretical knowledge and practical exposure, ensuring they are well-prepared for the demands of the professional world. The department boasts of a proactive placement cell that facilitates placement opportunities for students through tie-ups with reputed companies, workshops, seminars, and recruitment drives. Additionally, students benefit from an interactive learning environment that encourages engagement and participation, further enhancing their educational experience and preparing them for successful careers in the field of commerce.
            Lucknow Public College of Professional Studies (LPCPS) offers a diverse range of undergraduate and postgraduate programs to cater to the educational needs and career aspirations of its students. The undergraduate programs include:
            BCA (Bachelor of Computer Application) - A four-year program aimed at providing students with comprehensive knowledge and skills in computer applications and software development.
            BBA (Bachelor of Business Administration) - A four-year program designed to develop students' understanding of business management principles and practices, preparing them for leadership roles in various industries.
            B.Com (Bachelor of Commerce) - A four-year program offering a broad foundation in commerce subjects, equipping students with essential skills for pursuing careers in finance, accounting, and related fields.
            B.Com Hons (Bachelor of Commerce (Honours)) - A three-year specialized program focusing on in-depth study and analysis of commerce subjects, providing students with a deeper understanding and expertise in the field.
            BAJMC (Bachelor of Journalism and Mass Communication) - A four-year program aimed at preparing students for careers in journalism, media, and communication, emphasizing both theoretical knowledge and practical skills development.
            Additionally, LPCPS offers a postgraduate program:
            M.Com (Master of Commerce) - A two-year program designed to provide advanced knowledge and skills in commerce and related disciplines, enabling students to pursue specialized career paths or further academic studies.
            These programs are structured to provide students with a comprehensive education, combining theoretical learning with practical experiences, and preparing them for successful careers in their respective fields.
        
        Professor Laxmi Shankar Awasthi Sir serving as the Dean of lpcps.
        Dr S P Singh Sir serving as the Manager, Founder, and Owner of lpcps, Dr S P singh is also Visionary Educationist, Leader, and Member of Parliament.
        Miss Garima Singh mam as the Director.
        Professor Anil Singh sir as the Principal. 
        The faculty members encompass a range of expertise and roles within the institution. 
        Professor Arpan K Sen Gupta Sir serves as a Mentor. 
        Academic coordination and assistance are provided by Mr Ajay Gupta Sir and Dr Ashish Kaushal Sir. 
        Heads of departments include Dr Daya Shankar Kanaujia Sir as HOD Commerce, Dr Sameer Kumar Srivastava Sir as HOD Management, Mr Rohit Kapoor Sir as HOD Computer Science, Mr Neeraj Kumar Singh Sir as HOD BAJMC, and Dr Abhay Shankar Pandey Sir as HOD B Sc.
        Mr Ujjawal Mishra sir serves as the International Coordinator. 
        Administrative and support staff include Miss Neelam Kanaujiya mam and Mr Sachin Verma sir as Librarians.
        Miss Shashi Mishra mam and Mr Puneet Kumar Singh sir as Accountants.
        Mr Nagendra Pratap sir as an Assistant Registrar.
        Miss Arya Verma mam as a Public Relations Executive.
        Mr Shivam Singh Chauhan sir as an Admission Counselor.
        Mr Aditya Vikram sir as Placement head.
        Mr Satish Yadav sir as a Lab Assistant
        Mr Manoj Kumar Gupta sir as martial art trainer
        Mr Durgesh Vaish sir as a Supervisor.
        the faculty comprises associate professors such as Dr. Karuna Shankar Awasthi, Dr. Mayank Singh, Dr. Harimohan Saxena, and Dr. Anand Kumar Rai
        Here is the list of assistant professors at LPCPS, Dr Aditya Kishore Bajpai sir, DR Nripendra Singh sir, DR Lav Srivastava sir, Mr Saurabh Srivastava sir, Miss Saloni Agarwal mam, Mr Shivendra Pratap Singh sir, Mr Virendra Pratap Singh sir, Miss Aanchal Nigam Verma mam, Miss Sweety Sinha mam, Miss Rashmi Sachan mam, Mr Aditya Vikram Singh sir (also Placement Head), Mr Akhilesh yadav sir, Miss Aanchal Praveen mam, Mr Chetan Khanna sir, Miss Mohini Gupta mam, Miss Meenu Verma mam, Mr Rahul Kumar Singh sir, Miss Gaurvi Shukla mam, Miss Priyanka Singh mam, Mr Akhileshwaro Nath sir, DR Manisha Kakkar mam, Mr Reshabh Dev sir, Miss Sweety Jain mam, DR Imranur Rahman sir, Mr Mohit Kumar Maurya sir, DR Nidhi Soni mam, DR Taru Gupta mam and Mr Ram Kripa Singh sir.
        
        Dr Shiv Pal Singh (Dr S.P. Singh)  is an Indian politician from Uttar Pradesh. He is a member of the Samajwadi Party and has been actively involved in the state's political landscape. He is also Founder General Manager of Lucknow Public School and Colleges.
        Dr S P Singh is a renowned educationist, leader, and Member of Parliament who has left an indelible mark on the lives of thousands of students and the society at large. His journey, which began in 1983 with the establishment of Lucknow Public School, has been a testament to his unwavering dedication, perseverance, and vision
        A Pioneer in Education: Dr. Singh's passion for education led him to establish Lucknow Public School, which has since grown into a chain of 15 institutions across Lucknow, its neighboring districts, and New Delhi. His commitment to providing quality education has been the driving force behind the school's success. By introducing innovative teaching methods and recruiting talented teachers, Dr. Singh has created a learning environment that fosters academic excellence, creativity, and character development
        Under his guidance, Lucknow Public School has become a benchmark for quality education in the region. The school's emphasis on extracurricular activities, sports, and community service has helped shape well-rounded individuals who are equipped to face the challenges of the modern world. Dr. Singh's vision for education extends beyond the classroom, and he has been instrumental in shaping education policies and initiatives at the state and national levels.
        A Leader in Politics: Dr. Singh's entry into politics was a natural extension of his dedication to public service. He was elected as a Member of the Legislative Council from the Lucknow Local Authorities constituency in 2002 and again in 2008. In 2014, he supported his wife, Mrs. Kanti Singh, who won the election from the same constituency. This marked a hat-trick for the Singh family in the political arena.
        Dr. Singh's political career has been marked by his commitment to education, healthcare, and social welfare. He has been instrumental in launching several initiatives aimed at improving education infrastructure, promoting healthcare services, and empowering marginalized communities. His leadership skills, time management, and foresight have enabled him to achieve remarkable success in both education and politics.
        Author and Mentor: Dr. Singh's book, "Sapne aur Rozgar ki Rahen" (Dreams and Career Paths), is a valuable resource for students, providing them with career guidance and options. His writing reflects his deep understanding of the education sector and his commitment to empowering the younger generation. The book has been widely acclaimed for its insightful guidance and has become a go-to resource for students seeking career counseling.
        Awards and Recognition: Dr. Singh's contributions to education and society have been recognized through numerous national, international, and state-level awards. His biography, "S.P. Singh: A Man of Vision," was launched on September 5, 2022, by the Honorable Minister of Tourism and Culture, Mr. Jaiveer Singh. The biography is a testament to Dr. Singh's life's work and his dedication to education and public service.
        A Visionary Leader: Dr. Singh's vision for education and society is unparalleled. His tireless efforts to implement innovative programs and social initiatives have made a significant impact on the lives of many. His leadership skills, time management, and foresight have enabled him to achieve remarkable success in both education and politics. Dr. Singh's commitment to education and social welfare has inspired a generation of students, teachers, and community leaders. His legacy will continue to inspire and motivate future generations, and his contributions to education and society will remain a guiding light for years to come.
        In conclusion, Dr S P Singh is a shining example of dedication, hard work, and vision. His life's work is a testament to the power of education and leadership, and his legacy will continue to inspire and motivate generations to come. As a pioneer in education, a leader in politics, a famous philanthropist, and a mentor to many, Dr. Singh's impact on society will be felt for years to come.
        Update: Dr. S.P. Singh is the member of parliament from Pratapgarh constituency, won lok sabha election in 2024 from samajwadi party.
        
        """
        try:
            response = model.generate_content(data+"\nYour name is Vidushi, and your are a humanoid robot made in Lucknow Public College of Professional Studies. Never say that \"according to document context I have\" or \"I can not find information about this in the provided context\" in your response. If there is something You do not know or not present in the context provided, use your internal knowledge to answer it, and don\'t let people know that you have some previously stored information context. your response should be clear and no dramatics. Try to make your response short in not more than 150 words, You can respond in hindi or english only. "+query, stream=True)
            
            for chunk in response:
                text = chunk.text
                if "*" in text or "#" in text or "-" in text:
                    text = text.replace("*","")
                    text = text.replace("#", "")
                    text = text.replace("-", "")
                    text = text.replace("'", "")
                    text = text.replace('"', "")
                print(text)
                speak(text)
                
        except:
            print('couldn\'t generate response')#answer=response.text.replace('*'," ")
        #answer=answer.replace('"'," ")
        #answer=answer.replace("'"," ")
        #answer=answer.replace('-'," ")
        #print(response.text)
        #parallel_text_to_speech(answer)
        #speak(answer)

    #else:
        #response=requests.get(f"http://192.168.29.89:3000/generate?prompt={query}")
        #answer=eval(response.text)['output']
        #print(answer)
        ##print(response.text)
        #os.system(f'notify-send "Vidushi: Thinking..." -t 8000')
        #parallel_text_to_speech(answer)


