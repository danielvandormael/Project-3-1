from flask import Flask, render_template
from flask_socketio import SocketIO

import object_detection

"""
This App is used for the communication with the external server that sends the data about robot intentions

Function handle_message is called when a message is received from the server
In order to add nore functionality, add more if statements in the handle_message function and call specific module

For now recognized messages are:
    - ObjectMovement XXX (Where XXX is the ID of the object that is being moved)
"""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    # Connect to the HTML file
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    # This is the function that will be called when a message is sent from the server
    print('Received message: ' + data)
    if data.split(" ")[0] == "ObjectMovement":
        object_detection.object_movement(data.split(" ")[1])


if __name__ == '__main__':
    print("Running Flask App")
    socketio.run(app, debug=True)
