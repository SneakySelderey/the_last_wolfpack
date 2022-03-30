from browser import document, console


def get_cell_value(table, row_id, col_id):
    """Функция для получения данных из ячейки по id строки таблицы"""
    return table.rows[row_id].cells[col_id].innerHTML


def change_star(event):
    """Функция для изменения цвета и класса здездочки"""
    if 'checked' not in event.target.classList:
        event.target.style.color = 'orange'
        event.target.classList.add('checked')
    else:
        event.target.style.color = 'black'
        event.target.classList.remove('checked')


def f(event):
    console.log(get_cell_value(caps_table, int(event.target.id), 1))
    if 'checked' not in event.target.classList:
        event.target.style.color = 'orange'
        event.target.classList.add('checked')
    else:
        event.target.style.color = 'black'
        event.target.classList.remove('checked')


elements = document.querySelectorAll('.fa-star')
caps_table = document.getElementById('caps_table')
boats_table = document.getElementById('boats_table')
for i in range(len(elements)):
    elements[i].onclick = change_star