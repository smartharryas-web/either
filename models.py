from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base


class User(Base):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(unique=True)
  password_hash: Mapped[str]


class UserSession(Base):
  __tablename__ = 'sessions'

  # 로그인할 때 만든 세션 id (쿠키 session_id 값)
  id: Mapped[str] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
  user: Mapped['User'] = relationship()


# 우리 팀 표는 이 아래에 (PLAN.md의 표 설계대로)
