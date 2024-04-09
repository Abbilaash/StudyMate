from flask import Flask,render_template,request,send_file,jsonify,url_for,redirect,session
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import func,nltk
import PyPDF2

nltk.download('punkt')
nltk.download('words')


app = Flask(__name__)
app.secret_key = 'hg5YV4gtfs67vttsbVF'


# adding all the required variables and universal instatiations
utube_chatbot_text = """"""


# start the routing part of the application
# Route the main login page
@app.route('/utube_upload',methods=['GET','POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            global utube_chatbot_text
            youtube_url = request.form['youtube_url']
            pdf_file = request.files['pdf_file']
            if youtube_url or pdf_file:
                if youtube_url:
                    utube_chatbot_text = func.youtube_transcript(youtube_url)
                else:
                    reader = PyPDF2.PdfReader(pdf_file)
                    number_of_pages = len(reader.pages)
                    page = reader.pages[0]
                    text = page.extract_text()
                    utube_chatbot_text = text
                return redirect(url_for('utube_chatbot'))
            else:
                return render_template('index.html')
        return render_template('index.html',username=session['username'])
    else:
        return redirect(url_for('login'))

# Route the utube chatbot page
@app.route('/utube_chatbot',methods=['GET','POST'])
def utube_chatbot():
    if 'username' in session:
        if request.method == 'POST':
            text = request.form.get('text')
            response = func.utube_chatbot(utube_chatbot_text,text)
            return render_template('utube_chatbot.html',user_message=text, ai_response=response)
        return render_template('utube_chatbot.html',response=utube_chatbot_text)
    else:
        return redirect(url_for('login'))



@app.route('/resume-generator',methods=['GET','POST'])
def resume_generator():
    if 'username' in session:
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
    else:
        return redirect(url_for('login'))


# Route the para rater page
@app.route('/para-rater',methods=['GET','POST'])
def para_rater():
    if request.method == 'POST':
        paragraph = request.form['paragraph']
        #p = func.highlight_spelling_error(paragraph)
        p = func.check_for_errors(paragraph)
        try:
            func.add_para_to_db(paragraph,session['email'])
        except:
            pass
        suggestion = func.write_rater(paragraph,session['email'])
        return redirect(url_for('para_rater_result', paragraph=p,suggestion=suggestion))
    return render_template('para-rater.html')

@app.route('/para-rater-result', methods=['GET'])
def para_rater_result():
    paragraph = request.args.get('paragraph', '')
    suggestion = request.args.get('suggestion', '')
    return render_template('para-rater.html', paragraph=paragraph,suggestion=suggestion)









# Route the notes maker page
@app.route('/notes-generator',methods=['GET','POST'])
def notes_maker():
    if 'username' in session:
        if request.method == 'POST':
            youtube_url = request.form['youtube_url']
            preferences = request.form.getlist('preferences')
            generate_transcript = func.youtube_transcript(youtube_url)
            notes = func.generate_notes(preferences,generate_transcript)
            return render_template('generated_notes.html', parsed_notes=notes)


        return render_template('notes-maker.html')
    else:
        return redirect(url_for('login'))


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
        email = request.form['email']
        password = request.form['password']
        temp = func.verify_login(email,password)
        if temp != "":
            session['username'] = temp
            session['email'] = email
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('username',None)
    session.pop('email',None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
