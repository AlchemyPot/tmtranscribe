import sys
from tkinter import DISABLED, NORMAL, PhotoImage, Tk, Label, Toplevel, messagebox, ttk, Button, Listbox, Scrollbar, END, Frame
from tkinter import filedialog
import os
import threading
from middleComponent import create_middle_frame
from topComponent import create_top_frame

def center_window(window, width, height):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position of window's top-left corner
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def create_loading_window(root, time_consuming_tasks):
    loading_window = Toplevel(root)
    loading_window.title("loading...")
    center_window(loading_window, 500, 500)
    loading_window.resizable(False, False)
    loading_window.overrideredirect(True)  # Remove the title bar

    # Add a label with text
    text_label = Label(loading_window, text="Loading...", pady=20)
    text_label.pack()

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the absolute path to the image
    image_path = os.path.join(script_dir, '../assets/splash.png')
    print(f"Image path: {image_path}")  # Print the image path
    image = PhotoImage(file=image_path)
    image_label = Label(loading_window, image=image)
    image_label.image = image  # Keep a reference to the image to prevent it from being garbage collected
    image_label.pack()


    loading_window.update_idletasks()  # Force an update of the window

    # Run the time-consuming tasks in a separate thread
    threading.Thread(target=time_consuming_tasks, args=(root, loading_window)).start()

    loading_window.mainloop()

def create_root():
    root = Tk()
    root.title("WhisperX")
    center_window(root, 800, 600)
    root.resizable(False, False)
    root.withdraw()  # Hide the root window

    # Create the loading window
    create_loading_window(root, time_consuming_tasks)

    root.mainloop()

def time_consuming_tasks(root, loading_window):
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    topFrame, topListBox = create_top_frame(root)
    middleFrame = create_middle_frame(root, topListBox)

    root.deiconify()  # Show the root window
    loading_window.after(1000, loading_window.destroy)  # Delay the destruction of the loading window

def main():
    root = create_root()
    create_loading_window(root, time_consuming_tasks)

if __name__ == "__main__":
    main()