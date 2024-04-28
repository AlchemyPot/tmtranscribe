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
- If the model is not present in your .cache folder it will first be downloaded. This is done automatically by whisperx and will make your first run slower

# Recommended parameters (WIP)

You can find a model comparison here: https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages

- model: large-v3 (admitedly lower error rate than v2). In you are low in memory or require faster processing only then you might trade off accuracy for performance by downgrading to medium down to tiny.

# To do

- Add a checkbox that allows you to skip files that already have a subtitle file associated with them
