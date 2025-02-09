class Model:
    def __init__(self, generator = "Concatenate"):
        self.generator = generator

    def generate(self, text):
        if self.generator == "Concatenate":
            return self.generate_audio(text)
        elif self.generator == "SimpleAudioGenerator":
            return self.generate_audio2(text)
        else:
            return "Invalid generator"
        
    def train_model(self, text):
        if self.generator == "SimpleAudioGenerator":
            pass
