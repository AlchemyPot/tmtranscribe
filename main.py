import sys
from tkinter import DISABLED, NORMAL, Tk, Label, messagebox, ttk, Button, Listbox, Scrollbar, END, Frame
from tkinter import filedialog
import os
import threading
from middleComponent import create_middle_frame
from topComponent import create_top_frame


def create_root():
    root = Tk()
    root.title("WhisperX")
    root.geometry("800x600")
    root.resizable(False, False)
    # root.configure(bg='yellow')
    return root

def main():
    root = create_root()
    # Redirect stdout to the Text widget
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    topFrame, topListBox = create_top_frame(root)
    middleFrame = create_middle_frame(root, topListBox)

    root.mainloop()

if __name__ == "__main__":
    main()