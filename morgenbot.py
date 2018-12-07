import os
import re
import sys
import traceback
import json
import datetime
import time
import random
from slacker import Slacker
from flask import Flask, request
from datetime import date

debug = os.getenv('DEBUG', False)
app = Flask(__name__)
app.debug = debug

curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)

slack = Slacker(os.getenv('TOKEN'))
username = os.getenv('USERNAME', 'morgenbot')
icon_emoji = os.getenv('ICON_EMOJI', ':coffee:')
channel = os.getenv('CHANNEL', '#standup')

start_message = os.getenv('START_MESSAGE', 'What did you work on yesterday? What are you working on today? What, if any, are your blockers?')

def post_message(text, attachments=[]):
    slack.chat.post_message(channel     = channel,
                            text        = text,
                            username    = username,
                            parse       = 'full',
                            link_names  = 1,
                            attachments = attachments,
                            icon_emoji  = icon_emoji)


def start():
    post_message(start_message)


@app.route("/", methods=['POST'])
def main():
    # ignore message we sent
    msguser = request.form.get("user_name", "").strip()
    if msguser == username or msguser.lower() == "slackbot": return

    text = request.form.get("text", "")

    match = re.findall(r"^!(\S+)", text)
    if not match: return

    command = match[0]
    args = text[text.find("!%s" % command) + len(command) + 1:]
    command = command.lower()
    
    if command == "start":
        start()
        return json.dumps({ })

    return json.dumps({ })


@app.route("/daily", methods=['GET'])
def daily():
    if date.today().weekday() in [0,1,2,3,4,5]:
        start()


if __name__ == "__main__":
    app.run(debug=True)
