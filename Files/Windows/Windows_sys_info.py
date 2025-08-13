import tkinter as tk
import wmi
import platform
import psutil
from shutil import disk_usage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import clr
import sys
import os
import time
from collections import deque
from tkinter import ttk
import matplotlib.pyplot as plt
import platform

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

# Path to LibreHardwareMonitorLib.dll
dll_path = r"C:\aaa - Luiz Henrique Leal\Backup pendrive\Statistics\Suporte\Sys_Info\LibreHardwareMonitorLib.dll"
sys.path.append(os.path.dirname(dll_path))
clr.AddReference("LibreHardwareMonitorLib")

from LibreHardwareMonitor import Hardware

class Computer:
    def __init__(self):
        self.computer = Hardware.Computer()
        self.computer.IsCpuEnabled = True
        self.computer.Open()

    def get_core_max_temp(self):
        for hardware in self.computer.Hardware:
            hardware.Update()
            if hardware.HardwareType == Hardware.HardwareType.Cpu:
                for sensor in hardware.Sensors:
                    if (
                        sensor.SensorType == Hardware.SensorType.Temperature
                        and sensor.Name == "Core Max"
                    ):
                        return sensor.Value
        return None

# CPU Temperature Widget
class TempMonitorWidget:
    def __init__(self, parent):
        self.computer = Computer()
        self.max_points = 60
        self.temp_data = deque(maxlen=self.max_points)
        self.time_data = deque(maxlen=self.max_points)
        self.time_counter = 0
        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.line, = self.ax.plot([], [], color="red", label="CPU Temp (°C)")
        self.ax.set_xlim(0, self.max_points)
        self.ax.set_title("CPU Temperature Monitor", fontweight='bold')
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.legend()
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_chart()

    def update_chart(self):
        temp = self.computer.get_core_max_temp()
        if temp is not None:
            self.temp_data.append(temp)
            self.time_data.append(self.time_counter)
            self.time_counter += 1
            self.line.set_data(self.time_data, self.temp_data)
            self.ax.set_xlim(max(0, self.time_counter - self.max_points), self.time_counter)
            self.ax.relim()
            self.ax.autoscale_view(scaley=True)
            self.canvas.draw()
        self.canvas.get_tk_widget().after(1000, self.update_chart)

#######################################
#######################################
#######################################
#######################################
#######################################
#####                             #####
#####                             #####
#####                             #####
#####        CPU Usage (%)        #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

def plot_cpu_usage(ax, canvas):
    ax.clear()
    cpu_percent = psutil.cpu_percent(interval=None)
    ax.pie([cpu_percent, 100 - cpu_percent], labels=['Used', 'Free'], autopct='%1.2f%%', startangle=90, colors=['#ff6666', '#66b3ff'], textprops={'fontsize': 12})
    ax.set_title("CPU Usage", fontweight='bold')
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
    ax.pie([used, available], labels=['Used', 'Free'], autopct='%1.2f%%', textprops={'fontsize': 12}, colors=['#ff6666', '#66b3ff'])
    ax.set_title("RAM", fontweight='bold')
    ax.axis('equal')
    canvas.draw()

# RAM informations
def update_ram_label():
    mem = psutil.virtual_memory()
    total = mem.total / (1024 ** 3)
    available = mem.available / (1024 ** 3)
    used = (mem.total - mem.available) / (1024 ** 3)
    summary = (
        f"    Used: {used:.2f} GB ({(used/total)*100:.2f}%) \n"
        f"     Free: {available:.2f} GB ({(available/total)*100:.2f}%)\n"
        f"    Total: {total:.2f} GB \n\n\n\n\n\n"
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
    total_gb = total / 1024**3
    used_gb = used / 1024**3
    free_gb = free / 1024**3
    return total_gb, used_gb, free_gb

# Storage plot
def plot_pie_Disk(ax):
    total, used, free = get_disk_usage()
    ax.pie([used, free], labels=['Used', 'Free'], autopct='%1.2f%%', textprops={'fontsize': 12}, colors=['#ff6666', '#66b3ff', '#cccccc'])
    ax.set_title("Storage", fontweight='bold')

# Storage informations
totalDISK, usedDISK, freeDISK = get_disk_usage()
storage = 'Storage'
storage_Used=f"       Used: {usedDISK:.2f} GB ({(usedDISK/totalDISK)*100:.2f}%)"
storage_Free=f"        Free:   {freeDISK:.2f} GB ({(freeDISK/totalDISK)*100:.2f}%)"
storage_Total=f"       Total: {totalDISK:.2f} GB \n\n\n\n\n"

# Storage Output
Storage_titulo = f"""{storage}"""
Storage_info = f"""{storage_Used}
{storage_Free}
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
#####          Software           #####
#####                             #####
#####                             #####
#####                             #####
#######################################
#######################################
#######################################
#######################################
#######################################

Software = 'Software (operating system)'
S_O = platform.system() + ' ' + platform.release()
VERSION = 'Version: ' + platform.version() + '\n\n\n\n\n\n'

# System Info Output
stitulo = f"""{Software}"""
sinfo = f"""{S_O}
{VERSION}
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

def get_cpu_info():
    c = wmi.WMI()
    cpu = c.Win32_Processor()[0]
    name = ' '.join(cpu.Name.strip().split()[0:3])
    threads = psutil.cpu_count(logical=True)
    max_clock_speed = cpu.MaxClockSpeed / 1000
    freq = psutil.cpu_freq()
    result = f"{name} ({threads}) @ {max_clock_speed:.2f} GHz"
    return result

def get_number_of_threads():
    return psutil.cpu_count(logical=True)

def get_number_of_cores():
    return psutil.cpu_count(logical=False)

def get_gpu_info():
    w = wmi.WMI()
    gpu_info = []
    for gpu in w.Win32_VideoController():
        name = gpu.Name.strip()
        try:
            vram = int(gpu.AdapterRAM) / (1024 ** 2)
            vram_gb = str(vram / 1024) + ' GB'
        except AttributeError:
            vram_gb = 'VRAM is not available'
        try:
            clock_speed = '@' + str(gpu.CurrentClockSpeed / 1000) + ' GHz'
        except AttributeError:
            clock_speed = ''
        gpu_type = "Dedicated" if gpu.AdapterCompatibility and gpu.AdapterCompatibility != "Intel" else "Integrated"
        gpu_description = f"{name} {clock_speed} [{gpu_type}] "
        gpu_info.append(f"{gpu_description} VRAM: {vram_gb}")
    return gpu_info

def get_monitor_refresh_rate():
    try:
        c = wmi.WMI()
        for monitor in c.Win32_VideoController():
             return monitor.MaxRefreshRate
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_system_model():
    c = wmi.WMI()
    for system in c.Win32_ComputerSystem():
        return system.Model

# Run commands and get outputs
hardware_title = 'Hardware'
PC = '\u2022 ' + 'Product:  ' + wmi.WMI().Win32_ComputerSystem()[0].Manufacturer + '    \u27F6    ' + get_system_model()
CPU = '\u2022 ' + 'CPU: ' + get_cpu_info()
TC = '\u2022 ' + 'Threads: ' + str(get_number_of_threads()) + '    \u27F6    ' + 'Cores: ' +str(get_number_of_cores())
RAM = '\u2022 ' + 'RAM: ' + str(round(psutil.virtual_memory().total / (1024 ** 3), 2)) + ' GB'
GPU = '\u2022 ' + 'GPU: ' + get_gpu_info()[0]
Disk = '\u2022 ' + 'Storage: ' + str(round(totalDISK, 2)) + ' GB'
Display = '\u2022 ' + 'Display: ' + str(get_monitor_refresh_rate()) + ' Hz'

# System Info Output
htitulo = f"""{hardware_title}"""
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
root.title("Windows System Information")
root.geometry("1200x800")

# Configurar a grade
for i in range(3): root.grid_rowconfigure(i, weight=1)
for j in range(3): root.grid_columnconfigure(j, weight=1)

# Lista com (linha, coluna, colspan)
grid_positions = [
    (0, 0, 1),  # Software
    (0, 1, 1),  # Storage plot
    (0, 2, 1),  # Storage info
    (1, 0, 1),  # Hardware
    (1, 1, 1),  # RAM plot
    (1, 2, 1),  # RAM info
    (2, 0, 2),  # CPU Temperature (spans 2 columns)
    (2, 2, 1),  # CPU Usage
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
TempMonitorWidget(frames[6])
add_plot_to_frame(frames[7], plot_cpu_usage, update_interval=1000)

# Iniciar interface
root.mainloop()

