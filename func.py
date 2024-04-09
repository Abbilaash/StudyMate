# importing needed libraries
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi as yta
import os
import hashlib
import firebase_admin
from firebase_admin import credentials, firestore
from nltk.tokenize import word_tokenize
from nltk.corpus import words
import PyPDF2
import io


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

def generate_notes(preferences,transcript):
    prompt = f"Generate notes from the following transcript: {transcript} with few prefenreces like {preferences}. The should not contain the preferences but should be generated according to them"
    response_text = ""
    response = chat.send_message(prompt,stream=True)
    for chunk in response:
        response_text += chunk.text+" "
    notes_text = response.text
    sections = notes_text.split("\n\n")
    parsed_notes = {}
    for section in sections:
        lines = section.split("\n")
        heading = lines[0][2:-2]
        content = lines[1:]
        parsed_notes[heading] = content
    return parsed_notes

def highlight_spelling_error(paragraph):
    words_list = word_tokenize(paragraph)
    english_words = set(words.words())
    highlighted_words = []
    for word in words_list:
        if word.lower() not in english_words:
            highlighted_words.append(f'<span style="background-color: yellow;">{word}</span>')
        else:
            highlighted_words.append(word)
    highlighted_paragraph = ' '.join(highlighted_words)
    return highlighted_paragraph

def check_for_errors(paragraph):
    prompt = f"This is the text which i wrote {paragraph}. find all the spelling and grammar errrs in it."
    response_text = ""
    response = chat.send_message(prompt,stream=True)
    print(response)
    for chunk in response:
        response_text += chunk.text+" "
    return response_text

def add_para_to_db(paragraph,email):
    data = {'content':paragraph}
    doc_ref = db.collection('ParaRater').document(email)
    existing_data = doc_ref.get().to_dict()
    if existing_data:
        existing_data['content'].append(paragraph)
        doc_ref.set(existing_data)
    else:
        doc_ref.set({'values': data})

txts = model.start_chat(history=[])
def write_rater(input_para,email):
    doc_ref = db.collection("ParaRater").document(email)
    data = doc_ref.get().to_dict()['content']
    prompt = f"These are some of my previous texts i wrote: {data}. Now say what is my progress in writing paras by my latest writing {input_para}"
    response_text = ""
    response = txts.send_message(prompt,stream=True)
    for chunk in response:
        response_text += chunk.text+" "
    return response_text

def get_pdf_text(file):
    read_pdf = PyPDF2.PdfFileReader(io.BytesIO(file.read()))
    page = read_pdf.getPage(0)
    page_content = page.extractText()
    return page_content


