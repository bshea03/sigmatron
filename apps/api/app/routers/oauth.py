import os
from pathlib import Path
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

router = APIRouter(prefix="/oauth", tags=["OAuth"])


def _load_env():
    # Determine the .env location: apps/api/.env (two parents up from this file)
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)


@router.post("")
def post_oauth(request: Request):
    """Redirect the client to the OAuth provider authorize endpoint.

    This loads environment variables from `apps/api/.env` and uses
    `CLIENT_ID`, `RESPONSE_TYPE`, `REDIRECT_URI`, and `SCOPE` (if present)
    to construct the authorization URL query parameters. Returns a 302
    `RedirectResponse` to the provider authorize URL.
    """
    _load_env()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    response_type = os.getenv("RESPONSE_TYPE")
    redirect_uri = os.getenv("REDIRECT_URI")
    scope = os.getenv("SCOPE")

    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth client ID not configured",
        )

    # Base provider authorize URL - change this if you want a different provider
    authorize_base = "https://github.com/login/oauth/authorize"

    params = {"client_id": client_id, client_secret: client_secret}
    if response_type:
        params["response_type"] = response_type
    if redirect_uri:
        params["redirect_uri"] = redirect_uri
    if scope:
        params["scope"] = scope

    url = f"{authorize_base}?{urlencode(params)}"
    return RedirectResponse(url=url, status_code=302)

@router.post("/callback/discord")
async def callback_discord(code: str):
    _load_env()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    if not client_id or not client_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth client credentials not configured",
        )

    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, data=data, headers=headers)

    if token_resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token exchange failed: {token_resp.text}",
        )

    token_json = token_resp.json()
    access_token = token_json.get("access_token")
    expires_in = token_json.get("expires_in")

    # Optionally fetch user info:
    user_info = None
    if access_token:
        async with httpx.AsyncClient() as client:
            user_resp = await client.get(
                "https://discord.com/api/users/@me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if user_resp.status_code == 200:
            user_info = user_resp.json()

    # Create redirect to frontend. Use an HttpOnly cookie for the session.
    # NOTE: In production set secure=True, use SameSite and sign/encrypt the cookie (JWT or server session).
    frontend_redirect = "http://localhost:3000/dashboard"
    response = RedirectResponse(url=frontend_redirect, status_code=302)
    if access_token:
        response.set_cookie(
            key="sigmatron_session",
            value=access_token,              # replace with a signed token / session id in prod
            httponly=True,
            secure=False,                    # set True in prod (HTTPS)
            samesite="lax",
            max_age=int(expires_in) if expires_in else None,
        )

    return response