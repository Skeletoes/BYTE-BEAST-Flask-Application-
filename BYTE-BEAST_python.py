from flask import Flask, render_template, jsonify
import psutil
import time
from flaskwebgui import FlaskUI

app = Flask(__name__)

cpu_stats = []
cpu_time = []
memory_stats = []
memory_time=[]
networkIn_stats = []
networkOut_stats = []
network_time = []
diskRead_stats = []
diskWrite_stats = []
disk_time = []

@app.route('/')
def homepage():
    return render_template('BYTE-BEAST_html.html')

@app.route('/cpu-data')
def cpu_data():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_stats.append(cpu_percent)

    cpu_time1 = time.time()
    cpu_time2 = time.ctime(cpu_time1)
    cpu_time.append(cpu_time2[11:19])
    
    cpu_data = cpu_time[-30:]
    cpu_labels = cpu_stats[-30:]
    time.sleep(0.2)

    return jsonify({'cpu_labels': cpu_labels, 'cpu_data': cpu_data})

@app.route('/memory-data')
def memory_data():
    memory_percent = psutil.virtual_memory().percent
    memory_stats.append(memory_percent)

    memory_time1 = time.time()
    memory_time2 = time.ctime(memory_time1)
    memory_time.append(memory_time2[11:19])

    memory_data = memory_time[-30:]
    memory_labels = memory_stats[-30:]
    time.sleep(0.2)

    return jsonify({'memory_labels': memory_labels, 'memory_data': memory_data})

@app.route('/network-data')
def network_data():
    network = psutil.net_io_counters()
    bytesIn1 = network[0]
    bytesOut1 = network[1]
    time.sleep(0.1)
    network = psutil.net_io_counters()
    bytesIn2 = network[0]
    bytesOut2 = network[1]
    time.sleep(0.1)
    
    bytesIn = bytesIn2 - bytesIn1
    bytesOut = bytesOut2 - bytesOut1

    networkIn_stats.append(bytesIn)
    networkOut_stats.append(bytesOut)

    network_time1 = time.time()
    network_time2 = time.ctime(network_time1)
    network_time.append(network_time2[11:19])

    network_data = network_time[-30:]
    networkIn_labels = networkIn_stats[-30:]
    networkOut_labels = networkOut_stats[-30:]

    return jsonify({'networkIn_labels': networkIn_labels, 'networkOut_labels': networkOut_labels, 'network_data': network_data})

@app.route('/disk-data')
def disk_data():
    disk = psutil.disk_io_counters()
    bytes_read1 = disk.read_bytes
    bytes_write1 = disk.write_bytes
    time.sleep(0.1)
    disk = psutil.disk_io_counters()
    bytes_read2 = disk.read_bytes
    bytes_write2 = disk.write_bytes
    time.sleep(0.1)

    bytes_read = bytes_read2 - bytes_read1
    bytes_write = bytes_write2 - bytes_write1

    diskRead_stats.append(bytes_read)
    diskWrite_stats.append(bytes_write)

    diskTime1 = time.time()
    diskTime2 = time.ctime(diskTime1)
    disk_time.append(diskTime2[11:19])

    disk_data = disk_time[-30:]
    diskRead_labels = diskRead_stats[-30:]
    diskWrite_labels = diskWrite_stats[-30:]

    return jsonify({'diskRead_labels': diskRead_labels, 'diskWrite_labels': diskWrite_labels, 'disk_data': disk_data})


if __name__ == '__main__':
    # app.run(debug=True)
    FlaskUI(app=app, server="flask", width=800, height=480).run()