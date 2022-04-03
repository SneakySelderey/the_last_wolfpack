from browser import document, ajax, console


class Data:
    """Класс для сохранения данных GET-запроса"""
    def __init__(self):
        self.data = None
 
    def change(self, data):
        """Функция для изменения данных"""
        self.data = data
   
    def get(self, table, ids, col):
        """Функция для получения значения из json-файла"""
        return self.data[table][ids][col]


def put_data(url, args):
    """Функция для PUT-запроса на изменение данных об
    избранных капитанах или лодках"""
    console.log(args)
    ajax.put(url, data=args, oncomplete=lambda req: console.log(req))


def get_data(url, req):
    """Функция для получения списка капитанов и лодок"""
    global my_data
    if url is not None:
        return ajax.get(url, mode='json', oncomplete=lambda req: get_data(None, req))
    else:
        my_data.change(req.response)
        return True


def get_cell_value(table, row_id, col_id):
    """Функция для получения данных из ячейки по id строки таблицы"""
    console.log(table.rows[row_id].cells[col_id].innerHTML.strip())
    return table.rows[row_id].cells[col_id].innerHTML.strip()


def change_star(event):
    """Функция для изменения цвета и класса здездочки"""
    if 'checked' not in event.target.classList:
        event.target.classList.add('checked')
    else:
        event.target.classList.remove('checked')


def make_fav(event):
    """Функция, обрабатывающая нажатие на звездочку. Происходит измененеи
    ее цвета, создается put-запрос на изменение данных"""
    global my_id
    change_star(event)
    if caps_table is not None:
        cell_value = my_data.get('captains', int(event.target.id) - 1, 'name')
        req_dict = {"fav_caps": [cell_value]}
    else:
        cell_value = my_data.get('uboats', int(event.target.id) - 1, 'tactical_number')
        req_dict = {"fav_boats": [cell_value]}
    req_dict['add_fav'] = 1 if 'checked' in event.target.classList else 0
    put_data(f'/api/users/{user_id}', req_dict)


if document.getElementById('current_user_id').innerHTML:
    user_id = int(document.getElementById('current_user_id').innerHTML)
else:
    user_id = 0
elements = document.querySelectorAll('.fa-star')
caps_table = document.getElementById('caps_table')
boats_table = document.getElementById('boats_table')
my_url = '/api/caps' if caps_table is not None else '/api/uboats'
my_data = Data()
get_data(my_url, None)
for i in range(len(elements)):
    elements[i].onclick = make_fav