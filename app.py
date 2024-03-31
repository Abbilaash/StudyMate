from flask import Flask

app = Flask(__name__)


# Route for rendering the chat interface
@app.route('/')
def index():
    return "Hello!"

if __name__ == '__main__':
    app.run(debug=True)
