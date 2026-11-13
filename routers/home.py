from fastapi import Request, APIRouter

from deps import templates, CurrentUserDep

router = APIRouter()


# 첫 화면. 팀 서비스의 목록 화면 등으로 바꾼다
@router.get('/')
def home(
  request: Request,
  user: CurrentUserDep
):
  return templates.TemplateResponse(
    request=request,
    name='home.html',
    context={'user': user}
  )
