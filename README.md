
https://www.reddit.com/r/singularity/comments/1gyu5ud/help_fastest_reliable_embedding_model_for_300gb/lyv1jic/

https://huggingface.co/dunzhang/stella_en_400M_v5


# env

```pwsh
conda create -n hf python=3.10 -y
conda activate hf
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
pip install transformers
pip install numpy scipy scikit-learn
pip install sentence-transformers
pip3 install -U xformers --index-url https://download.pytorch.org/whl/cu124
```