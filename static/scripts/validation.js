const form  = document.getElementsByTagName('form')[0];
const email = document.getElementById('email');

email.addEventListener('input', function (event) {
    $.getJSON('/api/users', function(data) {
    console.log(data);
});
});

form.addEventListener('submit', function (event) {
  // Если поле email валдно, позволяем форме отправляться

  if(!email.validity.valid) {
    // Если поле email не валидно, отображаем соответствующее сообщение об ошибке
    showError();
    // Затем предотвращаем стандартное событие отправки формы
    event.preventDefault();
  }
});

function showError() {
  if(email.validity.valueMissing) {
    // Если поле пустое,
    // отображаем следующее сообщение об ошибке
    // alert('нету')
    email.setCustomValidity("This field is requiered")
  } else if(email.validity.typeMismatch) {
    // Если поле содержит не email-адрес,
    // отображаем следующее сообщение об ошибке
    // alert("Entered value needs to be an email address")
    email.setCustomValidity("Entered value needs to be an email address")
    email.reportValidity();
  } else {
    email.setCustomValidity('');
  }

}