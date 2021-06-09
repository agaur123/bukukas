from flask import Flask, jsonify, request
import threading
import time

app = Flask(__name__)
lock = threading.Lock()

d = {}
d['data'] = {}

def update_thread():
    global d
    while True:
        with lock:
            d['uptime'] = d.get('uptime', 0) + 1
        time.sleep(1.0)

@app.route('/clear', methods=['GET'])
def clear():
    global d
    with lock:
        d['data'] = {}
        return jsonify(d)

@app.route('/get', methods=['GET'])
def get():
    with lock:
        return jsonify(d)

@app.route('/search')
def search():
    global d
    Dict = {}
    with lock:
        if request.args.get('prefix'):
            prefix = request.args.get('prefix')
            for key, value in d['data'].items():
                if key.startswith(prefix):
                    Dict[key]=value
            return jsonify(Dict)            
        elif request.args.get('suffix'):
            suffix = request.args.get('suffix')
            for key, value in d['data'].items():
                if key.endswith(suffix):
                    Dict[key]=value
            return jsonify(Dict)            


@app.route('/get/<name>', methods=['GET'])
def get_name(name):
    with lock:
        return jsonify(d['data'].get(name, {}))

@app.route('/set/<name>', methods=['GET', 'POST'])
def set(name):
    global d
    with lock:
        d['data'][name] = d['data'].get(name, {})
        d['data'][name]['value'] = request.args.get('value') or float('nan')
        d['data'][name]['time'] = time.time()
        return jsonify(d)

if __name__ == '__main__':
    threading.Thread(target=update_thread).start()
    app.run(threaded=True, debug=True)
    app.run(host='0.0.0.0')