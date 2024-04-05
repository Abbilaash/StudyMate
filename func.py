# importing needed libraries
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi as yta
import os


# initializing the needed API keys and models
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')



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
