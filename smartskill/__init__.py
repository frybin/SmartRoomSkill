import logging
import os
import requests
from flask import Flask, render_template
from flask_ask import Ask, statement, question

app = Flask(__name__)


# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))


ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
URL = "https://smartroom-api.csh.rit.edu/"


@ask.launch
def launch():
    welcome_msg = render_template('welcomeStatment')
    return question(welcome_msg)

@ask.intent("ShadesIntent")
def shades_intent():
    shades_url = URL+"shades"
    request = requests.get(url=shades_url)
    data = request.json()
    msg = render_template('shadeStatus', percent=data['shadeStatus'])
    return question(msg)

@ask.intent("ChangeShadesIntent", convert={'percent': int})
def change_shades_intent(percent):
    shades_url = URL+"shades"
    data = {'howOpen': percent}
    request = requests.post(url=shades_url, json=data, verify=True)
    if request.text == "Success":
        msg = render_template('ChangeShadesIntent', percent=percent)
    else:
        msg = render_template('failed')
    return statement(msg)
