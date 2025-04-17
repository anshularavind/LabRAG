from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
import os
import requests
from urllib.parse import urlencode


app = FastAPI()

app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://localhost:3000"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

PROTOCOLS_IO_CLIENT_ID = os.getenv("PROTOCOLS_IO_CLIENT_ID")
PROTOCOLS_IO_CLIENT_SECRET = os.getenv("PROTOCOLS_IO_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")
AUTH_URL = "https://www.protocols.io/api/v3/oauth/authorize"
TOKEN_URL = "https://www.protocols.io/api/v3/oauth/token"


@app.get("/", response_class=HTMLResponse)
async def root():
    params = {
        "client_id": PROTOCOLS_IO_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    return f'<a href="{url}">Login with Protocols.io</a>'

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code provided"}

    data = {
        "client_id": PROTOCOLS_IO_CLIENT_ID,
        "client_secret": PROTOCOLS_IO_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, data=data)
    if response.status_code != 200:
        return {"error": "Token exchange failed", "details": response.text}

    token_data = response.json()
    return {
        "access_token": token_data["access_token"],
        "full_response": token_data
    }