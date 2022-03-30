from browser import document, ajax, console


def put_data(url, args):
    """Функция для PUT-запроса на изменение данных об
    избранных капитанах или лодках"""
    console.log(args)
    ajax.put(url, data=args, oncomplete=lambda req: console.log(req))


def get_cell_value(table, row_id, col_id):
    """Функция для получения данных из ячейки по id строки таблицы"""
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
    change_star(event)
    if caps_table is not None:
        cell_value = get_cell_value(caps_table, int(event.target.id), 1)
        req_dict = {"fav_caps": [cell_value]}
    else:
        cell_value = get_cell_value(boats_table, int(event.target.id), 1)
        req_dict = {"fav_boats": [cell_value]}
    req_dict['add_fav'] = 1 if 'checked' in event.target.classList else 0
    put_data(f'/api/users/{user_id}', req_dict)


user_id = int(document.getElementById('current_user_id').innerHTML)
elements = document.querySelectorAll('.fa-star')
caps_table = document.getElementById('caps_table')
boats_table = document.getElementById('boats_table')
for i in range(len(elements)):
    elements[i].onclick = make_fav