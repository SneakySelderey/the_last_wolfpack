from browser import document, console


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
        """Функция, проверяющая совпадение данных двух полей.
        Принимает два поля, значения которых необходимо сравнить"""
        if field1.value != field2.value:
            field1.setCustomValidity("Passwords do not match")
            field1.validity.valid = False
    
    def checkField(self, field):
        """Метод, проверяющий поле на валидность введенных значений (по всем 
        ранее созданных методам). Принимает поле"""
        console.log(field.value)
        field.setCustomValidity("")
        self.valueMissing(field)
        self.typeMismatch(field)
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