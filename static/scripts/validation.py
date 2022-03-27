from browser import document, console, window
import json


def checkPassword(data, min_l=8):
    """Функция для проверки пароля на надежность. Пароль считаестя надежным,
    если его длина не менее min_l символов и есть как минимум одна буква и
    одна цифра"""
    if len(data) < min_l:
        return f'Must be at least {min_l} characters'
    if not any(x.isalpha() for x in data):
        return 'Must be at least one letter'
    if not any(x.isdigit() for x in data):
        return 'Must be at least one digit'
    return False


class ErrorChecker:
    """Класс для проверки валидности вводимых пользователем данных"""
    def __init__(self):
        pass

    def valueMissing(self, field):
        """Метод, проверяющий наличие введенных данных в поле.
        Принимает поле"""
        if field.validity.valueMissing or not field.value:
            field.setCustomValidity("This field is requiered")
            field.validity.valid = False

    def typeMismatch(self, field):
        """Метод, проверяющий совпадение введенных данных с нужным типом.
        Принимает поле"""
        if field.validity.typeMismatch:
            field.setCustomValidity("Entered value needs to be an email "
                                    "address")
            field.validity.valid = False
    
    def equalsTo(self, field1, field2):
        """Метод, проверяющий совпадение данных двух полей.
        Принимает два поля, значения которых необходимо сравнить"""
        if field1.value != field2.value:
            field1.setCustomValidity("Passwords do not match")
            field1.validity.valid = False

    def badInput(self, field):
        """Метод, проверяющий валидность введенного пароля. Принимает поле"""
        resp = checkPassword(field.value)
        if resp:
            field.setCustomValidity(resp)
            field.validity.valid = False

    def ajaxCall(self):
        """Метод, проверяющий наличие пользователя в БД. Делает ajax-запрос,
        который в случае успешного выполнения делает остальную работу в
        функции onSuccess"""
        jq.ajax('/api/users', {'success': onSuccess})

    def checkField(self, field):
        """Метод, проверяющий поле на валидность введенных значений (по всем 
        ранее созданных методам). Принимает поле"""
        field.setCustomValidity("")
        self.valueMissing(field)
        self.typeMismatch(field)
        if field == email:
            self.ajaxCall()
        if field == password:
            self.badInput(field)
        if field == password2:
            self.equalsTo(field, password)
        field.reportValidity()
    
    def checkAll(self, fields):
        """Метод, проверяющий все поля на валидность. Принимает список полей.
        Возвращает True, если все поля валидны, иначе False"""
        if not all(field.validity.valid for field in fields):
            for field in fields:
                self.checkField(field)
            return False
        return True


def checkValidate(event):
    """Функция для проверки полей перед отправкой.
    Если не все поля валидны, запрещает отправку формы"""
    if not checker.checkAll([name, email, password, password2][::-1]):
        event.preventDefault()


def onSuccess(data, status, req):
    """Функция, которая вызывается, если ajax смог успешно выполнить запрос.
    Функция проверяет наличие почты, которую вводит пользователь в поле в
    списке почт зарегистрированных пользователей. Если она найдена, то
    вызываетяя ошибка валидации об уникальности"""
    if email.value in [data.users[i]["email"] for i in range(
            len(data.users))]:
        email.setCustomValidity("User with this email is already exists")
        email.validity.valid = False
        email.reportValidity()


jq = window.jQuery
form = document.getElementsByTagName('form')[0]
name = document.getElementById('name')
email = document.getElementById('email')
password = document.getElementById('password')
password2 = document.getElementById('password2')
checker = ErrorChecker()
name.addEventListener('input', lambda x: checker.checkField(name))
email.addEventListener('input', lambda x: checker.checkField(email))
password.addEventListener('input', lambda x: checker.checkField(password))
password2.addEventListener('input', lambda x: checker.checkField(password2))
form.addEventListener('submit', checkValidate)