import os
from tkinter import NORMAL, messagebox
import getpass
import torch

def is_model_downloaded(model_name):
    # Get the current user name
    user_name = getpass.getuser()
    model_directory = fr"C:\Users\{user_name}\.cache\huggingface\hub"
    model_folder = f"models--Systran--faster-whisper-{model_name}"
    model_path = os.path.join(model_directory, model_folder)
    return os.path.isdir(model_path)

def whisper_transcribe(button, audio_files=["./CartmanIpad.webm"], progressBar=None, selectedModel="base"):
    import gc
    import whisperx
    from whisperx import utils

    device = "cuda"
    batch_size = 16 # reduce if low on GPU mem
    compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
    length = len(audio_files)


    for i, audio_file in enumerate(audio_files):
        # 1. Transcribe with original whisper (batched)
        model = whisperx.load_model(selectedModel, device, compute_type=compute_type)
        print("Using whisper model: ", selectedModel)
        print(f"Transcribing {audio_file}")
        audio = whisperx.load_audio(audio_file)
        print("Transcription progress:")
        result = model.transcribe(audio, batch_size=batch_size, print_progress=True)

        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        print("Alignment progress:")
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False, print_progress=True)

        # Extract the directory from the audio_file path
        output_directory = os.path.dirname(audio_file)

        writer = utils.WriteSRT(output_directory)  # use the output_directory as the output directory for the SRT file
        result["language"] = metadata["language"]
        writer(result, audio_file, {"max_line_width": None, "max_line_count": None, "highlight_words": False})
        print("SRT file written. End")

        # Update the progress bar
        if progressBar is not None:
            progressBar['value'] = (i+1) * 100 / length
            button.master.update_idletasks()

        gc.collect()
        torch.cuda.empty_cache()
        del model

    button.config(state=NORMAL)