import torch
import torch.nn as nn
import torch.optim as optim
import soundfile as sf
from transformers import BertTokenizer, BertModel
from app.data_processing.text_to_audio import TextAudioDataset
import soundfile as sf
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertModel

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
    
    def train(self, audio_dir="fart_sounds"):
        audio_dir = "fart_sound_mono"
        dataset = TextAudioDataset(audio_dir)
        dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
        model = SimpleAudioGenerator()
        self.train_model(self.model, dataloader)
    
    def train_model(self, model, dataloader, epochs=50, lr=0.0005, grad_accum_steps=4):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-5)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.6)
        criterion = nn.MSELoss()
        
        for epoch in range(epochs):
            model.train()
            total_loss = 0
            optimizer.zero_grad()
            
            for i, (text_embedding, audio) in enumerate(dataloader):
                text_embedding, audio = text_embedding.to(device), audio.to(device)
                output = model(text_embedding)
                loss = criterion(output, audio)
                loss.backward()
                
                if (i + 1) % grad_accum_steps == 0:
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
                    optimizer.zero_grad()
                
                total_loss += loss.item()
            
            scheduler.step()
            avg_loss = total_loss / len(dataloader)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.6f}")
            
            if (epoch + 1) % 5 == 0:
                torch.save(model.state_dict(), f"fart_epoch/audio_generator_epoch_{epoch + 1}.pth")
        
        torch.save(model.state_dict(), "public/final_audio_generator.pth")