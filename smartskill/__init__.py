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


ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
URL = "https://smartroom-api.csh.rit.edu/"


@ask.launch
def launch():
    welcome_msg = render_template('welcomeStatment')
    return question(welcome_msg).simple_card(
        title='Welcome to CSH SmartRoom', content='say Shades to interact with the windows')

@ask.intent("ShadesIntent")
def shades_intent():
    shades_url = URL+"shades"
    request = requests.get(url=shades_url)
    data = request.json()
    msg = render_template('shadeStatus', percent=data['howOpen'])
    return question(msg).simple_card(title='Window Blinds control', content='say Shades to interact with the windows')

@ask.intent("ChangeShadesIntent", convert={'percent': int})
def change_shades_intent(percent):
    shades_url = URL+"shades"
    data = {'howOpen': percent}
    request = requests.post(url=shades_url, json=data, verify=True)
    if request.text == "Success":
        msg = render_template('ChangeShadesIntent', percent=percent)
    else:
        msg = render_template('failed')
    return statement(msg).simple_card(
        title='Welcome to CSH SmartRoom', content='say Shades to interact with the windows')

@ask.intent("CloseShadesIntent")
def close_shades_intent():
    shades_url = URL+"shades"
    data = {'howOpen': 100}
    request = requests.post(url=shades_url, json=data, verify=True)
    msg = render_template('CloseShadesIntent')
    return statement(msg)
    # if request.text == "Success":
    #     msg = render_template('CloseShadesIntent')
    # else:
    #     msg = render_template('failed')
    # return statement(msg)

@ask.intent("OpenShadesIntent")
def open_shades_intent():
    shades_url = URL+"shades"
    data = {'howOpen': 0}
    request = requests.post(url=shades_url, json=data, verify=True)
    msg = render_template('OpenShadesIntent')
    return statement(msg)
    # if request.text == "Success":
    #     msg = render_template('OpenShadesIntent')
    # else:
    #     msg = render_template('failed')
    # return statement(msg)

@ask.intent("AMAZON.HelpIntent")
def help_intent():
    msg = render_template('help')
    return statement(msg).simple_card(title='Smart Room Help Commands', content=msg)

@ask.intent("ShadeStatusHelp")
def status_help_intent():
    msg = render_template('ShadeStatusHelp')
    return statement(msg).simple_card(title='Smart Room Help Commands', content=msg)

@ask.intent("ChangeShadesHelp")
def change_help_intent():
    msg = render_template('ChangeShadesHelp')
    return statement(msg).simple_card(title='Smart Room Help Commands', content=msg)
    
@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
    response = "Thank you for coming to the Smart Room, Goodbye"
    return statement(response).simple_card('', response)

@ask.intent('AMAZON.StopIntent')
def stop_intent():
    response = "Thank you for coming to the Smart Room, Goodbye"
    return statement(response).simple_card('', response)