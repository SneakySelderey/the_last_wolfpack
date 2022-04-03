from browser import document, console, ajax
import json


class Data:
    """Класс для сохранения данных GET-запроса"""
    def __init__(self):
        self.data = None
 
    def change(self, data):
        """Функция для изменения данных"""
        self.data = data
    
    def get_names(self):
        """Функция для получения всех имен зарегистрировавшихся пользователей"""
        return [i['username'] for i in self.data['users']]
    
    def get_emails(self):
        """Функция для получения всех почт зарегистрировавшихся пользователей"""
        return [i["email"] for i in self.data['users']]


def get_data(url, req):
    """Функция для получения списка капитанов и лодок"""
    global users_data
    if url is not None:
        return ajax.get(url, oncomplete=lambda req: get_data(None, req))
    else:
        users_data.change(json.loads(req.text))
        return True


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


def checkExtension(data, *extensions):
    """Функция для проверки файла на соответствие разрещенным расширениям"""
    if data:
        if not any(data.endswith(x) for x in extensions):
            return 'Invalid file extension. Allowed extensions: ' + ', '.join(
                extensions)
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
    
    def checkUnique(self, field):
        """Функция, проверяющая уникальность значения поля. Принимает поле"""
        if field == name and field.value in users_data.get_names():
            field.setCustomValidity("User with this name is already exists")
            field.validity.valid = False
        if field == email and field.value in users_data.get_emails():
            field.setCustomValidity("User with this email is already exists")
            field.validity.valid = False

    def badInput(self, field):
        """Метод, проверяющий валидность введенного пароля. Принимает поле"""
        if field == password:
            resp = checkPassword(field.value)
        else:
            resp = checkExtension(field.value, '.png', '.jpg', '.jpeg')
        if resp:
            field.setCustomValidity(resp)
            field.validity.valid = False

    def checkField(self, field):
        """Метод, проверяющий поле на валидность введенных значений (по всем 
        ранее созданных методам). Принимает поле"""
        field.setCustomValidity("")
        if field != picture:
            self.valueMissing(field)
        self.typeMismatch(field)
        if field == name and (password2 is not None or picture is not None):
            self.checkUnique(name)
        if field == email and field.validity.valid and (
                password2 is not None or picture is not None):
            self.checkUnique(email)
        if field == password or field == picture:
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
        if form_submit is not None:
            form_submit.attributes.can_close = 'true'
        return True


def checkValidate(event):
    """Функция для проверки полей перед отправкой.
    Если не все поля валидны, запрещает отправку формы"""
    if password2 is not None:
        fields = [name, email, password, password2][::-1]
    elif picture is None:
        fields = [name, email]
    else:
        fields = [name, email, picture]
    if not checker.checkAll(fields):
        event.preventDefault()


def close(event):
    form_submit.attributes.can_close = 'true'
    document.getElementById("edit_form").style.display = "none"


form = document.getElementsByTagName('form')[0]
form_submit = document.getElementById('form_submit')
if form_submit is not None:
    form_submit.attributes.can_close = 'false'
name = document.getElementById('name')
email = document.getElementById('email')
password = document.getElementById('password')
password2 = document.getElementById('password2')
picture = document.getElementById('picture')
btn_close = document.getElementById('btn_close')
user_email = email.value if picture is not None else None
checker = ErrorChecker()
users_data = Data()
get_data('/api/users', None)
if btn_close is not None:
    btn_close.addEventListener('click', close)
if name is not None:
    name.addEventListener('input', lambda x: checker.checkField(name))
if email is not None:
    email.addEventListener('input', lambda x: checker.checkField(email))
if password is not None:
    password.addEventListener('input', lambda x: checker.checkField(password))
if password2 is not None:
    password2.addEventListener('input', lambda x: checker.checkField(password2))
if picture is not None:
    picture.addEventListener('input', lambda x: checker.checkField(picture))
form.addEventListener('submit', checkValidate)