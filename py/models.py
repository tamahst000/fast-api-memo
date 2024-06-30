from datetime import datetime

from py.db import Base

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER

import hashlib

SQLITE3_NAME = "./db.sqlite3"


class User(Base):
    """
    Userテーブル

    id    : 主キー
    username : ユーザネーム
    password : パスワード
    """

    __tablename__ = "user"
    id = Column(
        "id",
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    username = Column("username", String(256))
    password = Column("password", String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.md5(password.encode()).hexdigest()


class Task(Base):
    """
    toDoタスク

    id    : 主キー
    user_id : 外部キー
    content : 内容
    date   : 作成日
    """

    __tablename__ = "task"
    id = Column(
        "id",
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    user_id = Column("user_id", ForeignKey("user.id"))
    content = Column("content", String(256))
    date = Column(
        "date",
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )

    def __init__(
        self,
        user_id: int,
        content: str,
        date: datetime = datetime.now(),
    ):
        self.user_id = user_id
        self.content = content
        self.date = date
