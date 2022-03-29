from browser import document, console, window


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
        self.valueMissing(field)
        self.typeMismatch(field)
        if field == email and field.validity.valid and (
                password2 is not None or picture is not None):
            jq.ajax('/api/users', {'success': onSuccess})
            return
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


def onSuccess(data, status, req):
    """Функция, которая вызывается, если ajax смог успешно выполнить запрос.
    Функция проверяет наличие почты, которую вводит пользователь в поле в
    списке почт зарегистрированных пользователей. Если она найдена, то
    вызываетяя ошибка валидации об уникальности"""
    emails = [data.users[i]["email"] for i in range(len(data.users))]
    if email.value in emails and email.value != user_email:
        email.setCustomValidity("User with this email is already exists")
        email.validity.valid = False
        email.reportValidity()


jq = window.jQuery
form = document.getElementsByTagName('form')[0]
form_submit = document.getElementById('form_submit')
if form_submit is not None:
    form_submit.attributes.can_close = 'false'
name = document.getElementById('name')
email = document.getElementById('email')
password = document.getElementById('password')
password2 = document.getElementById('password2')
picture = document.getElementById('picture')
user_email = email.value if picture is not None else None
checker = ErrorChecker()
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