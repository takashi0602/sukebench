from flask import Flask, jsonify, render_template
from flask_bootstrap import Bootstrap
from machine_info import MachineInfo

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html',
                           cpu_info = MachineInfo.fetch_cpu_info(),
                           memory_info = MachineInfo.fetch_memory_info(),
                           swap_info = MachineInfo.fetch_swap_info(),
                           disks_info = MachineInfo.fetch_disks_info(),
                           network_info = MachineInfo.fetch_network_info(),
                           procs_info = MachineInfo.fetch_procs_info(),
                           device_info = MachineInfo.fetch_device_info())

@app.route('/api/cpu')
def cpu():
    return jsonify({})

@app.route('/api/memory')
def memory():
    return jsonify({})

@app.route('/api/swap')
def swap():
    return jsonify({})

@app.route('/api/disks')
def disks():
    return jsonify({})

@app.route('/api/network')
def network():
    return jsonify({})

@app.route('/api/procs')
def procs():
    return jsonify({})

@app.route('/api/devices')
def devices():
    return jsonify({})

@app.route('/api/hello')
def hello():
    return jsonify({'hello': 'world'})

if __name__ == '__main__':
    app.run(debug=True)