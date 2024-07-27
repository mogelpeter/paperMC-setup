import subprocess
import sys

# Funktion zur automatischen Installation von Paketen
def install_packages():
    required_packages = ['tkinter', 'json']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Pakete installieren
install_packages()

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import threading
import os
import io
import json

class ServerControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Control Panel")
        self.root.configure(bg='#282c34')
        self.set_icon()

        self.load_server_properties()

        self.version = self.get_minecraft_version()
        self.root.title(f"Server Control Panel - Minecraft Version {self.version}")

        self.start_button = tk.Button(root, text="Server Starten", command=self.start_server, bg='#61afef', fg='white')
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Server Stoppen", command=self.stop_server, bg='#e06c75', fg='white')
        self.stop_button.pack(pady=5)

        tk.Label(root, text="Min RAM (GB):", bg='#282c34', fg='white').pack(pady=5)
        self.min_ram_entry = tk.Entry(root, width=20, bg='#3e4451', fg='white')
        self.min_ram_entry.pack(pady=5)
        self.min_ram_entry.insert(0, self.min_ram)

        tk.Label(root, text="Max RAM (GB):", bg='#282c34', fg='white').pack(pady=5)
        self.max_ram_entry = tk.Entry(root, width=20, bg='#3e4451', fg='white')
        self.max_ram_entry.pack(pady=5)
        self.max_ram_entry.insert(0, self.max_ram)

        self.command_entry = tk.Entry(root, width=100, bg='#3e4451', fg='white')
        self.command_entry.pack(pady=5)
        
        self.send_command_button = tk.Button(root, text="Befehl Senden", command=self.send_command, bg='#98c379', fg='black')
        self.send_command_button.pack(pady=5)

        self.log_text = scrolledtext.ScrolledText(root, width=100, height=20, bg='#21252b', fg='white')
        self.log_text.pack(pady=5)

        self.process = None

    def set_icon(self):
        self.root.iconbitmap('icon.ico')

    def load_server_properties(self):
        self.min_ram = "1"
        self.max_ram = "2"
        if os.path.exists("server.properties"):
            with open("server.properties", "r") as f:
                for line in f:
                    if line.startswith("min_ram_gb="):
                        self.min_ram = line.strip().split("=")[1]
                    elif line.startswith("max_ram_gb="):
                        self.max_ram = line.strip().split("=")[1]

    def get_minecraft_version(self):
        if os.path.exists("version_history.json"):
            with open("version_history.json", "r") as f:
                data = json.load(f)
                return data.get("currentVersion", "Unbekannt")
        return "Unbekannt"

    def create_start_script(self):
        min_ram = self.min_ram_entry.get() + "G"
        max_ram = self.max_ram_entry.get() + "G"
        java_path = r"C:\Program Files\Amazon Corretto\jdk21.0.4_7\bin\java.exe"

        start_script = f"""
@echo off
"{java_path}" -Xms{min_ram} -Xmx{max_ram} -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -server -Dfile.encoding=UTF-8 -jar paper.jar nogui
pause
"""
        return start_script

    def start_server(self):
        if self.process is None:
            start_script = self.create_start_script()
            script_file = "start_temp.bat"
            with open(script_file, "w") as f:
                f.write(start_script)
            self.process = subprocess.Popen(['cmd.exe', '/c', script_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.log_text.insert(tk.END, "Server gestartet...\n", 'info')
            threading.Thread(target=self.read_output, args=(self.process.stdout,)).start()
            threading.Thread(target=self.read_output, args=(self.process.stderr,)).start()
        else:
            messagebox.showwarning("Warnung", "Server läuft bereits!")

    def stop_server(self):
        if self.process:
            self.process.kill()
            self.process.wait()
            self.process = None
            self.log_text.insert(tk.END, "Server gestoppt...\n", 'info')
        else:
            messagebox.showwarning("Warnung", "Server läuft nicht!")

    def send_command(self):
        command = self.command_entry.get()
        if self.process and self.process.stdin:
            self.process.stdin.write((command + '\n').encode('utf-8'))
            self.process.stdin.flush()
            self.log_text.insert(tk.END, f"Befehl gesendet: {command}\n", 'command')
        else:
            messagebox.showwarning("Warnung", "Server läuft nicht!")

    def read_output(self, pipe):
        with io.TextIOWrapper(pipe, encoding='utf-8', errors='replace') as f:
            for line in f:
                if "debug" in line.lower():
                    tag = 'debug'
                elif "error" in line.lower():
                    tag = 'error'
                elif "warn" in line.lower():
                    tag = 'warn'
                else:
                    tag = 'output'
                self.log_text.insert(tk.END, line, tag)
                self.log_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerControlApp(root)

    # Set up tag styles for log text
    app.log_text.tag_configure('info', foreground='#61afef', font=('TkDefaultFont', 10, 'bold'))
    app.log_text.tag_configure('command', foreground='#98c379', font=('TkDefaultFont', 10, 'bold'))
    app.log_text.tag_configure('output', foreground='#abb2bf', font=('TkDefaultFont', 10, 'bold'))
    app.log_text.tag_configure('warn', foreground='#e5c07b', font=('TkDefaultFont', 10, 'bold'))
    app.log_text.tag_configure('error', foreground='#e06c75', font=('TkDefaultFont', 10, 'bold'))
    app.log_text.tag_configure('debug', foreground='#c678dd', font=('TkDefaultFont', 10, 'bold'))

    root.mainloop()
