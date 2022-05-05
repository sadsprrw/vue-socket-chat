from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret'
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins='*')
messages = []
users_online = {
    '1': {'username': 'David', 'color': '#123112', 'id': '1'},
    '2': {'username': 'Nick', 'color': '#177B5DFF', 'id': '2'},
    '3': {'username': 'John', 'color': '#501A4FFF', 'id': '3'},
    '4': {'username': 'Ben', 'color': '#EED90BFF', 'id': '4'},
    '5': {'username': 'Hanna', 'color': '#E66099FF', 'id': '5'},
    '6': {'username': 'Gleb', 'color': '#D8EA10FF', 'id': '6'},
    '7': {'username': 'Dimitryi', 'color': '#10EABEFF', 'id': '7'},
    '8': {'username': 'Andrew', 'color': '#EA1010FF', 'id': '8'},
    '9': {'username': 'Igor', 'color': '#FF3900FF', 'id': '9'},
    '10': {'username': 'Olga', 'color': '#B1FF00FF', 'id': '10'},
    '11': {'username': 'Ru', 'color': '#0088FFFF', 'id': '11'},
    '12': {'username': 'Vivi', 'color': '#7C5EFEFF', 'id': '12'},
    '13': {'username': 'Jen', 'color': '#FEE35EFF', 'id': '13'},
    '14': {'username': 'Brock', 'color': '#FE5E5EFF', 'id': '14'},
    '15': {'username': 'San', 'color': '#6D0D19FF', 'id': '15'},
}
guests_count = 0
connections = [
    {'target': {'id': 'David'}, 'source': {'id': 'Nick'}},
    {'target': {'id': 'Nick'}, 'source': {'id': 'John'}},
    {'target': {'id': 'David'}, 'source': {'id': 'John'}},
    {'target': {'id': 'Ben'}, 'source': {'id': 'Hanna'}},
    {'target': {'id': 'David'}, 'source': {'id': 'Ben'}},
    {'target': {'id': 'Brock'}, 'source': {'id': 'San'}},
    {'target': {'id': 'Jen'}, 'source': {'id': 'San'}},
    {'target': {'id': 'Vivi'}, 'source': {'id': 'Ru'}},
    {'target': {'id': 'Vivi'}, 'source': {'id': 'Olga'}},
    {'target': {'id': 'Olga'}, 'source': {'id': 'Ru'}},
    {'target': {'id': 'Vivi'}, 'source': {'id': 'Hanna'}},
    {'target': {'id': 'Igor'}, 'source': {'id': 'Dimitryi'}},
    {'target': {'id': 'Gleb'}, 'source': {'id': 'Igor'}},
    {'target': {'id': 'Dimitryi'}, 'source': {'id': 'Gleb'}},
    {'target': {'id': 'Ben'}, 'source': {'id': 'Olga'}},
]


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
        'color': data['color'],
        'id': request.sid
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
