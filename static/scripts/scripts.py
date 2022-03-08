from browser import document, alert
from data import db_session


def sort_caps(event):
    data = document.getElementsByTagName("TR")
    sorted_data = sorted(list(data)[1:], key=lambda x: x.text.split('\t')[1].lower())
    document['caps_table'].text = '\n'.join([i.text for i in sorted_data])


document['sort_alph'].bind('click', sort_caps)