from app.utils import Emploe_Salary_Repository


#Cоздает администратора
def create_admin(username, password, permission_level, full_name, age, position):
    Emploe_Salary_Repository.create_user(username, password, permission_level, full_name, age, position)

#create_admin('user1', 'parol1', 1, 'Лесков Олег Владимирович', 32, 'Менеджер отдела кадров')


