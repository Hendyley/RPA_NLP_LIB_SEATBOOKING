import telebot
from flask import Flask, request
import threading
from data.constants import API_KEY
import csv

# Create a new instance of the TeleBot class with your bot token
bot = telebot.TeleBot(API_KEY)
bot.set_webhook()

# reads csv file in data folder into a dictionary.
userdictionary = {}

with open('/home/HackathonServer/mysite/data/users.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        print(f'{row["username"]}, {row["user-id"]}.')
        userdictionary.update({row["username"]: row["user-id"]})
        line_count += 1
    print(f'Processed {line_count} lines.')

# Utility function to write to csv
def update_Dictionary():
	with open('/home/HackathonServer/mysite/data/users.csv', mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["username","user-id"])
            for entry in userdictionary:
                 writer.writerow([entry, userdictionary[entry]])

# Define a function that handles the /start command
@bot.message_handler(commands=['start', 'refresh'])
def send_welcome(message):
      user_idnum =  message.from_user.id
      user_username = message.from_user.username
      bot.reply_to(message, f"Hello, {message.from_user.username}, welcome to NewBie, please remember to use /refresh if you ever change your username!")
      if user_username not in userdictionary:
        userdictionary.update({user_username:user_idnum})
        update_Dictionary()


def send_a_message(receiver, message):
        if(receiver in userdictionary):
            bot.send_message(userdictionary[receiver], message)
            return 0
        else:
            return 1


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)


# Define a Flask app instance
app = Flask(__name__)

# Define a Flask route that handles incoming messages from Telegram
@app.route('/')
def hello_world():
    print('Hello, World!')
    return '<a href="send?receiver=&message=">test link text</a>'

# Define a Flask route for testing the server
@app.route('/send')
def hello():
    receiver = request.args.get('receiver')
    message = request.args.get('message')
    print('Hello, World!')
    send_a_message(receiver, message)
    return 'Hello, Flask!'

# Define a function that starts the polling loop
def run_polling():
    bot.polling(none_stop=True, interval=10000)

# Define a function that starts the Flask server
def run_flask():
    app.run()

# Start the polling loop in a separate thread
polling_thread = threading.Thread(target=run_polling)
polling_thread.start()

# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()
