import tkinter as tk
import subprocess
import psutil
import os
import re
import time
from shutil import disk_usage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####   CPU temperature monitor   #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

# Get CPU temperature
def get_cpu_temperature():
    temps = psutil.sensors_temperatures()
    if not temps:
        return None
    for name, entries in temps.items():
        for entry in entries:
            if "cpu" in entry.label.lower() or "core" in entry.label.lower():
                return entry.current
    return None

# CPU temperature plot tracking state
cpu_temp_data = {
    "start_time": time.time(),
    "times": [],
    "temps": [],
    "line": None
}

# Plot CPU temperature monitor
def plot_cpu_temperature(ax, canvas):
    ax.clear()
    current_temp = get_cpu_temperature()
    current_time = time.time() - cpu_temp_data["start_time"]
    if current_temp is not None:
        cpu_temp_data["times"].append(current_time)
        cpu_temp_data["temps"].append(current_temp)
        cpu_temp_data["times"] = cpu_temp_data["times"][-60:]
        cpu_temp_data["temps"] = cpu_temp_data["temps"][-60:]
        ax.plot(cpu_temp_data["times"], cpu_temp_data["temps"], color="red", label="CPU Temp (°C)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("CPU Temperature Monitor", fontweight='bold')
        ax.legend()
        ax.relim()
        ax.autoscale_view()
    canvas.draw()

#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####             RAM             #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

# Plot RAM
def plot_ram_usage(ax, canvas):
    mem = psutil.virtual_memory()
    total = mem.total / (1024 ** 3)
    available = mem.available / (1024 ** 3)
    used = (mem.total - mem.available) / (1024 ** 3)
    ax.clear()
    ax.pie([used, available], labels=['Used', 'Free'],
           autopct='%1.2f%%', textprops={'fontsize': 12}, colors=['#ff6666', '#66b3ff'])
    ax.set_title("RAM", fontweight='bold')
    ax.axis('equal')
    canvas.draw()

# RAM informations
def update_ram_label():
    mem = psutil.virtual_memory()
    total = mem.total / (1024 ** 3)
    available = mem.available / (1024 ** 3)
    used = (mem.total - mem.available) / (1024 ** 3)
    buffers = mem.buffers / (1024 ** 3)
    cached = mem.cached / (1024 ** 3)
    summary = (
        f"    Used: {used:.2f} GB ({(used/total)*100:.2f}%) \n"
        f"     Free: {available:.2f} GB ({(available/total)*100:.2f}%)\n"
        f"    Total: {total:.2f} GB \n\n"
        f" Buffers: {buffers:.2f} GB \n"
        f"Cached: {cached:.2f} GB \n\n"
    )
    ram_label.config(text=summary)
    root.after(1000, update_ram_label)

#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####           Storage           #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

# Storage values
def get_disk_usage(path='/'):
    total, used, free = disk_usage(path)
    reserved = total - (used + free)
    total_gb = total / 1024**3
    used_gb = used / 1024**3
    free_gb = free / 1024**3
    reserved_gb = reserved / 1024**3
    return total_gb, used_gb, free_gb, reserved_gb

# Storage plot
def plot_pie_Disk(ax):
    total, used, free, reserved = get_disk_usage()
    ax.pie([used, free, reserved], labels=['Used', 'Free', 'Reserved'], autopct='%1.2f%%', textprops={'fontsize': 12}, colors=['#ff6666', '#66b3ff', '#cccccc'])
    ax.set_title("Storage", fontweight='bold')

# Storage informations
totalDISK, usedDISK, freeDISK, reservedDISK = get_disk_usage()
storage = 'Storage'
storage_Used=f"       Used: {usedDISK:.2f} GB ({(usedDISK/totalDISK)*100:.2f}%)"
storage_Free=f"        Free:   {freeDISK:.2f} GB ({(freeDISK/totalDISK)*100:.2f}%)"
storage_Reserved=f"Reserved:   {reservedDISK:.2f} GB ({(reservedDISK/totalDISK)*100:.2f}%)"
storage_Total=f"       Total: {totalDISK:.2f} GB \n\n\n"

# Storage Output
Storage_titulo = f"""{storage}"""
Storage_info = f"""{storage_Used}
{storage_Free}
{storage_Reserved}
{storage_Total}
"""
#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####     Run Linux Commands      #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

# Run Linux commands
def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, text=True)
        return output.strip()
    except subprocess.CalledProcessError:
        return "Command failed or not available"

#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####          Software           #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

def get_debian_version():
    try:
        version = subprocess.check_output("cat /etc/debian_version", shell=True, text=True).strip()
        if version == "bookworm/sid":
            return "Debian 12"
        elif version == "trixie/sid":
            return "Debian 13"
        elif version == "forky/sid":
            return "Debian 14"
        else:
            return f"Unknown Debian version ({version})"
    except subprocess.CalledProcessError:
        return "Debian version check failed"

# Commands
kernel_cmd = "echo Kernel $(uname -r | cut -d'-' -f1)"
ubuntu_version_cmd = "echo Ubuntu $(uname -v | grep -oP '\\d+\\.\\d+' | head -n1) LTS"
distro_desc_cmd = "lsb_release -d | cut -f2-"
gnome_version_cmd = "gnome-shell --version"

# Run commands and get outputs
Software = 'Software (operating system)'
kernel = '\u2022 ' + run_command(kernel_cmd)
debian_version = '\u2022 ' + get_debian_version()
ubuntu_version = '\u2022 ' + run_command(ubuntu_version_cmd)
distro_description = '\u2022 ' + run_command(distro_desc_cmd)
gnome_version = '\u2022 ' + run_command(gnome_version_cmd) + '\n\n'

# System Info Output
stitulo = f"""{Software}"""
sinfo = f"""{kernel}
{debian_version}
{ubuntu_version}
{distro_description}
{gnome_version}
"""

#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####          Hardware           #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

def get_number_of_threads():
    return psutil.cpu_count(logical=True)

def get_number_of_cores():
    return psutil.cpu_count(logical=False)

def get_total_cpu_cache():
    total_cache_kb = 0
    index = 0
    while True:
        path = f'/sys/devices/system/cpu/cpu0/cache/index{index}/size'
        if not os.path.exists(path):
            break
        try:
            with open(path, 'r') as f:
                size_str = f.read().strip()
                if size_str.endswith('K'):
                    total_cache_kb += int(size_str[:-1])
                elif size_str.endswith('M'):
                    total_cache_kb += int(size_str[:-1]) * 1024
        except Exception as e:
            print(f"Error reading {path}: {e}")
        index += 1
    return f"Cache: {round(total_cache_kb/1024, 0)} MB"

def get_ram_gb():
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal:'):
                mem_kb = int(line.split()[1])
                mem_gb = mem_kb / 1024 / 1024
                mem_gb = round(mem_gb, 2)
                return f"RAM: {mem_gb} GB"

def get_disk_models():
    result = subprocess.run(
        ['lsblk', '-d', '-o', 'MODEL,TYPE'],
        stdout=subprocess.PIPE,
        text=True
    )
    models = []
    for line in result.stdout.strip().split('\n')[1:]:  # skip header
        parts = line.strip().rsplit(None, 1)  # split MODEL and TYPE
        if len(parts) == 2:
            model, type_str = parts
            if type_str == 'disk' and model != '':
                models.append(model)
    return models

def get_monitor_refresh_rate_linux():
    try:
        xrandr_output = subprocess.check_output(['xrandr'], encoding='utf-8')
        match = re.search(r'(\d+\.\d+)\*', xrandr_output)
        if match:
            return f"Display: {float(match.group(1))} Hz"
    except Exception as e:
        print(f"Error: {e}")
    return None

# Commands
Manuf_cmd = "echo $(sudo dmidecode | grep -A3 '^System Information' | grep 'Manufacturer:' | cut -d: -f2 | sed 's/^ *//')"
Product_cmd = "echo $(fastfetch -s host --logo none | sed 's/^Host: //')"
CPU_cmd = "echo $(fastfetch -s cpu --logo none)  '('$(grep 'model name' /proc/cpuinfo | head -1 | grep -o '[0-9.]\+GHz' | sed 's/GHz/ GHz/')')'"
GPU_cmd = "echo $(fastfetch -s gpu --logo none)"
RAMtype_cmd = "echo $(sudo dmidecode -t memory | grep -i 'Type:' | grep -E 'DDR[3-6]' | awk '{print $2}' | sort -u)"

# Run commands and get outputs
Hardware = 'Hardware'
PC = '\u2022 ' + 'Product:  ' + run_command(Manuf_cmd) + '  ' + run_command(Product_cmd)
CPU = '\u2022 ' + run_command(CPU_cmd)
TC = '\u2022 ' + 'Threads: ' + str(get_number_of_threads()) + '    \u27F6    ' + 'Cores: ' +str(get_number_of_cores()) + '    \u27F6    ' + get_total_cpu_cache()
RAM = '\u2022 ' + get_ram_gb() + '   (' + run_command(RAMtype_cmd) + ')'
GPU = '\u2022 ' + run_command(GPU_cmd)
Disk = '\u2022 ' + 'Storage: ' + str(round(totalDISK, 2)) + ' GB' + '  (' + get_disk_models()[0] + ')'
Display = '\u2022 ' + get_monitor_refresh_rate_linux()

# System Info Output
htitulo = f"""{Hardware}"""
hinfo = f"""{PC}
{CPU}
{TC}
{RAM}
{GPU}
{Disk}
{Display}
"""

#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####             APP             #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

# Create and add plot into frame
def add_plot_to_frame(frame, plot_func, *args, update_interval=None, **kwargs):
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(expand=True, fill="both")
    if update_interval:
        def update():
            plot_func(ax, canvas)
            canvas.get_tk_widget().after(update_interval, update)
        update()
    else:
        plot_func(ax, *args, **kwargs)
        canvas.draw()

# Criar janela principal
root = tk.Tk()
root.title("Linux System Information")
root.geometry("1200x800")

# Configurar a grade
for i in range(3): root.grid_rowconfigure(i, weight=1)
for j in range(3): root.grid_columnconfigure(j, weight=1)

# Lista com (linha, coluna, colspan)
grid_positions = [
    (0, 0, 1),  # Texto 1
    (0, 1, 1),  # Gráfico 1
    (0, 2, 1),  # Texto 2
    (1, 0, 1),  # Texto 3
    (1, 1, 1),  # Gráfico 2
    (1, 2, 1),  # Texto 4
    (2, 0, 3),  # Gráfico 3 (ocupa 3 colunas)
]

# Criar frames
frames = []
for idx, (row, col, colspan) in enumerate(grid_positions):
    frame = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame.grid(row=row, column=col, columnspan=colspan, sticky="nsew")
    frames.append(frame)

# Add text
tk.Label(frames[0], text=stitulo       , font=("Arial", 14, "bold"), anchor="w", justify="left").pack(expand=True, fill="both")
tk.Label(frames[0], text=sinfo         , font=("Arial", 14)        , anchor="w", justify="left").pack(expand=True, fill="both")
tk.Label(frames[2], text=Storage_titulo, font=("Arial", 14, "bold"), anchor="w", justify="left").pack(expand=True, fill="both")
tk.Label(frames[2], text=Storage_info  , font=("Arial", 14)        , anchor="w", justify="left").pack(expand=True, fill="both")
tk.Label(frames[3], text=htitulo       , font=("Arial", 14, "bold"), anchor="w", justify="left").pack(expand=True, fill="both")
tk.Label(frames[3], text=hinfo         , font=("Arial", 14)        , anchor="w", justify="left").pack(expand=True, fill="both")
tk.Label(frames[5], text="RAM"         , font=("Arial", 14, "bold"), anchor="w", justify="left").pack(expand=True, fill="both")
ram_label = tk.Label(frames[5]         , font=("Arial", 14)        , anchor="w", justify="left")
ram_label.pack(expand=True, fill="both")
update_ram_label() # Start the RAM info update loop

# Add plots
add_plot_to_frame(frames[1], plot_pie_Disk)
add_plot_to_frame(frames[4], plot_ram_usage, update_interval=1000)
add_plot_to_frame(frames[6], plot_cpu_temperature, update_interval=1000)

# Iniciar interface
root.mainloop()

