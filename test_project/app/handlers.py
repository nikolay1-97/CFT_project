import datetime
from fastapi import APIRouter, Request, Form, Response, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.utils import Emploe_Salary_Repository, Token_Repository, authenticate_user, \
    create_access_token, verify_token
from starlette import status
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')



@router.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@router.get('/login_for_users')
def auth_for_users(request: Request, response: Response):
    valid_token = True
    return templates.TemplateResponse("auth.html", {'request': request, 'valid_token': valid_token})


@router.get('/logout', response_class=RedirectResponse, status_code=302)
def logout_for_users(request: Request, response: Response):
    user_id = request.cookies.get('user_id')
    Token_Repository.delete_token(user_id)
    response.set_cookie(key='user_id', value='')
    return '/login_for_users'


@router.post('/registration')
def registration(username: str=Form(), password: str=Form(), permission_level: str=Form(), full_name: str=Form(),
                       age: int=Form(), position: str=Form()):

    return Emploe_Salary_Repository.create_user(username, password, permission_level, full_name, age, position)


@router.get('/add_info_about_salary', response_class=RedirectResponse, status_code=302)
def add_information_about_salary_get(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'
    return templates.TemplateResponse("add_info_about_salary.html", {'request': request, 'user_id': user_id})


@router.post('/add_information_about_salary')
def add_information_about_salary_post(username: str=Form(), salary: str=Form(), salary_increase_date: str=Form()):
    return Emploe_Salary_Repository.add_salary(username, salary, salary_increase_date)


@router.get('/update_info_about_salary', response_class=RedirectResponse, status_code=302)
def update_salary(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'
    return templates.TemplateResponse("update_salary.html", {'request': request, 'user_id': user_id})


@router.post('/update_info_about_salary_post')
def update_salary_post(username: str=Form(), salary: str=Form(), salary_increase_date: str=Form()):
    return Emploe_Salary_Repository.update_salary(username, salary, salary_increase_date)


@router.get('/delete_salary', response_class=RedirectResponse, status_code=302)
def delete_salary(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'
    return templates.TemplateResponse("delete_salary.html", {'request': request, 'user_id': user_id})


@router.post('/delete_salary_post')
def delete_salary_post(username: str=Form()):
    return Emploe_Salary_Repository.delete_salary(username)


@router.get('/get_info', response_class=RedirectResponse, status_code=302)
def get_info(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '':
        return '/login_for_users'
    user = Emploe_Salary_Repository.get_user_by_id(user_id)
    is_admin = False
    if user.permission_level == 1:
        is_admin = True
    return templates.TemplateResponse("get_info.html", {'request': request, 'user_id': user_id, 'is_admin': is_admin})

#Вход в систему. Генерирует и записывает токен в redis
@router.post('/token', response_class=RedirectResponse, status_code=302)
def login_for_access_token(request: Request, response: Response, username: str = Form(), password: str = Form()):

    user = authenticate_user(username, password)

    if not user:
        wrong_password = True
        return templates.TemplateResponse("auth.html", {'request': request, 'wrong_password': wrong_password})
    else:
        access_token_expires = datetime.timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
        Token_Repository.write_token(user, token)
        response.set_cookie(key='user_id', value=user.id)
        return '/get_info'

#Отображает страницу с информацией о зарплате
@router.post("/get_info_about_salary", response_class=RedirectResponse, status_code=302)
def get_info_about_salay(request: Request):
    user_id = request.cookies.get('user_id')

    user = Emploe_Salary_Repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователь не найден')
    token = Token_Repository.get_token(user_id)
    valid_token = verify_token(token)
    if not valid_token:
        return templates.TemplateResponse("auth.html", {'request': request, 'valid_token': valid_token})

    salary = Emploe_Salary_Repository.get_salary(user.username)
    if not salary:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Данные о вашей зарплате еще не занесены в систему')

    return templates.TemplateResponse("info_page.html", {'request': request,
                                                         'salary': salary.salary,
                                                    'date': salary.salary_increase_date, 'user_id': user_id})



@router.get('/user_registration', response_class=RedirectResponse, status_code=302)
def registration_for_users(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'

    return templates.TemplateResponse("registration.html", {'request': request, 'user_id': user_id})


@router.get('/update_user', response_class=RedirectResponse, status_code=302)
def update_user(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'

    return templates.TemplateResponse("update_user.html", {'request': request, 'user_id': user_id})


@router.post('/update_user_post')
def update_user_post(username: str=Form(), permission_level: str=Form(), full_name: str=Form(),
                       age: int=Form(), position: str=Form()):

    return Emploe_Salary_Repository.update_user(username, permission_level, full_name, age, position)


@router.get('/delete_user', response_class=RedirectResponse, status_code=302)
def delete_user(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'

    return templates.TemplateResponse("delete_user.html", {'request': request, 'user_id': user_id})


@router.post('/delete_user_post')
def delete_user_post(username: str=Form()):
    return Emploe_Salary_Repository.delete_user(username)


@router.get('/get_users', response_class=RedirectResponse, status_code=302)
def get_users(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'

    users = Emploe_Salary_Repository.get_users()

    return templates.TemplateResponse("users_list.html", {'request': request, 'users': users, 'user_id': user_id})


@router.get('/get_salary_list', response_class=RedirectResponse, status_code=302)
def get_salary_list(request: Request):
    user_id = request.cookies.get('user_id')
    if user_id == '' or Emploe_Salary_Repository.get_user_by_id(user_id).permission_level != 1:
        return '/login_for_users'

    salary_list = Emploe_Salary_Repository.get_salary_list()

    return templates.TemplateResponse("salary_list.html", {'request': request, 'salary_list': salary_list, 'user_id': user_id})
