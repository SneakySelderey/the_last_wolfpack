from browser import document, console


def showError(event):
    if email.validity.valueMissing:
        email.setCustomValidity("This field is requiered")
        email.reportValidity()
    elif email.validity.typeMismatch:
        email.setCustomValidity("Entered value needs to be an email address")
        email.reportValidity()
    else:
        email.setCustomValidity('')


def checkValidate(event):
    if not email.validity.valid:
        showError()
        event.preventDefault()


form = document.getElementsByTagName('form')[0]
email = document.getElementById('email')
email.addEventListener('blur', showError)
form.addEventListener('submit', checkValidate)