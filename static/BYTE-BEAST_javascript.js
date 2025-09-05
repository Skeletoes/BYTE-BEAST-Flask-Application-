const CPU_graph = document.getElementById('CPU_chart').getContext('2d');

const CPU_config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'CPU Usage (%)',
            backgroundColor: 'rgb(4, 170, 109)',
            borderColor: 'rgb(4, 170, 109)',
            data: [],
            fill: true,
            tension: 0.3,
            animation: false,
        }]
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            x: {
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            },
            y: {
                beginAtZero: true,
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            }
        },
        plugins: {
            legend: {
                labels: { color: '#ccc' }
            }
        }
    }
};

const CPU_chart = new Chart(CPU_graph, CPU_config);

const MEMORY_graph = document.getElementById('MEMORY_chart').getContext('2d');

const MEMORY_config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Memory Usage (%)',
            backgroundColor: 'rgb(4, 170, 109)',
            borderColor: 'rgb(4, 170, 109)',
            data: [],
            fill: true,
            tension: 0.3,
            animation: false,
        }]
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            x: {
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            },
            y: {
                beginAtZero: true,
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            }
        },
        plugins: {
            legend: {
                labels: { color: '#ccc' }
            }
        }
    }
};

const MEMORY_chart = new Chart(MEMORY_graph, MEMORY_config);

const NETWORK_graph = document.getElementById('NETWORK_chart').getContext('2d');

const NETWORK_config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Bytes Received',
            backgroundColor: 'rgb(4, 100, 109)',
            borderColor: 'rgb(4, 100, 109)',
            data: [],
            fill: false,
            tension: 0.3,
            animation: false,
        },{
            label: 'Bytes Sent',
            backgroundColor: 'rgb(4, 255, 109)',
            borderColor: 'rgb(4, 255, 109)',
            data: [],
            fill: false,
            tension: 0.3,
            animation: false,
        }]
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            x: {
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            },
            y: {
                beginAtZero: true,
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            }
        },
        plugins: {
            legend: {
                labels: { color: '#ccc' }
            }
        }
    }
};

const NETWORK_chart = new Chart(NETWORK_graph, NETWORK_config);

const DISK_graph = document.getElementById('DISK_chart').getContext('2d');

const DISK_config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Bytes Read',
            backgroundColor: 'rgb(4, 100, 109)',
            borderColor: 'rgb(4, 100, 109)',
            data: [],
            fill: false,
            tension: 0.3,
            animation: false,
        },{
            label: 'Bytes Written',
            backgroundColor: 'rgb(4, 255, 109)',
            borderColor: 'rgb(4, 255, 109)',
            data: [],
            fill: false,
            tension: 0.3,
            animation: false,
        }]
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            x: {
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            },
            y: {
                beginAtZero: true,
                ticks: { color: '#ccc' },
                grid: { color: '#333' }
            }
        },
        plugins: {
            legend: {
                labels: { color: '#ccc' }
            }
        }
    }
};

const DISK_chart = new Chart(DISK_graph, DISK_config);

function fetchData() {
    fetch('/cpu-data')
        .then(response => response.json())
        .then(json => {
            CPU_chart.data.labels = json.cpu_data;
            CPU_chart.data.datasets[0].data = json.cpu_labels;
            CPU_chart.update();

            // Update CPU dropdown
            updateDropdown('cpu-dropdown', [
                `Cores: ${json.cpu_cores}`,
                `Physical Cores: ${json.cpu_physicalCores}`,
                `Frequency: ${json.cpu_frequency} MHz`
            ]);
        });
    fetch('/memory-data')
        .then(response => response.json())
        .then(json => {
            MEMORY_chart.data.labels = json.memory_data;
            MEMORY_chart.data.datasets[0].data = json.memory_labels;
            MEMORY_chart.update();

            // Update Memory dropdown
            updateDropdown('memory-dropdown', [
                `Total: ${json.memory_total} MB`,
                `Used: ${json.memory_used} MB`,
                `Available: ${json.memory_available} MB`
            ]);
        });
    fetch('/network-data')
        .then(response => response.json())
        .then(json => {
            NETWORK_chart.data.labels = json.network_data;
            NETWORK_chart.data.datasets[0].data = json.networkIn_labels;
            NETWORK_chart.data.datasets[1].data = json.networkOut_labels;
            NETWORK_chart.update();

            // Update Network dropdown
            updateDropdown('network-dropdown', [
                `Download: ${json.download} KB/s`,
                `Upload: ${json.upload} KB/s`
            ]);
        });
    fetch('/disk-data')
        .then(response => response.json())
        .then(json => {
            DISK_chart.data.labels = json.disk_data;
            DISK_chart.data.datasets[0].data = json.diskRead_labels;
            DISK_chart.data.datasets[1].data = json.diskWrite_labels;
            DISK_chart.update();

            // Update Disk dropdown
            updateDropdown('disk-dropdown', [
                `Read: ${json.read} MB/s`,
                `Write: ${json.write} MB/s`
            ]);
        });
}

function updateDropdown(id, stats) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return;
    dropdown.innerHTML = '';
    stats.forEach(stat => {
        const statElem = document.createElement('a');
        statElem.href = '#';
        statElem.textContent = stat;
        dropdown.appendChild(statElem);
    });
}



// Initial fetch
fetchData();

// Poll every second
setInterval(fetchData, 1000);

