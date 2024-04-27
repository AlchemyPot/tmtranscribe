import sys
import threading
from tkinter import DISABLED, END, Button, Frame, Listbox, Scrollbar
from tkinter.ttk import Progressbar, Combobox

class ListboxRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(END, str)
        self.widget.see(END)

    def flush(self):
        pass

def create_middle_frame(root, topListBox):
    middleFrame = Frame(root)
    # middleFrame.configure(bg='green')
    middleFrame.grid_columnconfigure(0, weight=1)
    middleFrame.grid_rowconfigure(0, weight=1)
    middleFrame.grid_rowconfigure(1, weight=1)
    middleFrame.grid(row=1, column=0, columnspan=3, sticky='new', padx=10 ,pady=(10, 0))

    listBox = create_listbox(middleFrame)
    sys.stdout = ListboxRedirector(listBox)

    progressBar = create_progress_bar(middleFrame)
    modelSelector = create_model_selector(middleFrame)
    create_whisper_button(middleFrame, listBox, topListBox, progressBar, modelSelector)

def create_progress_bar(root):
    progress = Progressbar(root, orient="horizontal", length=100, mode="determinate")
    progress.grid(row=2, column=0, columnspan=3, sticky="new", pady=(0,10))
    return progress

def create_whisper_button(root, listBox, topListBox, progressBar, modelSelector):
    from whisper import whisper_transcribe

    button = Button(root, text="Transcribe")
    button.grid(row=0, column=0, sticky="new", pady=(0,0))
    def start_whisper():
        progressBar['value'] = 0
        listBox.delete(0, END)
        selected_files = topListBox.get(0, END)
        selectedModel = modelSelector.get()
        # Disable the button
        if selected_files:
            button.config(state=DISABLED)
            threading.Thread(target=whisper_transcribe, args=(button,selected_files, progressBar,selectedModel)).start()
        else:
            print("No files selected")

    button.config(command=start_whisper)
    return button

def create_model_selector(root):
    models = ['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3']
    modelSelector = Combobox(root, values=models)
    modelSelector.current(1)
    # Place the combobox in the grid
    modelSelector.grid(row=1, column=0, columnspan=3, sticky="new", pady=(0,0))
    return modelSelector


def create_listbox(root):
    frame = Frame(root)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid(sticky='nsew')

    scrollbar = Scrollbar(frame)
    scrollbar.grid(row=0, column=1, sticky='ns')

    listbox = Listbox(frame, yscrollcommand=scrollbar.set)
    listbox.grid(row=0, column=0, sticky='nsew')

    scrollbar.config(command=listbox.yview)

    frame.grid(row=2, column=0, sticky='nsew')

    return listbox