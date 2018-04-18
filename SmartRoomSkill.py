import logging

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():
    welcome_msg = render_template('Welcome To The CSH Smart Room Skill')
    return question(welcome_msg)

if __name__ == '__main__':
    app.run(debug=True)
