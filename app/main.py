import os
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.model.fart_model import FartModel

class FartBodyRequest(BaseModel):
    text: str

# Initialize the FartModel
fartModel = FartModel()

# Create FastAPI app
app = FastAPI()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# # Add rate limit exceeded handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fartifytweet.fun", "https://api.fartifytweet.fun"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["fartifytweet.fun", "api.fartifytweet.fun", "localhost"]
)

@app.get("/", status_code=200)
async def read_root(request: Request):
    return {"message": "Health Check!!!"}

# @app.post("/fart", status_code=200)
# @limiter.limit("8/minute")
# async def get_fart(request: Request, body: FartBodyRequest):
#     try:
#         audio_buffer = fartModel.generate_audio(body.text)
#         return StreamingResponse(
#             audio_buffer, 
#             media_type="audio/wav", 
#             headers={
#                 "Content-Disposition": "attachment; filename=fart.wav"
#             }
#         )
#     except Exception as e:
#         print(e)
#         return JSONResponse(
#             status_code=400,
#             content={"message": "Error Processing", "error": True},
        # )
    
@app.post("/tweet2fart", status_code=200)
@limiter.limit("8/minute")
async def get_fart(request: Request, body: FartBodyRequest):
    try:
        audio_buffer = fartModel.generate_audio_from_tweet(body.text)
        return StreamingResponse(
            audio_buffer, 
            media_type="audio/wav", 
            headers={
                "Content-Disposition": "attachment; filename=fart.wav"
            }
        )
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