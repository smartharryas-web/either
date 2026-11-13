from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import auth, home

app = FastAPI()

# media 폴더는 .gitignore에 있어서 clone하면 없다. 없으면 mount에서 서버가 뜨지 않는다
Path('media').mkdir(exist_ok=True)

app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')

app.include_router(home.router)
app.include_router(auth.router)
