import os
import sys
import time
import threading
import webbrowser
from pathlib import Path

# Absolute directory paths
ROOT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = ROOT_DIR / "tn_transport_ai"

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import app

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("=" * 70)
    print("  TAMIL NADU SMART TRANSPORT AI - ADVANCED TRANSIT PLATFORM")
    print("=" * 70)
    print("  Laptop / Desktop:    http://127.0.0.1:5000")
    print("  Mobile Phone (WiFi): http://192.168.1.14:5000")
    print("  Opening browser automatically in 1 second...")
    print("  Press CTRL+C in this window to stop the server")
    print("=" * 70)
    
    # Auto-open default browser
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
