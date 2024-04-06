from flask import Flask,render_template,request,send_file,jsonify,url_for,redirect,sessions
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import func

app = Flask(__name__)


# adding all the required variables and universal instatiations
utube_chatbot_text = """"""


# start the routing part of the application
# Route the main login page
@app.route('/utube_upload',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        global utube_chatbot_text
        youtube_url = request.form['youtube_url']
        pdf_file = request.files['pdf_file']
        if youtube_url or pdf_file:
            if youtube_url:
                utube_chatbot_text = func.youtube_transcript(youtube_url)
            else:
                utube_chatbot_text = func.get_text_pdf(pdf_file)
            return redirect(url_for('utube_chatbot'))
        else:
            return render_template('index.html')
    return render_template('index.html',username=sessions['username'])

# Route the utube chatbot page
@app.route('/utube_chatbot',methods=['GET','POST'])
def utube_chatbot():
    if request.method == 'POST':
        text = request.form.get('text')
        response = func.utube_chatbot(utube_chatbot_text,text)
        return render_template('utube_chatbot.html',user_message=text, ai_response=response)
    return render_template('utube_chatbot.html',response=utube_chatbot_text)



@app.route('/resume-generator',methods=['GET','POST'])
def resume_generator():
    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']
        education_entries = request.form.getlist('education-name')
        certification_entries = request.form.getlist('certifications-name')
        skill_entries = request.form.getlist('skills-name')
        technologies_entries = request.form.getlist('technologies-name')
        projects_entries = request.form.getlist('projects-name')
        phone = request.form['phone']
        email = request.form['email']
        linkedin = request.form['linkedin']
        github = request.form['github']

        resume_data = {
            "name":name,
            "about":about,
            "education_entries":education_entries,
            "certification_entries":certification_entries,
            "skill_entries":skill_entries,
            "technologies_entries":technologies_entries,
            "projects_entries":projects_entries,
            "phone":phone,
            "email":email,
            "linkedin":linkedin,
            "github":github,
        }
        return render_template('resume_sample.html', resume_data=resume_data)
    return render_template('resume-gen.html')



# Route the para rater page
@app.route('/para-rater')
def para_rater():
    return render_template('para-rater.html')


# Route the notes maker page
@app.route('/notes-generator',methods=['GET','POST'])
def notes_maker():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        preferences = request.form.getlist('preferences')
        generate_transcript = func.youtube_transcript(youtube_url)
    return render_template('notes-maker.html')





@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        func.signup(name,email,password)
        return redirect(url_for('login'))
    return render_template('signup.html')




@app.route("/",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['gmail']
        password = request.form['password']
        temp = func.verify_login(email,password)
        password = request.form['password']
        if temp != "":
            sessions['username'] = temp
            return redirect(url_for('index'))
    return render_template('login.html')






if __name__ == '__main__':
    app.run(debug=True)
