import os
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.model.fart_model import FartModel

class FartBodyRequest(BaseModel):
    text: str

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     instrumentator.expose(app)
    
#     connect_to_mongo()
#     yield
#     close_mongo_connection()

fartModel = FartModel()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # change this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=200)
def read_root():
    return {"message": "Health Check!!!"}

@app.post("/fart", status_code=200)
def get_fart(body: FartBodyRequest):
    try:
        audio_buffer = fartModel.generate_audio(body.text)
        print("audio", audio_buffer)
        return StreamingResponse(audio_buffer, media_type="audio/wav", headers={
            "Content-Disposition": "attachment; filename=fart.wav"
        })
    except Exception as e:
        print(e)
        return {"error": "Unable to generate audio"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)