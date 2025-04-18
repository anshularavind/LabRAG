from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
import os
import requests
from urllib.parse import urlencode
from rag import get_answer_for_protocol
from constants import dois

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

@app.get("/answer")
def answer_endpoint(
    protocol: str = Query(..., description="Protocol keyword to filter by (e.g. 'elisa')"),
    query:   str = Query(..., description="Question about the protocol specified"),
    k:       int = Query(3,   description="Number of source chunks to retrieve")
):
    try:
        result = get_answer_for_protocol(protocol, query, k)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occured: " + str(e))
    
@app.get("/cite")
def citation_endpoint(fileName):
    doi = dois[fileName]
    apiUrl = f"https://citation.doi.org/format?doi={doi}";
    response = requests.get(apiUrl)
    try:
        response.raise_for_status()
        return response.text[3:]
    except:
        return "DOI not available for this protocol."
    