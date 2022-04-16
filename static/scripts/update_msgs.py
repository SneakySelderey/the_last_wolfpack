from browser import document, aio, timer, ajax, html


class Data:
    """Класс для сохранения данных GET-запроса"""
    def __init__(self):
        self.data = []
 
    def change(self, data):
        """Функция для изменения данных"""
        self.data = data


def get_data(url, req, first=False):
    """Функция для получения списка сообщений ы"""
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
                    if msg['user']['id'] == user_id:
                        new_div.html = f"""<div class="media w-50 ml-auto mb-3">
    <div class="media-body">
        <div class="bg-dark-purple rounded py-2 px-3 mb-2 text-wrap">
            <p class="text-small mb-0 text-white text-break">{msg['text']}</p>
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
                    <p class="text-small mb-0 text-muted text-break">{msg['text']}</p>
                </div>
                <p class="small text-muted">{msg['time']}</p>
            </div>
        </div>"""
                    chatbox <= new_div
                    chatbox.scrollTop = chatbox.scrollHeight
        return True


async def main():
    """Функция устанновки таймера для периодического обновления сообщений"""
    timer.set_interval(update, 500)


def update():
    """Фукнция обновления сообщений"""
    get_data('api/messages', None)


if document.getElementById('current_user_id').innerHTML:
    user_id = int(document.getElementById('current_user_id').innerHTML)
else:
    user_id = 0
my_data = Data()
get_data('api/messages', None)
chatbox = document.getElementById('chatbox')
aio.run(main())