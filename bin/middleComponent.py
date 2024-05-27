import sys
import threading
from tkinter import DISABLED, END, Button, Frame, Label, Listbox, Scrollbar
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
    middleFrame.grid_columnconfigure(0, weight=1, uniform='a')
    middleFrame.grid_columnconfigure(1, weight=1, uniform="a")
    middleFrame.grid_columnconfigure(2, weight=1, uniform="a")
    middleFrame.grid_rowconfigure(0, weight=1)
    middleFrame.grid_rowconfigure(1, weight=1)
    middleFrame.grid(row=1, column=0, sticky='new', padx=10 ,pady=(10, 0))

    listBox = create_listbox(middleFrame)
    sys.stdout = ListboxRedirector(listBox)

    progressBar, progress_label = create_progress_bar(middleFrame)
    modelSelector = create_model_selector(middleFrame)
    batchSelector = create_batch_selector(middleFrame)
    computeSelector = create_compute_selector(middleFrame)
    create_whisper_button(middleFrame, listBox, topListBox, progressBar, modelSelector, progress_label, batchSelector, computeSelector)

def create_progress_bar(root):
    progress_frame = Frame(root)
    progress_frame.grid(row=5, columnspan=3, sticky="new")
    progress_frame.grid_columnconfigure(0, weight=1)

    progress = Progressbar(progress_frame, orient="horizontal", length=100, mode="determinate")
    progress.grid(row=0, column=0, sticky="ew")

    # Create a label and place it next to the progress bar
    progress_label = Label(progress_frame, text="0/0", bg='white')
    progress_label.grid(row=0, column=1, sticky="w")

    return progress, progress_label

def create_whisper_button(root, listBox, topListBox, progressBar, modelSelector, progress_label, batchSelector, computeSelector):
    from whisper import whisper_transcribe

    button = Button(root, text="Transcribe")
    button.grid(row=4, columnspan=3, sticky="new", pady=(10,0))
    def start_whisper():
        progressBar['value'] = 0
        listBox.delete(0, END)
        selected_files = topListBox.get(0, END)
        selectedModel = modelSelector.get()
        batch_size = int(batchSelector.get())
        compute_type = computeSelector.get()
        # Disable the button
        if selected_files:
            button.config(state=DISABLED)
            threading.Thread(target=whisper_transcribe, args=(button,selected_files, progressBar,selectedModel, progress_label, batch_size, compute_type)).start()
        else:
            print("No files selected")

    button.config(command=start_whisper)
    return button

def create_language_selector(root):
    
def create_model_selector(root):
    models = ['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3']

    # Create a new frame
    model_frame = Frame(root)
    model_frame.grid(row=0, column=0, sticky="new", pady=(0,0))

    # Create a label and place it in the frame
    model_label = Label(model_frame, text="Model:")
    model_label.pack(side="top")

    modelSelector = Combobox(model_frame, values=models)
    modelSelector.current(6)

    # Place the combobox in the frame, to the right of the label
    modelSelector.pack(side="top")

    return modelSelector

def create_batch_selector(root):
    batch_sizes = [0,2,4,8,16,32]

    # Create a new frame
    batch_frame = Frame(root)
    batch_frame.grid(row=0, column=1, sticky="new", pady=(0,0))

    # Create a label and place it in the frame
    batch_label = Label(batch_frame, text="Batch Size:")
    batch_label.pack(side="top")

    batchSelector = Combobox(batch_frame, values=batch_sizes)
    batchSelector.current(3)

    # Place the combobox in the frame, to the right of the label
    batchSelector.pack(side="top")

    return batchSelector

def create_compute_selector(root):
    compute_types = ['float16', 'int8']

    # Create a new frame
    compute_frame = Frame(root)
    compute_frame.grid(row=0, column=2, sticky="new", pady=(0,0))

    # Create a label and place it in the frame
    compute_label = Label(compute_frame, text="Compute Type:")
    compute_label.pack(side="top")

    computeSelector = Combobox(compute_frame, values=compute_types)
    computeSelector.current(0)

    # Place the combobox in the frame, to the right of the label
    computeSelector.pack(side="top")

    return computeSelector

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

    frame.grid(row=6, columnspan=3, sticky='nsew')

    return listbox