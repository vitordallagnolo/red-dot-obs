import obspython as obs
import tkinter as tk
import threading

root = None
root_thread = None
thread_running = False


def create_red_dot_window():
    global root
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    canvas_width = 50
    canvas_height = 50

    x_position = screen_width - canvas_width
    y_position = 0

    root.geometry(f"{canvas_width}x{canvas_height}+{x_position}+{y_position}")

    canvas = tk.Canvas(
        root, width=canvas_width, height=canvas_height, highlightthickness=0
    )
    canvas.pack()

    canvas.create_rectangle(
        0, 0, canvas_width, canvas_height, fill="white", outline="white"
    )

    x = canvas_width // 2
    y = canvas_height // 2
    radius = 10

    canvas.create_oval(
        x - radius, y - radius, x + radius, y + radius, fill="red", outline="red"
    )


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
