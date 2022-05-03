from flask import Flask, request
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret'
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins='*')
messages = []
users_online = {}
guests_count = 0
connections = []


def check_connection(connection):
    if connection in connections or {'target': connection['source'], 'source': connection['target']} in connections:
        return False
    return True


@socketio.on('connect')
def client_connect():
    emit('USER_ONLINE_PUBLIC_DATA', users_online)


@socketio.on('login')
def user_login(data):
    users_online[request.sid] = {
        'username': data['name'],
        'color': data['color']
    }
    emit('NEW_USER', {'id': request.sid, 'username': data['name'], 'color': data['color']}, broadcast=True)
    emit('CONNECTION_DATA', connections)


@socketio.on('disconnect')
def client_disconnect():
    print('disconnect')
    global connections
    if request.sid in users_online:
        username = {'id': users_online[request.sid]['username']}
        old_connections = [x for x in connections if
                           x['target'] == username or x['source'] == username]

        if len(old_connections) != 0:
            for conn in old_connections:
                connections.remove(conn)
            emit('CONNECTION_DATA', connections, broadcast=True)
        del users_online[request.sid]
        emit('DELETE_USER', {'id': request.sid, 'username': username['id']}, broadcast=True)


@socketio.on('send_message')
def client_send(data):
    global connections
    if data['msg'].strip() != '':
        message = {
            'user': users_online[request.sid]['username'],
            'msg': data['msg'],
            'type': "received",
        }
        new_connect = {'target': {'id': data['to']['username']}, 'source': {'id': data['user']}}
        if check_connection(new_connect):
            connections.append(new_connect)
            emit('NEW_CONNECTION', new_connect, broadcast=True)
        emit('MESSAGE', {
            'message': message,
            'to': data['to']['id'],
            'from': request.sid
        }, to=data['to']['id'])
        emit('MESSAGE_ANIMATION', new_connect, broadcast=True)
    else:
        print('empty message')


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=8000)
    app.run()
