# How to start?

- Create a venv using conda with python v3.10: `conda create --name whisperx python=3.10`
- Activate the venv `conda activate whisperx`
- Install the following:
  - `conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia` [other methods](https://pytorch.org/get-started/previous-versions/#v200)
  - `pip install git+https://github.com/m-bain/whisperx.git`
- Run the app using `python main.py`.

# How to use?

The GUI is self explanatory:

- Select a folder or a number of files
- Select your model (tiny,base,small,medium,large,large-v2,large-v3)
- Click on transcribe to generate the `.srt` next to each file
- If the model is not present in your .cache folder it will first be downloaded. This is done automatically by Whisperx and will make your first run slower

# Recommended parameters (WIP)

You can find a model comparison here: https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages

- model: large-v3 (admittedly has a lower error rate than v2). If you are low in memory or require faster processing only then you might want to trade off accuracy for performance by downgrading to medium down to tiny. Other than that, I recommend sticking with large-v3
- batch size: Choose a higher batch size to improve performance when you have a powerful GPU. Lower the batch size if you run into CUDA memory issues
- compute type: float16 is the recommended value. Downgrade to int8 to if you are getting CUDA memory issues at the cost of decreasing the accuracy
