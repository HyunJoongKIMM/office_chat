import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__, static_folder=".")
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('message')
def handle_message(msg):
    print(f"Message from {request.sid}: {msg}")
    # broadcast 인자 제거 (최신 버전에서는 지원 안됨)
    socketio.emit('message', {'id': request.sid, 'msg': msg})
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
