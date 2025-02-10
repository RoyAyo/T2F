import torch
import torch.nn as nn
import torch.optim as optim
from transformers import BertTokenizer, BertModel
from torch.utils.data import DataLoader
from app.data_processing.text_to_audio import TextAudioDataset
from app.utils.helper import create_text_to_audio_map

class DiffWaveGenerator(nn.Module):
    def __init__(self, input_dim=768, audio_dim=22050):
        super(DiffWaveGenerator, self).__init__()
        self.input_dim = input_dim
        self.audio_dim = audio_dim
        
        # Text conditioning network
        self.text_proj = nn.Linear(input_dim, 256)
        
        # Initial convolution to handle concatenated input
        self.initial_conv = nn.Conv1d(257, 64, kernel_size=3, padding=1)
        
        # DiffWave layers
        self.diffusion = nn.Sequential(
            nn.ReLU(),
            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(256, 1, kernel_size=3, padding=1),
        )

    def forward(self, text_embedding, audio):
        # Project text embedding
        text_embedding = self.text_proj(text_embedding).unsqueeze(-1)  # [batch, 256, 1]
        
        # Repeat text embedding to match audio length
        text_embedding = text_embedding.repeat(1, 1, self.audio_dim)  # [batch, 256, audio_len]
        
        # Concatenate text embedding with audio
        x = torch.cat([audio.unsqueeze(1), text_embedding], dim=1)  # [batch, 257, audio_len]
        
        # Pass through initial convolution
        x = self.initial_conv(x)
        
        # Pass through DiffWave layers
        output = self.diffusion(x)
        return output.squeeze(1)

class DiffWave():
    def __init__(self):
        # Load Model
        self.model_path = "public/final_audio_generator.pth"
        self.model = DiffWaveGenerator()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.text_encoder = BertModel.from_pretrained('bert-base-uncased')

    def generate_audio(self, text, max_audio_len=22050):
        self.model.load_state_dict(torch.load(self.model_path))
        self.model.eval()
        
        # Encode text
        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', max_length=50, truncation=True)
        with torch.no_grad():
            text_embedding = self.text_encoder(**inputs).last_hidden_state.mean(dim=1)
        
        # Generate random noise as initial audio
        noise = torch.zeros(1, max_audio_len)
        
        # Generate audio
        with torch.no_grad():
            generated_audio = self.model(text_embedding, noise)
        
        return generated_audio.squeeze().numpy()
    
    def train(self, audio_dir="fart_sounds"):
        text_to_audio_map = create_text_to_audio_map(audio_dir)
        print(text_to_audio_map)

        dataset = TextAudioDataset(text_to_audio_map, audio_dir)
        dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
        self.train_model(dataloader)
    
    def train_model(self, dataloader, epochs=50, lr=0.0005, grad_accum_steps=4):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        optimizer = optim.AdamW(self.model.parameters(), lr=lr, weight_decay=1e-5)
        criterion = nn.MSELoss()
        
        self.model.train()

        for epoch in range(epochs):
            total_loss = 0
            for text_embedding, audio in dataloader:
                optimizer.zero_grad()
                output = self.model(text_embedding, audio)
                loss = criterion(output, audio)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {total_loss/len(dataloader):.6f}")
