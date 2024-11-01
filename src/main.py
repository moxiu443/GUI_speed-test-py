import tkinter as tk
from tkinter import messagebox
import speedtest
import webbrowser
import os
import threading
import time
import json

# Function to animate the "Calculating..." label
def animate_calculating():
    states = ["Calculating.", "Calculating..", "Calculating..."]
    idx = 0
    while calculating:
        calc_label.config(text=states[idx % 3])
        idx += 1
        time.sleep(0.5)  # Change dots every 0.5 seconds

# Function to run the speed test and log history
def run_speed_test():
    global calculating
    calculating = True  # Set calculating flag to True
    threading.Thread(target=animate_calculating).start()  # Start animation in a separate thread

    try:
        st = speedtest.Speedtest()
        st.download()  # Initialize server list for speedtest
        st.get_best_server()  # Select the best server
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping  # Get ping in ms

        # Update labels with speed results
        download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        ping_label.config(text=f"Ping: {ping} ms")

        # Log the speed test result to the history JSON file
        result = {
            "download_speed": download_speed,
            "upload_speed": upload_speed,
            "ping": ping
        }

        # Append to JSON file
        if os.path.exists("speed_test_results.json"):
            with open("speed_test_results.json", "r") as f:
                data = json.load(f)
        else:
            data = []
        
        data.append(result)

        with open("speed_test_results.json", "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to run speed test: {e}")
    finally:
        calculating = False  # Stop the animation
        calc_label.config(text="")  # Clear the "Calculating..." text

# Function to open GitHub link
def open_github():
    webbrowser.open("https://github.com/moxiu443")

# Function to toggle between dark mode and light mode
def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()
    save_theme()

# Function to apply the theme based on the current mode
def apply_theme():
    if dark_mode:
        app.config(bg="#2E2E2E")
        title_label.config(bg="#2E2E2E", fg="white")
        download_label.config(bg="#2E2E2E", fg="white")
        upload_label.config(bg="#2E2E2E", fg="white")
        ping_label.config(bg="#2E2E2E", fg="white")
        toggle_button.config(text="Light Mode", bg="#444444", fg="white")
        github_link.config(bg="#2E2E2E", fg="#4DA6FF")
        start_button.config(bg="#444444", fg="white")
        calc_label.config(bg="#2E2E2E", fg="white")
    else:
        app.config(bg="white")
        title_label.config(bg="white", fg="black")
        download_label.config(bg="white", fg="black")
        upload_label.config(bg="white", fg="black")
        ping_label.config(bg="white", fg="black")
        toggle_button.config(text="Dark Mode", bg="#E0E0E0", fg="black")
        github_link.config(bg="white", fg="blue")
        start_button.config(bg="#E0E0E0", fg="black")
        calc_label.config(bg="white", fg="black")

# Function to save the theme preference to a file
def save_theme():
    with open("theme_config.txt", "w") as f:
        f.write("dark" if dark_mode else "light")

# Function to load the theme preference from a file
def load_theme():
    global dark_mode
    if os.path.exists("theme_config.txt"):
        with open("theme_config.txt", "r") as f:
            theme = f.read().strip()
            dark_mode = (theme == "dark")
    else:
        dark_mode = False  # Default to light mode if config file doesn't exist
    apply_theme()

# Set up the main application window
app = tk.Tk()
app.title("Internet Speed Test")
app.geometry("600x600")
app.resizable(False, False)  # Disable resizing
dark_mode = False  # Track current mode (light mode by default)
calculating = False  # Track if calculating is in progress

# Title label
title_label = tk.Label(app, text="Internet Speed Test", font=("Arial", 18, "bold"))
title_label.pack(pady=20)

# Labels to display download, upload, and ping results
download_label = tk.Label(app, text="Download Speed: - Mbps", font=("Arial", 14))
download_label.pack(pady=5)

upload_label = tk.Label(app, text="Upload Speed: - Mbps", font=("Arial", 14))
upload_label.pack(pady=5)

ping_label = tk.Label(app, text="Ping: - ms", font=("Arial", 14))
ping_label.pack(pady=5)

# Animated "Calculating..." label
calc_label = tk.Label(app, text="", font=("Arial", 14))
calc_label.pack(pady=5)

# Button to start the speed test
start_button = tk.Button(app, text="Run Speed Test", font=("Arial", 14), command=lambda: threading.Thread(target=run_speed_test).start())
start_button.pack(pady=20)

# Credits (clickable GitHub link) in the center bottom
github_link = tk.Label(app, text="Author: Moxiu - Click here!", font=("Arial", 12, "underline"), fg="blue", cursor="hand2")
github_link.bind("<Button-1>", lambda e: open_github())
github_link.pack(pady=10)

# Toggle button for dark mode/light mode
toggle_button = tk.Button(app, text="Dark Mode", font=("Arial", 12), command=toggle_mode)
toggle_button.pack(pady=10)

# Load theme preference
load_theme()

# Run the Tkinter main loop
app.mainloop()
