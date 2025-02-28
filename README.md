# wingman 🎙️
 Conversation, deconstructed. 📝🔬

## Setup
1. Fast Ubuntu creation on WSL with: [fastsetup](https://github.com/AnswerDotAI/fastsetup)
2. Conda env:
```bash
git clone https://github.com/lukexyz/wingman.git
cd GameSetChat
conda create -n wingman python=3.11 pip jupyter
conda activate wingman
pip install -r requirements.txt
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
