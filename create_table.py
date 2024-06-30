from py.models import *
import py.db as db
import os


if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        Base.metadata.create_all(db.engine)

    user = User(username="fastapi", password="fastapi")
    db.session.add(user)
    db.session.commit()

    task1 = Task(
        user_id=user.id,
        content="上の「新規メモを作成」からメモを作成できます",
    )
    task2 = Task(
        user_id=user.id,
        content="ここをクリックすることで、メモの編集ができます",
    )
    task3 = Task(
        user_id=user.id,
        content="右の「X」を押すとメモの消去ができます",
    )
    task4 = Task(
        user_id=user.id,
        content="右上の「Logout」からログアウトできます",
    )
    db.session.add(task1)
    db.session.add(task2)
    db.session.add(task3)
    db.session.add(task4)
    db.session.commit()

    db.session.close()
