from browser import document, console, ajax, html


def put_data(url, args):
    """Функция для PUT-запроса на добавление сообщения"""
    console.log(args)
    ajax.put(url, data=args, oncomplete=lambda req: console.log(req))


def send_message(event):
    """Функция для отправки сообщения"""
    if field.value:
        put_data(f'/api/users/{user_id}', {'msg': field.value})
        field.value = ''


if document.getElementById('current_user_id').innerHTML:
    user_id = int(document.getElementById('current_user_id').innerHTML)
else:
    user_id = 0
btn = document.getElementById('button-addon2')
chatbox = document.getElementById('chatbox')
if btn is not None:
    btn.onclick = send_message
field = document.getElementById('msg_input')