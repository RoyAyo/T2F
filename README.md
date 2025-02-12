# FartifyTweetAI

FartifyTweetAI is an AI-powered tweet analyzer that **breaks down, analyzes, and "sentisizes" tweets** to detect emotions and structures. It then maps them to a variety of **preprocessed and trained farts**, creating a unique, humorous, and absurd auditory representation of tweets.

---

## 🚀 Features
- **AI-powered Tweet Analysis**: Breaks down the structure and sentiment of tweets.
- **Emotion Mapping**: Detects emotions and maps them to different fart sounds.
- **Pretrained Fart Models**: Uses a dataset of diverse fart sounds mapped to emotional tones.
- **FastAPI-based API**: Lightweight and efficient backend for processing requests.
- **Rate Limiting**: Prevents spam with built-in request limiting.

---

## 🛠️ Installation

### **1️⃣ Clone the Repository**
```sh
 git clone https://github.com/yourusername/FartifyTweetAI.git
 cd FartifyTweetAI
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## ⚡ Usage

### **Start the FastAPI Server**
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Available Endpoints**
#### **1️⃣ Health Check**
```sh
GET /
```
_Response:_ `{ "message": "Health Check!!!" }`

#### **2️⃣ Convert Tweet to Fart**
```sh
POST /tweet2fart
```
**Request Body:**
```json
{
    "text": "Your tweet here"
}
```
_Response:_ A fart sound file (`fart.wav`) generated from the tweet.

---

## 🌍 Deployment
### **Run with Docker**
_Incoming_
```sh
docker build -t fartifytweetai .
docker run -p 8000:8000 fartifytweetai
```

### **Deploy on a Server (Gunicorn + Uvicorn)**
```sh
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

---

## 🎉 Contributing
Want to contribute? Feel free to submit a PR or open an issue!

---

## 📜 License
This project is licensed under the MIT License.

---

🚀 **FartifyTweetAI: Because most tweets are just farts in disguise.**

