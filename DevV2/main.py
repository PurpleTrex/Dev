import subprocess
import os
import time
import threading
import webbrowser
import socket

def get_local_ip():
    """Get the local IP address of this machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def start_streamlit():
    # Get the path to the app.py file
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    
    # Start the Streamlit server with network parameters
    process = subprocess.Popen(
        ["streamlit", "run", app_path, "--server.address=0.0.0.0", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    return process

def open_browser():
    # Wait a moment for the server to start
    time.sleep(3)
    # Open the browser
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Starting DevTalk application...")
    print(f"To access from other devices on your network, use: http://{local_ip}:8501")
    
    # Start Streamlit in a separate process
    streamlit_process = start_streamlit()
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        if streamlit_process:
            streamlit_process.terminate()
