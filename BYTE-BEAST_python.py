# Import required libraries
from flask import Flask, render_template, jsonify  # Flask web framework components
import psutil  # For system and process utilities
from flaskwebgui import FlaskUI  # For creating desktop-like GUI
import webbrowser  # For opening URLs in browser
import threading  # For running concurrent tasks
import requests  # For making HTTP requests
import time  # For time-related functions

# Initialize Flask application
app = Flask(__name__)

# Lists to store historical data for various system metrics
# Each list stores the last 10 data points for graphing
cpu_stats = []  # CPU usage percentages
cpu_time = []   # Timestamps for CPU measurements
memory_stats = []  # Memory usage percentages
memory_time=[]    # Timestamps for memory measurements
networkIn_stats = []  # Network incoming bytes
networkOut_stats = [] # Network outgoing bytes
network_time = []     # Timestamps for network measurements
diskRead_stats = []   # Disk read bytes
diskWrite_stats = []  # Disk write bytes
disk_time = []        # Timestamps for disk measurements

# Route for the main application page
@app.route('/')
def homepage():
    return render_template('BYTE-BEAST_html.html')

# Route to get CPU statistics and information
@app.route('/cpu-data')
def cpu_data():
    # Get current CPU usage percentage
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_stats.append(cpu_percent)
    
    # Get CPU frequency information
    cpu_freq1 = psutil.cpu_freq()
    cpu_freq2 = cpu_freq1.current
    
    # Get number of CPU cores (logical and physical)
    cpu_cores = psutil.cpu_count(logical=True)
    cpu_physicalCores = psutil.cpu_count(logical=False)

    cpu_time1 = time.time()
    cpu_time2 = time.ctime(cpu_time1)
    cpu_time.append(cpu_time2[11:19])
    
    cpu_data = cpu_time[-10:]
    cpu_labels = cpu_stats[-10:]
    time.sleep(0.2)

    return jsonify({'cpu_labels': cpu_labels, 'cpu_data': cpu_data, 'cpu_frequency': cpu_freq2, 'cpu_cores': cpu_cores, 'cpu_physicalCores': cpu_physicalCores})

# Route to get memory usage statistics
@app.route('/memory-data')
def memory_data():
    # Get current memory usage percentage
    memory_percent = psutil.virtual_memory().percent
    memory_stats.append(memory_percent)
    
    # Calculate memory metrics in MB
    memory_available = psutil.virtual_memory().available // (1024 * 1024)  # Available memory in MB
    memory_total = psutil.virtual_memory().total // (1024 * 1024)         # Total memory in MB
    memory_used = psutil.virtual_memory().used // (1024 * 1024)          # Used memory in MB

    memory_time1 = time.time()
    memory_time2 = time.ctime(memory_time1)
    memory_time.append(memory_time2[11:19])

    memory_data = memory_time[-10:]
    memory_labels = memory_stats[-10:]
    time.sleep(0.3)

    return jsonify({'memory_labels': memory_labels, 'memory_data': memory_data, 'memory_available': memory_available, 'memory_total': memory_total, 'memory_used': memory_used})

# Route to get network traffic statistics
@app.route('/network-data')
def network_data():
    # Get initial network counters
    network = psutil.net_io_counters()
    bytesIn1 = network[0]
    bytesOut1 = network[1]
    time.sleep(0.1)  # Wait briefly to measure rate
    
    # Get updated network counters
    network = psutil.net_io_counters()
    bytesIn2 = network[0]
    bytesOut2 = network[1]
    time.sleep(0.1)
    
    # Calculate network throughput (bytes/sec)
    bytesIn = bytesIn2 - bytesIn1
    bytesOut = bytesOut2 - bytesOut1
    packetsSent = network.packets_sent
    packetsRecv = network.packets_recv

    networkIn_stats.append(bytesIn)
    networkOut_stats.append(bytesOut)

    network_time1 = time.time()
    network_time2 = time.ctime(network_time1)
    network_time.append(network_time2[11:19])

    network_data = network_time[-10:]
    networkIn_labels = networkIn_stats[-10:]
    networkOut_labels = networkOut_stats[-10:]

    return jsonify({'networkIn_labels': networkIn_labels, 'networkOut_labels': networkOut_labels, 'network_data': network_data, 'packetsSent': packetsSent, 'packetsRecv': packetsRecv})

# Route to get disk I/O and usage statistics
@app.route('/disk-data')
def disk_data():
    # Get initial disk I/O counters
    disk = psutil.disk_io_counters()
    bytes_read1 = disk.read_bytes
    bytes_write1 = disk.write_bytes
    time.sleep(0.1)  # Wait briefly to measure rate
    
    # Get updated disk I/O counters
    disk = psutil.disk_io_counters()
    bytes_read2 = disk.read_bytes
    bytes_write2 = disk.write_bytes
    time.sleep(0.1)

    # Calculate disk I/O rates and space usage in MB
    bytes_read = bytes_read2 - bytes_read1
    bytes_write = bytes_write2 - bytes_write1
    disk_available = psutil.disk_usage('/').free // (1024 * 1024)  # Free space in MB
    disk_total = psutil.disk_usage('/').total // (1024 * 1024)     # Total space in MB
    disk_used = psutil.disk_usage('/').used // (1024 * 1024)       # Used space in MB

    diskRead_stats.append(bytes_read)
    diskWrite_stats.append(bytes_write)

    diskTime1 = time.time()
    diskTime2 = time.ctime(diskTime1)
    disk_time.append(diskTime2[11:19])

    disk_data = disk_time[-10:]
    diskRead_labels = diskRead_stats[-10:]
    diskWrite_labels = diskWrite_stats[-10:]

    return jsonify({'diskRead_labels': diskRead_labels, 'diskWrite_labels': diskWrite_labels, 'disk_data': disk_data, 'disk_available': disk_available, 'disk_total': disk_total, 'disk_used': disk_used})


# Uncomment to auto-open browser when server starts
#def open_browser_when_ready(url): 
#    import time, requests, webbrowser
#    for _ in range(60):  # Try for up to 30 seconds
#        try:
#            requests.get(url)
#            webbrowser.open(url)
#            return
#        except Exception:
#            time.sleep(0.5)

if __name__ == '__main__':
    #Uncomment to auto-open browser when server starts
    #threading.Thread(target=open_browser_when_ready, args=("http://127.0.0.1:8000",)).start()
    #FlaskUI(app=app, server="flask", width=800, height=480, port=8000, browser_path=None).run()
    FlaskUI(app=app, server="flask", width=800, height=480, port=8000).run()

