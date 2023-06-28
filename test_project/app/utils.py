from fastapi import HTTPException
from starlette import status
from app.models import Employe_model, Salary_model, connect_db, get_redis_instance
from app.config import SECRET_KEY, ALGORITHM
import datetime
import hashlib
from jose import JWTError, jwt


class Emploe_Salary_Repository:

    SESSION = connect_db()

    @classmethod
    def get_users(cls):
        users =  cls.SESSION.query(Employe_model).all()
        return users

    @classmethod
    def get_salary_list(cls):
        salary_list = cls.SESSION.query(Salary_model).all()
        return salary_list

    @classmethod
    def get_user_by_id(cls, user_id: int):
        exists_user = cls.SESSION.query(Employe_model).filter(Employe_model.c.id == user_id).one_or_none()
        if exists_user:
            return exists_user
        return False

    @classmethod
    def get_user_by_username(cls, username: str):
        exists_user = cls.SESSION.query(Employe_model).filter(Employe_model.c.username == username).one_or_none()
        if exists_user:
            return exists_user
        return False

    @classmethod
    def create_user(cls, username, password, permission_level, full_name, age, position):
        exists_user = cls.get_user_by_username(username)
        if exists_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Пользователь {username} уже существует')
        try:
            query = Employe_model.insert().values(username=username, hashed_password=get_password_hash(password),
                                                     permission_level=permission_level, full_name=full_name,
                                                     age=age, position=position)
            cls.SESSION.execute(query)
            cls.SESSION.commit()
            return f'Пользователь успешно добавлен. Имя пользователя: {username}; уровень доступа: {permission_level}; ' \
                   f'полное имя: {full_name}; возраст: {age}; должность: {position}.'

        except Exception:
            return 'Произошла ошибка при работе с базой данных'

    @classmethod
    def update_user(cls, username, permission_level, full_name, age, position):
        exists_user = cls.get_user_by_username(username)
        if exists_user:
            try:
                query = Employe_model.update().where(Employe_model.c.username == username).values(
                    permission_level=permission_level,
                    full_name=full_name,
                    age=age,
                    position=position)

                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return f'Данные успешно обновлены. Имя пользователя: {username}; уровень доступа: {permission_level}; ' \
                   f'полное имя: {full_name}; возраст: {age}; должность: {position}'

            except Exception:
                return 'Произошла ошибка при работе с базой данных'
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Пользователь {username} не найден')

    @classmethod
    def delete_user(cls, username):
        exists_user = cls.get_user_by_username(username)
        if exists_user:
            try:
                query = Employe_model.delete().where(Employe_model.c.username == username)
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return f'Пользователь {username} успешно удален'

            except Exception:
                return 'Произошла ошибка при работе с базой данных'
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Пользователь {username} не найден')

    @classmethod
    def get_salary(cls, username):
        salary = cls.SESSION.query(Salary_model).filter(Salary_model.c.employe_username == username).one_or_none()
        return salary

    @classmethod
    def add_salary(cls, username, salary, salary_increase_date):
        exists_salary = cls.get_salary(username)
        if exists_salary:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Данные для '
                                                                                f'пользователя {username} '
                                                                                f'уже существуют')
        query = Salary_model.insert().values(salary=salary, employe_username=username,
                                                    salary_increase_date=salary_increase_date)
        cls.SESSION.execute(query)
        cls.SESSION.commit()
        return f'Добавлены новые данные. Имя пользователя: {username}; зарплата: {salary}; ' \
               f'дата повышения зарплаты: {salary_increase_date}.'

    @classmethod
    def update_salary(cls, username, salary, salary_increase_date):
        exists_salary = cls.get_salary(username)
        if exists_salary:
            try:
                query = Salary_model.update().where(Salary_model.c.employe_username == username).values(
                    salary=salary,
                    salary_increase_date=salary_increase_date)

                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return f'Данные успешно обновлены. Имя пользователя: {username}; зарплата: {salary}; ' \
                       f'дата повышения зарплаты: {salary_increase_date}'

            except Exception:
                return 'Произошла ошибка при работе с базой данных'
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=
            f'Данные о пользователе {username} не найдены')

    @classmethod
    def delete_salary(cls, username):
        exists_salary = cls.get_salary(username)
        if exists_salary:
            try:
                query = Salary_model.delete().where(Salary_model.c.employe_username == username)
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return f'Данные пользователя {username} успешно удалены'

            except Exception:
                return 'Произошла ошибка при работе с базой данных'
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=
            f'Данные пользователя {username} не найдены')


class Token_Repository():

    REDIS_INSTANCE = get_redis_instance()

    @classmethod
    def get_redis_instance(cls):
        redis_instance = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        return redis_instance

    @classmethod
    def write_token(cls, user, token):
        exists_token = cls.REDIS_INSTANCE.get(user.id)
        if exists_token:
            new_value = token
            cls.REDIS_INSTANCE.set(user.id, new_value)
        else:
            cls.REDIS_INSTANCE.set(user.id, token)

    @classmethod
    def get_token(cls, user_id):
        token = cls.REDIS_INSTANCE.get(user_id)
        return token

    @classmethod
    def delete_token(cls, user_id):
        cls.REDIS_INSTANCE.delete(user_id)


def get_password_hash(password: str):
    return hashlib.sha256(f'{SECRET_KEY}{password}'.encode('utf8')).hexdigest()

def verify_password(plain_password, hashed_password):
    if get_password_hash(plain_password) != hashed_password:
        return False
    return True

def authenticate_user(username, password):
    user_item = Emploe_Salary_Repository.get_user_by_username(username)
    if not user_item:
        return False
    if not verify_password(password, user_item.hashed_password):
        return False
    return user_item


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return False
    return True

