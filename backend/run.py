from app import create_app, socketio

app = create_app('default')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)    