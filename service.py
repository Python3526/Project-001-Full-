import utils
from typing import Union
from db import commit, cur
from dto import UserRegisterDTO
from models import User, UserRole, UserStatus, TodoType
from sessions import Session
from validators import check_validators

session = Session()


@commit
def login(username: str, password: str) -> Union[utils.BadRequest, utils.ResponseData]:
    user: User | None = session.check_session()
    if user:
        return utils.BadRequest('You already logged in\n', status_code=401)

    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username, (username,))
    user_data = cur.fetchone()
    if not user_data:
        return utils.BadRequest('Bad credentials\n', status_code=401)
    user = User.from_tuple(user_data)
    if user.login_try_count >= 3:
        return utils.BadRequest('User is blocked\n')
    if not utils.check_password(password, user.password):
        update_count_query = """update users set login_try_count = login_try_count + 1 where username = %s;"""
        cur.execute(update_count_query, (user.username,))
        return utils.BadRequest('Bad credentials\n', status_code=401)

    session.add_session(user)
    return utils.ResponseData('User Successfully Logged in✅\n')


def login_for_blocking(username: str, password: str) -> Union[utils.BadRequest, utils.ResponseData]:
    user: User | None = session.check_session()
    if user:
        return utils.BadRequest('You already logged in\n', status_code=401)

    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username, (username,))
    user_data = cur.fetchone()

    if not user_data:
        return utils.BadRequest('Bad credentials\n', status_code=401)

    user = User.from_tuple(user_data)

    if user.login_try_count >= 3:
        return utils.BadRequest('User is blocked\n')

    if user.role == "ADMIN":
        if not utils.check_password(password, user.password):
            update_count_query = """update users set login_try_count = login_try_count + 1 where username = %s;"""
            cur.execute(update_count_query, (user.username,))
            return utils.BadRequest('Bad credentials\n', status_code=401)

        session.add_session(user)
        return utils.ResponseData('U can block users✅\n')

    else:
        return utils.BadRequest("U do'nt have permisson to block users\n", status_code=401)


@commit
def register(dto: UserRegisterDTO):
    try:
        check_validators(dto)
        user_data = '''select * from users where username = %s;'''
        cur.execute(user_data, (dto.username,))
        user = cur.fetchone()
        if user:
            return utils.BadRequest('User already registered❗\n', status_code=401)

        insert_user_query = """
        insert into users(username,password,role,status,login_try_count)
        values (%s,%s,%s,%s,%s);
        """
        user_data = (dto.username, utils.hash_password(dto.password), UserRole.USER.value, UserStatus.ACTIVE.value, 0)
        cur.execute(insert_user_query, user_data)
        return utils.ResponseData('User Successfully Registered👌\n')

    except AssertionError as e:
        return utils.BadRequest(e)


def logout():
    global session
    if session.check_session():
        session.session = None
        return utils.ResponseData('User Successfully Logged Out ✅\n')


@commit
def todo_add(title: str):
    insert_query = """INSERT INTO todos(name,todo_type,user_id)
        VALUES (%s,%s,%s);"""
    data = (title, TodoType.Personal.value, session.session.id)

    cur.execute(insert_query, data)
    return utils.ResponseData('INSERTED TODO✅')


@commit
def todo_delete(en_id: int):
    delete_query = """DELETE FROM todos WHERE id = %s;"""
    cur.execute(delete_query, (en_id,))

    return utils.ResponseData('DELETED TODO✅')


@commit
def todo_update(en_id: int, title: str):
    update_query = """UPDATE todos SET title = %s, id = %s"""
    cur.execute(update_query, (title, en_id))

    return utils.ResponseData('UPDATED✅')


def display_todos_inc():
    cur.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    for i in todos:
        print(i)

    return utils.ResponseData('All todos diplayed✅\n')


def display_todos_desc():
    cur.execute("SELECT * FROM todos ORDER BY id DESC")
    todos = cur.fetchall()
    for i in todos:
        print(i)

    return utils.ResponseData('All todos diplayed✅\n')


def display_todos_title_inc():
    cur.execute("SELECT * FROM todos ORDER BY name")
    todos = cur.fetchall()
    for i in todos:
        print(i)

    return utils.ResponseData('All todos diplayed✅\n')


def display_todos_title_desc():
    cur.execute("SELECT * FROM todos ORDER BY name DESC")
    todos = cur.fetchall()
    for i in todos:
        print(i)

    return utils.ResponseData('All todos diplayed✅\n')


@commit
def block_user(en_id: int):
    blocking_query = """UPDATE users SET login_try_count = 4 WHERE id = %s;"""
    cur.execute(blocking_query, (en_id,))

    return utils.ResponseData('User blocked')
