import bcrypt
from typing import Optional
from sessions import Session

session = Session()


def hash_password(raw_password: Optional[str] = None):
    assert raw_password, 'Raw password can not be None'
    return bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(raw_password: Optional[str] = None, encoded_password: Optional[str] = None):
    assert raw_password, 'Raw password can not be None'
    assert encoded_password, 'Encoded password can not be None'
    return bcrypt.checkpw(raw_password.encode('utf-8'), encoded_password.encode('utf-8'))


class ResponseData:
    def __init__(self,
                 data,
                 status_code=200,
                 success=True):
        self.data = data
        self.status_code = status_code
        self.success = success


class BadRequest:
    def __init__(self, data, status_code=401):
        self.data = data
        self.status_code = status_code
