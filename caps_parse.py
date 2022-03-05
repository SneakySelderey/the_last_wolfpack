from bs4 import BeautifulSoup
import requests
from data import db_session
from data.captains import Captain


response = requests.get("https://uboat.net/men/commanders/")
soup = BeautifulSoup(response.content, 'lxml')

tr = soup.find_all('tr')

db_session.global_init("db/database.db")
session = db_session.create_session()

count = 0
for i in tr:
    block = BeautifulSoup(str(i), 'lxml')
    a = block.find_all('a')
    profile_link = 'https://uboat.net' + a[0].attrs['href']  # profile link

    try:
        img = block.find_all('img')
        photo_link = 'https://uboat.net' + img[0].attrs['src']  # photo link
    except IndexError:
        photo_link = 'None'

    name = a[1].text  # name
    if 'U-' in name or 'UC-' in name or 'UB' in name or 'UIT-' in name or 'UD-' in name:
        name = a[0].text

    td = block.find_all('td')
    info = td[1].text
    info = info[len(name):]
    count_no_space = info.count(')')
    count_with_space = info.count(') ')
    while True:
        info = info.replace(')', ') ')
        count_with_space = info.count(') ')
        if count_with_space == count_no_space:
            break
    count_no_space = info.count('.')
    count_with_space = info.count('. ')
    while True:
        info = info.replace('.', '. ')
        count_with_space = info.count('. ')
        if count_with_space == count_no_space:
            break
    for x in range(len(info)):
        info[x].replace('Г¤', 'a')
    boats = info.split('Commands:')[1]
    info = info[:info.find('Commands:')]

    cap_list = (profile_link, photo_link, name, info, boats)

    try:
        cap = Captain(
            image=requests.get(cap_list[1]).content,
            name=cap_list[2],
            info=cap_list[3],
            boats=cap_list[4],
            profile_link=cap_list[0])
        session.add(cap)
        session.commit()
    except requests.exceptions.MissingSchema:
        cap = Captain(
            name=cap_list[2],
            info=cap_list[3],
            boats=cap_list[4],
            profile_link=cap_list[0])
        session.add(cap)
        session.commit()
    count += 1
    print(count / len(tr) * 100)
