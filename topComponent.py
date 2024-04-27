import os
from tkinter import END, Button, Frame, Listbox, Scrollbar, filedialog, messagebox


def create_select_folder_button(root, listbox):
    def select_folder():
        listbox.delete(0, END)
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        for root_dir, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.mp3', '.wav', '.mp4', '.avi', '.mov', '.mkv', '.flac', '.ogg', '.wmv', '.mpeg')):
                    listbox.insert(END, os.path.join(root_dir, file))
                else:
                    print(f"Skipping {file} as it is not an audio/video file")

    # Create the first button in the frame
    button = Button(root, text="Select Folder", command=select_folder).grid(row=0, column=0, sticky="new", pady=(0,0))
    return button

def create_select_file_button(root,listbox):
    def select_file():
        listbox.delete(0, END)
        file_paths = filedialog.askopenfilenames(filetypes=[("Audio/Video Files", '*.mp3 *.wav *.mp4 *.avi *.mov *.mkv *.flac *.ogg *.wmv *.mpeg'), ("All Files", "*.*")])
        if file_paths:
            for file_path in file_paths:
                listbox.insert(END, file_path)
        else:
            messagebox.showerror("Error", "Please select a file with a valid extension")

    # Create the first button in the frame
    button = Button(root, text="Select Files", command=select_file).grid(row=1, column=0, sticky="new", pady=(0,10))
    return button


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

def create_top_frame(root):
    topFrame = Frame(root)
    # topFrame.configure(bg='blue')
    topFrame.grid_columnconfigure(0, weight=1)

    topFrame.grid_rowconfigure(0, weight=1)
    topFrame.grid_rowconfigure(1, weight=1)
    
    topFrame.grid(row=0, column=0, columnspan=3, sticky='new', padx=10 ,pady=(10, 0))

    listbox = create_listbox(topFrame)
    create_select_folder_button(topFrame, listbox)
    create_select_file_button(topFrame, listbox)

    return topFrame, listbox