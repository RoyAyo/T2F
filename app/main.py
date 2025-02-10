import os
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.model.fart_model import FartModel

class FartBodyRequest(BaseModel):
    text: str

fartModel = FartModel()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://text2fart.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
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
        return JSONResponse(
            status_code=400,
            content={"message": "Error Processing", "error": True},
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)