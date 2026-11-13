from fastapi import Request, Form, APIRouter
from fastapi.responses import RedirectResponse
from sqlalchemy import select
import secrets

from deps import templates, password_hash, CurrentUserDep, SessionDep
from models import User, UserSession

router = APIRouter()


@router.get('/signup')
def signup_form(
  request: Request,
  user: CurrentUserDep
):
  return templates.TemplateResponse(
    request=request,
    name='signup.html',
    context={'user': user}
  )


@router.post('/signup')
def signup(
  request: Request,
  db: SessionDep,
  username: str = Form(),
  password: str = Form()
):
  # 이미 쓰는 아이디인지 확인
  exists = db.scalar(select(User).where(User.username == username))

  if exists:
    return templates.TemplateResponse(
      request=request,
      name='signup.html',
      context={'error': '이미 있는 아이디입니다.'}
    )

  # 비밀번호는 해시로 바꿔서 저장
  hashed_pw = password_hash.hash(password)

  user = User(username=username, password_hash=hashed_pw)
  db.add(user)
  db.commit()

  return RedirectResponse('/login', status_code=303)


@router.get('/login')
def login_form(
  request: Request,
  user: CurrentUserDep
):
  return templates.TemplateResponse(
    request=request,
    name='login.html',
    context={'user': user}
  )


@router.post('/login')
def login(
  request: Request,
  db: SessionDep,
  username: str = Form(),
  password: str = Form()
):
  user = db.scalar(select(User).where(User.username == username))

  # 아이디가 없거나 비밀번호가 다르면 같은 에러 (어느 쪽이 틀렸는지 알려 주지 않는다)
  if (user is None) or not (password_hash.verify(password, user.password_hash)):
    return templates.TemplateResponse(
      request=request,
      name='login.html',
      context={'error': '아이디가 존재하지 않거나 비밀번호가 틀렸습니다.'}
    )

  # 세션 id를 만들어 세션 표에 저장하고 쿠키로 보낸다
  session_id = secrets.token_urlsafe(32)
  user_session = UserSession(id=session_id, user=user)
  db.add(user_session)
  db.commit()

  response = RedirectResponse('/', status_code=303)
  response.set_cookie('session_id', session_id, httponly=True, samesite='lax')
  return response


@router.post('/logout')
def logout(request: Request, db: SessionDep):
  session_id = request.cookies.get('session_id')
  user_session = db.get(UserSession, session_id)

  if user_session:
    db.delete(user_session)
    db.commit()

  response = RedirectResponse('/', status_code=303)
  response.delete_cookie('session_id')
  return response
