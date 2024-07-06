# OBS Red Dot Recording Indicator Script

## Description

This script displays a red dot in the top right corner of your screen whenever recording starts in OBS (Open Broadcaster Software). The red dot disappears when recording stops. This is achieved using the Tkinter library to create a transparent overlay window.

## Requirements

- OBS Studio with Python scripting enabled
- Python 3.x installed on your system
- Tkinter library (usually comes with Python)

## Installation

1. **Ensure Python and Tkinter are installed:**

   - Download and install Python from [python.org](https://www.python.org/).
   - Tkinter is included with standard Python installations. If it's not installed, you can usually install it via your package manager (e.g., `apt-get install python3-tk` for Debian-based systems).

2. **Enable Python scripting in OBS:**

   - Open OBS Studio.
   - Go to `Tools` -> `Scripts`.
   - Ensure the Python scripting interface is enabled. If not, follow the prompts to install it.

3. **Download the Script:**

   - Save the script file as `status-overlay.py` or any name you prefer.

## Usage

1. **Load the Script in OBS:**

   - Open OBS Studio.
   - Go to `Tools` -> `Scripts`.
   - Click the `+` button and select the script file you saved earlier (`status-overlay.py`).
   - Ensure the script is enabled and running.

2. **Start Recording:**

   - Start recording in OBS. A red dot will appear in the top right corner of your screen.
   - Stop recording, and the red dot will disappear.

## Script Code

```python
import obspython as obs
import tkinter as tk
import threading

# Global variables
root = None
root_thread = None
thread_running = False

def create_red_dot_window():
    global root
    # Create the main window
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations (border, title bar, etc.)
    root.attributes("-topmost", True)  # Keep the window on top of all other windows
    root.attributes("-transparentcolor", "white")  # Set transparent color

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the size of the window
    canvas_width = 50
    canvas_height = 50

    # Calculate the position to place the window in the top right corner
    x_position = screen_width - canvas_width
    y_position = 0

    # Set the window position
    root.geometry(f"{canvas_width}x{canvas_height}+{x_position}+{y_position}")

    # Create a canvas widget with a transparent background
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, highlightthickness=0)
    canvas.pack()

    # Fill the background with a color that will be made transparent
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="white", outline="white")

    # Coordinates for the red dot (center of the canvas)
    x = canvas_width // 2
    y = canvas_height // 2
    radius = 10

    # Draw the red dot
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", outline="red")

def show_red_dot():
    create_red_dot_window()
    root.mainloop()

def start_recording_signal(cd):
    global root_thread, thread_running
    if not thread_running:
        thread_running = True
        root_thread = threading.Thread(target=show_red_dot)
        root_thread.start()

def stop_recording_signal(cd):
    global root, thread_running
    if root is not None:
        root.after(0, root.destroy)
        root = None
        thread_running = False

def script_description():
    return "Show a red dot in the top right corner during recording."

def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        start_recording_signal(None)
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        stop_recording_signal(None)
```


## Troubleshooting
No Red Dot Appearing: Ensure the script is properly loaded and enabled in OBS. Check the OBS script log for any errors.
Script Crashing OBS: Make sure you have the correct version of Python installed and that Tkinter is available. If the issue persists, try restarting OBS and reloading the script.
Contributing
If you have suggestions for improvements or find any bugs, feel free to open an issue or submit a pull request on the repository where this script is hosted.

## License
This script is released under the MIT License. Feel free to use, modify, and distribute it as per the terms of the license.
