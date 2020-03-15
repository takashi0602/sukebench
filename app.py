import psutil, datetime

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

def sec2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return '%d:%02d:%02d' % (hh, mm, ss)

def fetch_cpu_info():
    cpu_info = {
        'use_rate': psutil.cpu_percent(),
        'load_average': psutil.getloadavg(),
        'real_count': psutil.cpu_count(logical=False),
        'logical_count': psutil.cpu_count(),
        'frequency': psutil.cpu_freq().current / 1000,
    }
    return cpu_info

def fetch_memory_info():
    memory_info = {
        'total': psutil.virtual_memory().total / 1_000_000_000,
        'available': psutil.virtual_memory().available / 1_000_000_000,
        'used': psutil.virtual_memory().used / 1_000_000_000,
    }
    return memory_info

def fetch_swap_info():
    swap_info = {
        'total': psutil.swap_memory().total / 1_000_000_000,
        'free': psutil.swap_memory().free / 1_000_000_000,
        'used': psutil.swap_memory().used / 1_000_000_000,
    }
    return swap_info

def fetch_disks_info():
    disks_info = {
        'total': psutil.disk_usage(path='/').total / 1_000_000_000,
        'free': psutil.disk_usage(path='/').free / 1_000_000_000,
        'used': psutil.disk_usage(path='/').used / 1_000_000_000,
        'use_rate': psutil.disk_usage(path='/').percent,
        'partitions': psutil.disk_partitions(),
        'read_count': '{:,d}'.format(psutil.disk_io_counters().read_count),
        'write_count': '{:,d}'.format(psutil.disk_io_counters().write_count),
        'read_bytes': '{:,d}'.format(psutil.disk_io_counters().read_bytes),
        'write_bytes': '{:,d}'.format(psutil.disk_io_counters().write_bytes),
    }
    return disks_info

def fetch_network_info():
    network_info = {
        'bytes_sent': '{:,d}'.format(psutil.net_io_counters().bytes_sent),
        'bytes_recv': '{:,d}'.format(psutil.net_io_counters().bytes_recv),
        'packets_sent': '{:,d}'.format(psutil.net_io_counters().packets_sent),
        'packets_recv': '{:,d}'.format(psutil.net_io_counters().packets_recv),
        'errin': '{:,d}'.format(psutil.net_io_counters().errin),
        'errout': '{:,d}'.format(psutil.net_io_counters().errout),
        'dropin': '{:,d}'.format(psutil.net_io_counters().dropin),
        'dropout': '{:,d}'.format(psutil.net_io_counters().dropout),
        'connections': psutil.net_connections(),
        'addrs': psutil.net_if_addrs(),
        'stats': psutil.net_if_stats(),
    }
    return network_info

def fetch_procs_info():
    procs_info = {
        'procs': psutil.process_iter(['pid', 'name', 'username']),
    }
    return procs_info

def fetch_device_info():
    # sensors_temperatures, sensors_fans はmacOS環境では取れず
    device_info = {
        'procs': psutil.process_iter(['pid', 'name', 'username']),
        'users': psutil.users(),
        'battery_percent': psutil.sensors_battery().percent,
        'battery_secleft': sec2hours(psutil.sensors_battery().secsleft),
        'battery_power_plugged': psutil.sensors_battery().power_plugged,
        'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y/%m/%d %H:%M:%S"),
    }
    return device_info

@app.route('/')
def index():
    return render_template('index.html',
                           cpu_info = fetch_cpu_info(),
                           memory_info = fetch_memory_info(),
                           swap_info = fetch_swap_info(),
                           disks_info = fetch_disks_info(),
                           network_info = fetch_network_info(),
                           procs_info = fetch_procs_info(),
                           device_info = fetch_device_info())

if __name__ == '__main__':
    app.run(debug=True)