import tkinter as tk
import threading
import gc
import time
import win32api
import keyboard  # Import the keyboard library

# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to close the application
def close_app():
    print("Closing the application with F10")
    root.quit()
    root.destroy()

# Function to draw a small dot at the center
def draw_dot_crosshair():
    crosshair_size = 11
    gap_size = 4
    canvas.delete("all")
    gc.collect()
    # Top line
    canvas.create_line(canvas_size // 2, (canvas_size // 2) - crosshair_size // 2, canvas_size // 2, (canvas_size // 2) - gap_size // 2, fill="red", width=2)
    # Bottom line
    canvas.create_line(canvas_size // 2, (canvas_size // 2) + gap_size // 2, canvas_size // 2, (canvas_size // 2) + crosshair_size // 2, fill="red", width=2)
    # Left line
    canvas.create_line((canvas_size // 2) - crosshair_size // 2, canvas_size // 2, (canvas_size // 2) - gap_size // 2, canvas_size // 2, fill="red", width=2)
    # Right line
    canvas.create_line((canvas_size // 2) + gap_size // 2, canvas_size // 2, (canvas_size // 2) + crosshair_size // 2, canvas_size // 2, fill="red", width=2)
    

# Function to draw a circle at the center with a specified radius
def draw_circle_crosshair(radius=20):
    canvas.delete("all")
    crosshair_size = 33
    gap_size = 5
    canvas.delete("all")
    gc.collect()
    # Top line
    canvas.create_line(canvas_size // 2, (canvas_size // 2) - crosshair_size // 2, canvas_size // 2, (canvas_size // 2) - gap_size // 2, fill="red", width=2)
    # Bottom line
    canvas.create_line(canvas_size // 2, (canvas_size // 2) + gap_size // 2, canvas_size // 2, (canvas_size // 2) + crosshair_size // 2, fill="red", width=2)
    # Left line
    canvas.create_line((canvas_size // 2) - crosshair_size // 2, canvas_size // 2, (canvas_size // 2) - gap_size // 2, canvas_size // 2, fill="red", width=2)
    # Right line
    canvas.create_line((canvas_size // 2) + gap_size // 2, canvas_size // 2, (canvas_size // 2) + crosshair_size // 2, canvas_size // 2, fill="red", width=2)
    

# Function to switch between crosshairs
def switch_crosshair(mode):
    if mode == 1:
        draw_dot_crosshair()
        #print("Switched to dot crosshair")
    elif mode == 2:
        draw_circle_crosshair()
        #print("Switched to circle crosshair")

# Create the main application window
root = tk.Tk()
root.title("Crosshair")
root.overrideredirect(True)
root.attributes('-topmost', True)
root.wm_attributes('-transparentcolor', 'black')

canvas_size = 2000
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='black', highlightthickness=0)
canvas.pack()

# Initialize with dot crosshair
draw_dot_crosshair()
center_window(root, canvas_size, canvas_size)

# Track current mode to prevent unnecessary redraws
current_mode = 1

# Function to monitor key presses and mouse events
def monitor_keys():
    global current_mode
    current_radius = 20  # Default circle radius
    small_radius = 10     # Smaller circle radius

    

    while True:
        buttons = ['3', '5', 'v', 'g', 'r', 't', 'q', 'f']
        if (any(keyboard.is_pressed(key) for key in buttons) and current_mode != 1):
            current_mode = 1
            switch_crosshair(current_mode)
        elif keyboard.is_pressed('4') and current_mode != 2:
            current_mode = 2
            switch_crosshair(current_mode)
        elif keyboard.is_pressed('F10'):
            close_app()
            break

        elif win32api.GetAsyncKeyState(0x02) < 0 and current_mode == 2:  # Right mouse button pressed
            draw_circle_crosshair(small_radius)
        elif win32api.GetAsyncKeyState(0x02) >= 0 and current_mode == 2:  # Right mouse button released
            draw_circle_crosshair(current_radius)

        time.sleep(0.05)  # Shorter delay for more responsive key detection

# Start the key monitoring in a separate thread
key_monitor_thread = threading.Thread(target=monitor_keys, daemon=True)
key_monitor_thread.start()

# Start the Tkinter event loop
root.mainloop()
