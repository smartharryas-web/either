# 밸런스 게임

짜장면이냐 짬뽕이냐, 부먹이냐 찍먹이냐.
질문 하나에 선택지 두 개를 올리고, 사람들이 고르면 어느 쪽이 많은지 보여 주는 사이트입니다.

회원가입, 로그인, 로그아웃은 이미 동작합니다. 질문, 투표, 댓글은 팀이 직접 만듭니다.

## 시작하기

팀장 컴퓨터 한 대로 진행합니다.

### 1. 팀 저장소 만들기

1. 이 저장소 오른쪽 위의 **Use this template** → **Create a new repository**를 누릅니다.
2. 저장소 이름을 정하고 **Private**으로 만듭니다.
3. **Settings** → **Collaborators**에서 팀원과 강사를 초대합니다.

### 2. 내려받기

```bash
git clone https://github.com/팀장아이디/저장소이름.git
cd 저장소이름
code .
```

VS Code 터미널에서 패키지를 설치합니다.

```bash
uv sync
```

### 3. DB 만들기

```bash
psql -d postgres     # macOS
psql -U postgres     # Windows
```

```sql
CREATE DATABASE either OWNER sd4;
\q
```

### 4. 실행하기

```bash
uv run alembic upgrade head
uv run fastapi dev
```

http://localhost:8000/ 에서 회원가입하고 로그인해 보세요. 위쪽에 내 아이디가 보이면 준비가 끝났습니다.

## 만들 것

1. 질문 목록, 질문 올리기, 질문 상세
2. A나 B에 투표하고 결과를 퍼센트로 보기. 마음이 바뀌면 다시 고를 수 있습니다.
3. 댓글 달기와 지우기
4. 내가 올린 질문, 내가 쓴 댓글만 지울 수 있게 하기

표와 주소는 `PLAN.md`에 먼저 적고 시작합니다.

## 작업 방식

코드는 직접 칩니다. Claude에게 질문하거나 에러 뜻을 물어볼 수는 있지만, `.py` 파일을 대신 써 주지는 않습니다.

치는 사람은 기능마다 돌아가며 바꿉니다. 치지 않는 사람은 옆에서 insta 코드를 찾아 주고 빠진 줄을 짚어 주세요.

기능 하나가 동작하면 바로 커밋합니다. 메시지에 친 사람 이름을 적어 주세요.

```bash
git add .
git commit -m "투표 기능 (민수)"
```

새 라우터 파일을 만들었다면 `main.py`에 두 줄을 더해야 주소가 생깁니다.

```python
from routers import auth, home, questions

app.include_router(questions.router)
```

표에 칸을 더하거나 표를 새로 만들 때는 `models.py`를 고친 다음 리비전을 하나 더 만듭니다.

```bash
uv run alembic revision --autogenerate -m "무엇을 바꿨는지"
uv run alembic upgrade head
```

끝나면 팀장이 push하고, 팀원은 각자 clone해 둡니다.

## 화면 꾸미기

화면은 Claude에게 맡깁니다. 한 번에 한 페이지씩, 원하는 느낌을 말로 설명하거나 참고할 사이트 캡처를 보여 주세요. 처음에는 `base.html`과 첫 화면부터 하는 게 좋습니다.

이 저장소에는 디자인을 도와주는 `frontend-design` 스킬이 들어 있어서, Claude가 화면을 꾸밀 때 알아서 씁니다. 첫 부탁에서는 사이트 전체의 분위기를 먼저 정해 주세요. "레트로 오락실 느낌", "신문 1면처럼", "파스텔 톤에 둥근 카드"처럼 말하면 됩니다.

꾸민 뒤에는 두 가지를 확인합니다.

- `git diff`에서 폼의 `name`, `action`, 링크 주소가 그대로인지
- 가입부터 투표, 댓글, 지우기까지 다시 눌러 봐도 잘 되는지

Claude가 정한 색과 버튼 모양은 `design/DESIGN.md`에 쌓입니다. 다음 페이지도 그 규칙을 따라 꾸며집니다.

## 폴더 구조

```
├── main.py            앱 시작, 라우터 연결
├── database.py        DB 주소와 Base
├── models.py          표 (User, UserSession + 우리가 만들 표)
├── deps.py            SessionDep, CurrentUserDep, templates
├── photos.py          사진 저장 save_photo
├── routers/
│   ├── auth.py        가입, 로그인, 로그아웃
│   └── home.py        첫 화면 /
├── templates/         HTML
├── static/style.css   CSS
├── alembic/           리비전
├── design/DESIGN.md   디자인 규칙
└── PLAN.md            우리 팀 설계
```

## 막혔을 때

- `database "either" already exists` — 이미 DB가 있다는 뜻입니다. 그대로 `uv run alembic upgrade head`로 넘어가면 됩니다.
- `Target database is not up to date` — 리비전을 만들기 전에 `uv run alembic upgrade head`를 먼저 하세요.
- 새로 만든 주소에서 `{"detail":"Not Found"}` — `main.py`에 `include_router`를 더했는지 확인하세요.
