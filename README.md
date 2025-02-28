# wingman 🎙️
 Conversation, deconstructed. 📝🔬

## Setup
1. Fast WSL Ubuntu setup: [fastsetup](https://github.com/AnswerDotAI/fastsetup)
2. Conda env for `wingman`
```bash
git clone https://github.com/lukexyz/wingman.git
cd GameSetChat
conda create -n wingman python=3.11 pip jupyter
conda activate wingman
pip install -r requirements.txt
```
3. Update your package lists and install `ffmpeg`
```bash
sudo apt update
sudo apt install ffmpeg portaudio19-dev python-all-dev
```
4. If you also want to fix the sounddevice related warning, install its dependencies:
```bashsudo apt install libportaudio2 libasound-dev
pip install sounddevice
```
### Nbdev (optional)  
[Quickstart doc](https://nbdev.fast.ai/tutorials/tutorial.html) from nbdev.fast.ai.
```bash
nbdev_new
nbdev_install_hooks 
```
1. 🏗️ Build lib from notebooks  
```bash
nbdev_export
```
