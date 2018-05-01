from flask import Flask, render_template, session, current_app

app = Flask(__name__)


@app.route('/')
def hi():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()