import os
from tkinter import NORMAL, messagebox
import getpass
import torch
import winsound
import gc
import whisperx
from whisperx import utils


def is_model_downloaded(model_name):
    # Get the current user name
    user_name = getpass.getuser()
    model_directory = fr"C:\Users\{user_name}\.cache\huggingface\hub"
    model_folder = f"models--Systran--faster-whisper-{model_name}"
    model_path = os.path.join(model_directory, model_folder)
    return os.path.isdir(model_path)

def load_and_transcribe_model(audio_file, selectedModel, device, batch_size, compute_type):
    model = whisperx.load_model(selectedModel, device, compute_type=compute_type, language="en")
    print(f"Using whisper model: {selectedModel}, Device: {device}, Compute Type: {compute_type}, Batch Size: {batch_size}")
    print(f"Transcribing {audio_file}")
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size, print_progress=True)
    return result, audio, model

def align_output(result, device, audio):
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    print("Alignment progress:")
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False, print_progress=True)
    return result, metadata

def write_srt_file(result, metadata, audio_file):
    output_directory = os.path.dirname(audio_file)
    writer = utils.WriteSRT(output_directory)
    result["language"] = metadata["language"]
    writer(result, audio_file, {"max_line_width": None, "max_line_count": None, "highlight_words": False})
    print("SRT file written. End")

def update_progress(progressBar, progress_label, i, length):
    if progressBar is not None:
        progressBar['value'] = (i+1) * 100 / length
        progressBar.master.update_idletasks()
    if progress_label is not None:
        progress_label["text"] = f"{i+1}/{length}"

def check_input(audio_files, batch_size, compute_type, selectedModel):
    if batch_size is None:
        messagebox.showerror("Error", "Batch size not selected")
        return False
    if compute_type is None:
        messagebox.showerror("Error", "Compute type not selected")
        return False
    if audio_files is None:
        messagebox.showerror("Error", "No files selected")
        return False
    if selectedModel is None:
        messagebox.showerror("Error", "Model not selected")
        return False
    if not is_model_downloaded(selectedModel):
        messagebox.showerror("Error", "Model not downloaded")
        return False
    return True

def whisper_transcribe(button, audio_files=None, progressBar=None, selectedModel=None, progress_label=None, batch_size=None, compute_type=None):
    device = "cuda"
    length = len(audio_files)

    if not check_input(audio_files, batch_size, compute_type, selectedModel):
        button.config(state=NORMAL)
        return
    # Initialize the progress bar
    update_progress(progressBar, progress_label, -1, length)

    for i, audio_file in enumerate(audio_files):
        try:
            result, audio, model = load_and_transcribe_model(audio_file, selectedModel, device, batch_size, compute_type)
            result, metadata = align_output(result, device, audio)
            write_srt_file(result, metadata, audio_file)
            update_progress(progressBar, progress_label, i, length)
            gc.collect()
            torch.cuda.empty_cache()
            del model
        except torch.cuda.CudaError as e:
            messagebox.showerror("CUDA Error", str(e))
            button.config(state=NORMAL)
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            button.config(state=NORMAL)
            return

    button.config(state=NORMAL)
    winsound.Beep(440, 500)