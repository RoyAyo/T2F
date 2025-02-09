# not implemented or tested/ throwing errors.
import torch
import torch.nn as nn

class VAE(nn.Module):
    def __init__(self, text_dim=768, latent_dim=128, audio_dim=(64, 331)):
        super(VAE, self).__init__()
        self.latent_dim = latent_dim
        self.audio_dim = audio_dim
        
        # Encoder with batch normalization
        self.encoder = nn.Sequential(
            nn.Linear(text_dim, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU()
        )
        
        self.mu = nn.Linear(128, latent_dim)
        self.logvar = nn.Linear(128, latent_dim)
        
        # Decoder with batch normalization
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Linear(512, audio_dim[0] * audio_dim[1]),
            nn.Sigmoid()  # Changed from Tanh to Sigmoid since we normalized mel specs to [0,1]
        )

    def reparameterize(self, mu, logvar):
        # Add clipping to prevent explosion
        logvar = torch.clamp(logvar, -20, 20)
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def forward(self, text_embedding):
        encoded = self.encoder(text_embedding)
        mu, logvar = self.mu(encoded), self.logvar(encoded)
        z = self.reparameterize(mu, logvar)
        output = self.decoder(z).view(-1, *self.audio_dim)  # Reshape to [64, 331]
        return output, mu, logvar