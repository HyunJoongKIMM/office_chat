import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder=".")
socketio = SocketIO(app, async_mode='eventlet')

usernames = {}  # { sid: name }

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('set_name')
def handle_set_name(data):
    name = data['name']
    if name in usernames.values():
        # 이미 존재하는 이름이면 거부
        emit('name_error', {'error': '이미 사용 중인 이름입니다. 다른 이름을 입력해주세요.'})
        return
    usernames[request.sid] = name
    print(f"{name} 입장 ({request.sid})")
    emit('notice', {'msg': f"👤 {name} 님이 입장하셨습니다."}, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    name = usernames.get(request.sid, '익명')
    print(f"[{name}]: {msg}")
    socketio.emit('message', {'id': request.sid, 'name': name, 'msg': msg})

@socketio.on('disconnect')
def handle_disconnect():
    name = usernames.pop(request.sid, '익명')
    print(f"{name} 퇴장 ({request.sid})")
    socketio.emit('notice', {'msg': f"🚪 {name} 님이 퇴장하셨습니다."}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)