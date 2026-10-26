import os
import sys
import time
import socket
import threading
import subprocess
import webbrowser
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

if not is_port_in_use(5000):
    import app
    server_thread = threading.Thread(
        target=lambda: app.app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    server_thread.start()
    time.sleep(1.8)

url = "http://127.0.0.1:5000"
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

launched = False

if os.path.exists(edge_exe):
    try:
        subprocess.Popen([edge_exe, f"--app={url}", "--window-size=1260,860"])
        launched = True
    except Exception:
        pass

if not launched and os.path.exists(chrome_exe):
    try:
        subprocess.Popen([chrome_exe, f"--app={url}", "--window-size=1260,860"])
        launched = True
    except Exception:
        pass

if not launched:
    webbrowser.open(url)

while True:
    time.sleep(2)
