import torch
import torch.nn as nn
import librosa
import soundfile as sf
from transformers import BertTokenizer, BertModel
from app.model.audiowave import SimpleAudioGenerator

# Load Tokenizer & Encoder
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
text_encoder = BertModel.from_pretrained('bert-base-uncased')

class SimpleAudioGenerator(nn.Module):
    def __init__(self, text_dim=768, hidden_dim=512, audio_len=22050):
        super().__init__()
        self.text_encoder = nn.Sequential(
            nn.Linear(text_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, hidden_dim * 4),
            nn.ReLU(),
            nn.Linear(hidden_dim * 4, audio_len),
            nn.Tanh()
        )
    
    def forward(self, text_embedding):
        hidden = self.text_encoder(text_embedding)
        audio = self.decoder(hidden)
        return audio


class AudioWave():
    def __init__(self):
        # Load Model
        model_path = "public/final_audio_generator.pth"
        self.model = SimpleAudioGenerator()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def generate_audio(self, text, output_file="new.wav", sr=22050, max_audio_len=22050):
        inputs = tokenizer(text, return_tensors='pt', padding='max_length', max_length=50, truncation=True)
        with torch.no_grad():
            text_embedding = text_encoder(**inputs).last_hidden_state.mean(dim=1)  # [1, 768]
        
        with torch.no_grad():
            generated_audio = self.model(text_embedding).squeeze(0).numpy()
        
        sf.write(output_file, generated_audio, samplerate=sr)
        print(f"Audio saved to {output_file}")

        return output_file