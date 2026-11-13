from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine
from models import User, UserSession


templates = Jinja2Templates(directory='templates')
password_hash = PasswordHash.recommended()

def get_db():
  with Session(engine) as db:
    yield db

SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user(request: Request, db: SessionDep):
  session_id = request.cookies.get('session_id')

  # 쿠키가 없으면 로그인 안 한 사람
  if session_id is None:
    return None

  user_session = db.get(UserSession, session_id)

  # 쿠키는 있지만 세션 표에 없으면(로그아웃한 세션) 로그인 안 한 사람
  if user_session is None:
    return None

  return user_session.user

CurrentUserDep = Annotated[User | None, Depends(get_current_user)]


# 없는 글이면 404를 내는 의존성은 팀 표를 만든 뒤 이 아래에.
# insta의 PostDep 모양:
#
# def get_post_or_404(post_id: int, db: SessionDep):
#   post = db.get(Post, post_id)
#   if post is None:
#     raise HTTPException(status_code=404, detail='해당 게시물이 없습니다.')
#   return post
#
# PostDep = Annotated[Post, Depends(get_post_or_404)]
