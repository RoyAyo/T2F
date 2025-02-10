import os
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.model.fart_model import FartModel

class FartBodyRequest(BaseModel):
    text: str

fartModel = FartModel()

app = FastAPI()

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://text2fart.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000) 
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["text2fart.com", "api.text2fart.com" , "localhost"])
app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    response = await limiter(request, call_next)
    return response

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