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
import ctypes, struct

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

def get_max_clock_from_smbios():
    RSMB = 0x52534D42  # 'RSMB' in little-endian
    k32 = ctypes.windll.kernel32
    k32.GetSystemFirmwareTable.restype = ctypes.c_uint32
    size = k32.GetSystemFirmwareTable(RSMB, 0, None, 0)
    if size == 0:
        raise OSError("GetSystemFirmwareTable returned size 0 (SMBIOS unavailable).")
    buf = ctypes.create_string_buffer(size)
    ret = k32.GetSystemFirmwareTable(RSMB, 0, buf, size)
    if ret != size:
        raise OSError(f"GetSystemFirmwareTable returned {ret}, expected {size}.")
    data = buf.raw
    if len(data) < 8:
        raise ValueError("RawSMBIOSData header too small.")
    total_len = struct.unpack_from("<I", data, 4)[0]
    table = data[8:8+total_len]
    off = 0
    max_mhz_values = []
    cur_mhz_values = []
    while off + 4 <= len(table):
        typ = table[off]
        slen = table[off+1]
        if slen < 4:
            break
        if typ == 127:
            break
        nxt = off + slen
        while nxt + 1 < len(table) and not (table[nxt] == 0 and table[nxt+1] == 0):
            nxt += 1
        nxt += 2  # skip the double NUL terminator
        if typ == 4 and slen >= 24:
            # SMBIOS Type 4 (v2.6+): Max Speed at offset 20 (WORD), Current Speed at offset 22 (WORD)
            max_mhz = struct.unpack_from("<H", table, off + 20)[0]
            cur_mhz = struct.unpack_from("<H", table, off + 22)[0]
            if max_mhz not in (0, 0xFFFF):
                max_mhz_values.append(max_mhz)
            if cur_mhz not in (0, 0xFFFF):
                cur_mhz_values.append(cur_mhz)
        off = nxt
    if not max_mhz_values:
        raise RuntimeError("No SMBIOS Type 4 Max Speed found.")
    mhz = max(max_mhz_values)
    return mhz, cur_mhz_values

mhz, cur_list = get_max_clock_from_smbios()

def get_cpu_info():
    c = wmi.WMI()
    cpu = c.Win32_Processor()[0]
    name = ' '.join(cpu.Name.strip().split()[0:3])
    threads = psutil.cpu_count(logical=True)
    max_clock_speed = cpu.MaxClockSpeed / 1000
    freq = psutil.cpu_freq()
    result = f"{name} ({threads}) @ {mhz/1024:.2f} GHz ({max_clock_speed:.2f} GHz)"
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

def get_cache():
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        CACHE = cpu.L3CacheSize / 1024
    return CACHE

def get_storage_brand():
    c = wmi.WMI()
    for disk in c.Win32_DiskDrive():
        return disk.Model

# ----------------------------------- Type of RAM ----------------------------------- #
# Map of SMBIOS
SMBIOS_MEM_TYPE = {
    0x01: "Other",
    0x02: "Unknown",
    0x03: "DRAM",
    0x04: "EDRAM",
    0x05: "VRAM",
    0x06: "SRAM",
    0x07: "RAM",
    0x08: "ROM",
    0x09: "FLASH",
    0x0A: "EEPROM",
    0x0B: "FEPROM",
    0x0C: "EPROM",
    0x0D: "CDRAM",
    0x0E: "3DRAM",
    0x0F: "SDRAM",
    0x10: "SGRAM",
    0x11: "RDRAM",
    0x12: "DDR",
    0x13: "DDR2",
    0x14: "DDR2 FB-DIMM",
    0x18: "DDR3",
    0x19: "FBD2",
    0x1A: "DDR4",
    0x1B: "LPDDR",
    0x1C: "LPDDR2",
    0x1D: "LPDDR3",
    0x1E: "LPDDR4",
    0x1F: "Logical non-volatile device",
    0x20: "HBM",
    0x21: "HBM2",
    0x22: "DDR5",
    0x23: "LPDDR5",
    0x24: "HBM3",
}

def _get_rsmb_blob():
    """Return raw SMBIOS bytes using GetSystemFirmwareTable('RSMB')."""
    RSMB = 0x52534D42  # 'RSMB'
    k32 = ctypes.windll.kernel32
    k32.GetSystemFirmwareTable.restype = ctypes.c_uint32
    needed = k32.GetSystemFirmwareTable(RSMB, 0, None, 0)
    if needed == 0:
        raise OSError("Raw SMBIOS not available (GetSystemFirmwareTable size=0).")
    buf = ctypes.create_string_buffer(needed)
    ret = k32.GetSystemFirmwareTable(RSMB, 0, buf, needed)
    if ret != needed:
        raise OSError("GetSystemFirmwareTable returned unexpected size.")
    data = buf.raw
    if len(data) < 8:
        raise ValueError("RawSMBIOSData header too small.")
    total_len = struct.unpack_from("<I", data, 4)[0]
    return data[8:8 + total_len]  # SMBIOS table bytes

def _iter_smbios_structs(table_bytes):
    """Yield (stype, slen, start_off, next_off) for each SMBIOS structure."""
    off = 0
    n = len(table_bytes)
    while off + 4 <= n:
        stype = table_bytes[off]
        slen = table_bytes[off + 1]
        if slen < 4:  # malformed
            break
        # Find end of string-set (double NUL) after formatted area
        nxt = off + slen
        while nxt + 1 < n and not (table_bytes[nxt] == 0 and table_bytes[nxt + 1] == 0):
            nxt += 1
        nxt += 2
        yield stype, slen, off, nxt
        if stype == 127:  # End-of-table
            break
        off = nxt

def get_ram_types_via_smbios():
    tbl = _get_rsmb_blob()
    results = []
    for stype, slen, off, nxt in _iter_smbios_structs(tbl):
        if stype == 17:  # Memory Device
            # "Memory Type" is a BYTE at offset 0x12 from the start of this structure (Type 17)
            if slen > 0x12:
                mem_type_code = tbl[off + 0x12]
                mem_type = SMBIOS_MEM_TYPE.get(mem_type_code, f"Unknown (0x{mem_type_code:02X})")

                # Optional: read Speed (WORD at 0x15) if present (SMBIOS 2.3+)
                speed_mts = None
                if slen > 0x16:
                    speed_mts = struct.unpack_from("<H", tbl, off + 0x15)[0]
                    if speed_mts == 0 or speed_mts == 0xFFFF:
                        speed_mts = None

                results.append((mem_type, speed_mts))
    return results

# ----------------------------------- Type of RAM ----------------------------------- #
sticks = get_ram_types_via_smbios()
for i, (mem_type, speed) in enumerate(sticks):
  TIPO = mem_type

# Run commands and get outputs
hardware_title = 'Hardware'
PC = '\u2022 ' + 'Product:  ' + wmi.WMI().Win32_ComputerSystem()[0].Manufacturer + ' ' + get_system_model()
CPU = '\u2022 ' + 'CPU: ' + get_cpu_info()
TC = '\u2022 ' + 'Threads: ' + str(get_number_of_threads()) + '    \u27F6    ' + 'Cores: ' + str(get_number_of_cores())  + '    \u27F6    ' + 'Cache: ' + str(get_cache()) + ' MB'
RAM = '\u2022 ' + 'RAM: ' + str(round(psutil.virtual_memory().total / (1024 ** 3), 2)) + ' GB' + ' (' + TIPO + ')'
GPU = '\u2022 ' + 'GPU: ' + get_gpu_info()[0]
Disk = '\u2022 ' + 'Storage: ' + str(round(totalDISK, 2)) + ' GB' + ' (' + get_storage_brand() + ')'
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

