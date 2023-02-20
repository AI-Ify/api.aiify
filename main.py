from fastapi import FastAPI
#from authlib.integrations.scarlette_client import OAuth

app = FastAPI()


@app.get('/playlist/id/{id}')
async def get_from_id(id: int):
    pass

@app.post('/playlist/id/')
async def create_link():
    pass

@app.put('/playlist/id/{id}')
async def update_link(id: int):
    pass

@app.get('/playlist/like/')
async def playlist_like():
    pass

@app.get('/playlist/text/{text}')
async def playlist_from_text(text: str, length: int = 10):
    return {'text': text}


@app.get('/image/{playlist}')
async def image_from_playlist(playlist):
    pass
