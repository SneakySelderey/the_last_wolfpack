from browser import document, aio, timer, ajax, html, console
import re


class Data:
    """Класс для сохранения данных GET-запроса"""
    def __init__(self):
        self.data = []

    def change(self, data):
        """Функция для изменения данных"""
        self.data = data


def get_data(url, req):
    """Функция для получения списка сообщений и обновления"""
    global my_data
    if url is not None:
        return ajax.get(url, mode='json', oncomplete=lambda req: get_data(None, req))
    else:
        msg_count = len(my_data.data)
        my_data.change(req.response['messages'])
        if len(my_data.data) > msg_count:
            if chatbox is not None:
                for msg in my_data.data[msg_count:]:
                    new_div = html.DIV()
                    links = re.findall("(?P<url>https?://[^\s]+)", msg['text'])
                    new_text = []
                    for i in msg['text'].split():
                        if i in links:
                            new_text.append(f'<a href="{i}" class="link-light">' + i + '</a>')
                        else:
                            new_text.append(i)
                    new_text = ' '.join(new_text)
                    if msg['user']['id'] == user_id:
                        new_div.html = f"""<div class="media w-50 ml-auto mb-3">
    <div class="media-body">
        <div class="bg-dark-purple rounded py-2 px-3 mb-2 text-wrap">
            <p class="text-small mb-0 text-white text-break mb-link">{new_text}</p>
        </div>
        <p class="small text-muted text-right">{msg['time']}</p>
    </div>
    </div>"""
                    else:
                        path = 'static/img/profile_pictures/' + msg['user']['profile_picture']
                        new_div.html = f"""<div class="media w-50 mb-3">
            <figure>
                <img src="{path}" alt="user" width="50" class="rounded-circle">
                <figcaption class="mt-1 text-center" style="font-size: 11px;">{msg['user']['username']}</figcaption>
            </figure>
            <div class="media-body ml-3 text-wrap">
                <div class="bg-light rounded py-2 px-3 mb-2">
                    <p class="text-small mb-0 text-muted text-break mb-link">{new_text}</p>
                </div>
                <p class="small text-muted">{msg['time']}</p>
            </div>
        </div>"""
                    chatbox <= new_div
                    chatbox.scrollTop = chatbox.scrollHeight
        console.log('b')
        return True


async def main():
    """Функция устанновки таймера для периодического обновления сообщений"""
    timer.set_interval(update, 500)


def update():
    """Фукнция обновления сообщений"""
    get_data('api/messages', None)


def put_data(url, args):
    """Функция для PUT-запроса на добавление сообщения"""
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
my_data = Data()
get_data('api/messages', None)
chatbox = document.getElementById('chatbox')
btn = document.getElementById('button-addon2')
if btn is not None:
    btn.onclick = send_message
field = document.getElementById('msg_input')
aio.run(main())