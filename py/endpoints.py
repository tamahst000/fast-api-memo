from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import py.db as db
from py.models import User, Task
import re
import hashlib

app = FastAPI(title="FastAPIメモアプリ")

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env
app.mount(path="/py", app=StaticFiles(directory="py"))
app.mount(path="/js", app=StaticFiles(directory="javascript"))


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{username}/admin")
def admin(request: Request, username):
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()

    return templates.TemplateResponse(
        "admin.html", {"request": request, "user": user, "task": task}
    )


@app.post("/{username}/admin")
def admin(request: Request, username):
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()

    return templates.TemplateResponse(
        "admin.html", {"request": request, "user": user, "task": task}
    )


@app.get("/{username}/detail")
def detail(request: Request, username: str):
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()
    return templates.TemplateResponse(
        "detail.html", {"request": request, "user": user, "task": task}
    )


@app.post("/{username}/add")
async def add(request: Request, username: str):
    user = db.session.query(User).filter(User.username == username).first()
    data = await request.form()
    task = Task(user_id=user.id, content=data["content"])
    db.session.add(task)
    db.session.commit()
    db.session.close()
    return RedirectResponse(f"/{username}/admin")


@app.get("/{username}/delete/{task_id}")
def delete(request: Request, username: str, task_id: int):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    db.session.delete(task)
    db.session.commit()
    db.session.close()
    return RedirectResponse(f"/{username}/admin")


@app.get("/{username}/detail/{task_id}")
def task_detail(request: Request, username: str, task_id: int):
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.id == task_id).first()
    db.session.close()
    return templates.TemplateResponse(
        "update_detail.html", {"request": request, "user": user, "task": task}
    )


@app.post("/{username}/update/{task_id}")
async def update(request: Request, username: str, task_id: int):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    data = await request.form()
    task.content = data["content"]
    db.session.add(task)
    db.session.commit()
    db.session.close()
    return RedirectResponse(f"/{username}/admin")


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/certification")
async def certification(request: Request):
    data = await request.form()
    username = data.get("username")
    password = data.get("password")
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    error = []
    tmp_user = db.session.query(User).filter(User.username == username).first()
    tmp_password = (
        db.session.query(User).filter(User.password == hashed_password).first()
    )
    pattern = re.compile(r"\w{4,20}")
    pattern_pw = re.compile(r"\w{6,20}")

    if tmp_user is None or tmp_password is None:
        error.append("ユーザ名かパスワードが間違っています")
    if pattern.match(username) is None:
        error.append("ユーザ名は4~20文字の半角英数字にしてください。")
    if pattern_pw.match(password) is None:
        error.append("パスワードは6~20文字の半角英数字にしてください。")

    if error:
        return templates.TemplateResponse(
            "login.html", {"request": request, "username": username, "error": error}
        )

    return RedirectResponse(f"/{username}/admin")


@app.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/register")
async def register(request: Request):
    data = await request.form()
    username = data.get("username")
    password = data.get("password")
    password_tmp = data.get("password_tmp")

    error = []
    tmp_user = db.session.query(User).filter(User.username == username).first()
    pattern = re.compile(r"\w{4,20}")
    pattern_pw = re.compile(r"\w{6,20}")
    if tmp_user is not None:
        error.append("同じユーザ名のユーザが存在します。")
    if password != password_tmp:
        error.append("入力したパスワードが一致しません。")
    if pattern.match(username) is None:
        error.append("ユーザ名は4~20文字の半角英数字にしてください。")
    if pattern_pw.match(password) is None:
        error.append("パスワードは6~20文字の半角英数字にしてください。")

    if error:
        return templates.TemplateResponse(
            "signup.html", {"request": request, "username": username, "error": error}
        )

    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    db.session.close()

    complete = [
        f"~{ username }~ さんのユーザ登録が完了しました!!",
        "↓ ログインはこちらから",
    ]

    return templates.TemplateResponse(
        "login.html", {"request": request, "username": username, "complete": complete}
    )


@app.get("/get-user")
def get(request: Request):
    user = db.session.query(User)
    db.session.close()
    user_json = [
        {
            "id": u.id,
            "username": u.username,
        }
        for u in user
    ]
    return user_json


@app.get("/get-task/{username}")
def get(request: Request, username: str):
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()
    task_json = [
        {
            "id": t.id,
            "user_id": t.user_id,
            "content": t.content,
            "date": t.date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for t in task
    ]
    return task_json


@app.delete("/delete-user/{username}")
def delete(request: Request, username: str):
    user = db.session.query(User).filter(User.username == username).first()
    db.session.delete(user)
    db.session.commit()
    db.session.close()
    delete_user_json = [{"message": "ユーザが削除されました"}]
    return delete_user_json
