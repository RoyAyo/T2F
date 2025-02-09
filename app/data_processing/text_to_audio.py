import os
import torch
import numpy as np
import librosa
from torch.utils.data import Dataset
from transformers import BertTokenizer, BertModel

class TextAudioDataset(Dataset):
    def __init__(self, audio_dir, sr=22050, max_audio_len=22050):
        self.audio_dir = audio_dir
        self.sr = sr
        self.max_audio_len = max_audio_len
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.text_encoder = BertModel.from_pretrained('bert-base-uncased')
        self.text_to_audio_map = self.create_text_to_audio_map()
    
    def create_text_to_audio_map(self):
        text_to_audio_map = []
        for file in os.listdir(self.audio_dir):
            if file.endswith(".wav"):
                text = file.split(".")[0].split("_")[1]
                text_to_audio_map.append((text, file))
        return text_to_audio_map

    def __len__(self):
        return len(self.text_to_audio_map)

    def __getitem__(self, idx):
        text, audio_file = self.text_to_audio_map[idx]
        audio_path = os.path.join(self.audio_dir, audio_file)
        
        # Load and preprocess audio
        audio, _ = librosa.load(audio_path, sr=self.sr)
        audio = np.pad(audio, (0, max(0, self.max_audio_len - len(audio))), mode='constant')[:self.max_audio_len]
        
        # Convert text to embedding
        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', max_length=50, truncation=True)
        with torch.no_grad():
            text_embedding = self.text_encoder(**inputs).last_hidden_state.mean(dim=1)
        
        return text_embedding.squeeze(0), torch.tensor(audio, dtype=torch.float32)