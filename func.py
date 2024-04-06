# importing needed libraries
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi as yta
import os
import hashlib
import firebase_admin
from firebase_admin import credentials, firestore


# initializing the needed API keys and models
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

cred = credentials.Certificate('A:\HACKATHONS\SRM HACKATHON 8.0\SRM-Hackathon-8.0\studymate-256b0-firebase-adminsdk-gq2rk-0e5021aaf7.json')
firebase_admin.initialize_app(cred)
db = firestore.client()



def get_text_pdf(file):
    return 0


# prompting the model with the relevant information and the question
chat = model.start_chat(history=[])
def utube_chatbot(training_text,text):
    prompt = f"Here's the relevant information: {training_text}. Now, answer the question: {text}"
    response_text = ""
    try:
        response = chat.send_message(prompt,stream=True)
        for chunk in response:
            response_text += chunk.text+" "
    except Exception as e:
        response_text = 'Sorry, The given content you gave has some issues. Please try some other content.'
    return response_text


def youtube_transcript(url):
    url_id = url.split("=")[-1]
    data = yta.get_transcript(url_id)
    transcript = ""
    for value in data:
        for key,val in value.items():
            if key == "text":
                transcript += val + " "
    l = transcript.splitlines()
    final_tra = " ".join(l)
    return final_tra

def hashing(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()

def verify_login(gmail,password):
    users_ref = db.collection('users')
    query = users_ref.where('gmail', '==', hashing(gmail)).where('password', '==', hashing(password)).limit(1).get()
    for doc in query:
        return doc.get('username')  
    else:
        return ""
    
def signup(username,gmail,password):
    user_ref = db.collection('users').document()
    user_ref.set({
        'username': username,
        'gmail': hashing(gmail),
        'password': hashing(password)
    })
    
#print(hashing("user@gmail.com"))
#print(hashing("password"))
