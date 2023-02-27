import os

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.base_client.errors import MismatchingStateError
from fastapi import FastAPI, Request, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from .utils import random_string

APP_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UVICORN_PORT = os.getenv('UVICORN_PORT', 8000)

AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'
ACCESS_TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECTION_URL = f'http://localhost:{UVICORN_PORT}/callback'


config = Config(os.path.join(APP_BASE, 'secrets/.env'))
oath = OAuth(config)
oath.register(
    name='spotify',
    authorize_url=AUTHORIZATION_URL,
    authorize_params={
        'response_type': 'code',
    },
    access_token_url=ACCESS_TOKEN_URL,
    access_token_params={
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECTION_URL,
    },
    api_base_url='https://api.spotify.com',
    client_kwargs={
        'scope': 'user-top-read playlist-modify-public',
        'token_endpoint_auth_method':'client_secret_post',
    },
)


app = FastAPI()

# Add later, want to make sure requests are secure
# app.add_middleware(HTTPSRedirectMiddleware)

# Allow authlib to use request.session
app.add_middleware(SessionMiddleware, secret_key=random_string(10))


# Note! 
# If changing this route, need to change the route in spotify dev dashboard
@app.get('/callback/', include_in_schema=False)
async def callback(request: Request, response: Response):
    token = await oath.spotify.authorize_access_token(request)
    try:
        token = await oath.spotify.authorize_access_token(request)
    except MismatchingStateError:
        response.status_code = 475
        return {'error': 'MismatchingStateError'}
    return token


@app.get('/authorize/')
async def login(request: Request):
    """gets a token to use with /playlist/ endpoints
    to customize results based on user's spotify history
    """
    spotify = oath.create_client('spotify')
    return await spotify.authorize_redirect(request, REDIRECTION_URL)


@app.get('/link/{id}')
async def get_link(id: int):
    """For getting a playlist link based on id
    """
    pass

@app.post('/link/')
async def create_link():
    """For creating a playlist link
    """
    pass

@app.put('/link/{id}')
async def update_link(id: int):
    """For updating a playlist link
    """
    pass

@app.get('/playlist/like/')
async def playlist_like():
    """For getting a playlist based on advanced search
    """
    pass

@app.get('/playlist/text/{text}')
async def playlist_from_text(text: str, length: int = 10):
    """For getting a playlist based on a string of text
    """
    return {'text': text}


@app.get('/image/{playlist}')
async def image_from_playlist(playlist):
    """For getting an image based on a playlist
        (sharing to snapchat/instagram)
    """
    pass

@app.get('/', include_in_schema=False)
async def get_docs():
    return RedirectResponse(url='/docs')