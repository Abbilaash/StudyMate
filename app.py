from flask import Flask,render_template,request,send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)

sessions = {}
sessions['username'] = "abbilaash"

# Route the main login page
@app.route('/')
def index():
    return render_template('index.html')


# Route the resume generator page
# This contains the youtube chatbot
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
@app.route('/notes-maker')
def notes_maker():
    return render_template('notes-maker.html')


# Route the profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')




if __name__ == '__main__':
    app.run(debug=True)
