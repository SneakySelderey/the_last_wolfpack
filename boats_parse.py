from ast import Index
from bs4 import BeautifulSoup
import requests
from data import db_session
from data.captains import Captain


response = requests.get("https://uboat.net/boats/u2.htm")
soup = BeautifulSoup(response.content, 'lxml')

tr = soup.find_all('tr')

# db_session.global_init("db/database.db")
# session = db_session.create_session()

count = 0
number = 2

tac_num = f'U-{number}'

ordered = tr[1].text[7:]
laid_down = tr[2].text[9:]
launched = tr[3].text[8:]
commissioned = tr[4].text[12:]
while '\xa0' in commissioned:
    commissioned = commissioned.replace('\xa0', ' ')
commanders = tr[5].text[10:]
while True:
    fail = False
    try:
        for i in range(len(commanders)):
            if commanders[i].isalpha() and commanders[i + 1].isdigit():
                fail = True
                commanders = commanders.replace(commanders[i] + commanders[i + 1], commanders[i] + '       ' + commanders[i + 1])
                break
    except IndexError:
        pass
    if not fail:
        break
while '\xa0' in commanders:
    commanders = commanders.replace('\xa0', ' ')
commanders = commanders.replace('   ', ' ')
career = tr[9].text[6:]
if 'patrols' in career:
    career = career.replace('patrols', 'patrols:   ')
elif 'patrol' in career:
    career = career.replace('patrol', 'patrol:   ')
count_no_space = career.count(')')
count_with_space = career.count(') ')
while True:
    career = career.replace(')', ') ')
    count_with_space = career.count(') ')
    if count_with_space == count_no_space:
        break
successes = tr[13].text[9:]
fate = tr[14].text[6:-1]
p = soup.find_all('p')
for i in p:
    if f'U-{number}' in i.text:
        info = i.text
        break

boat_list = (tac_num, ordered, laid_down, launched, commissioned, commanders, career, successes, fate, info)

print(boat_list)

# try:
#     cap = Captain(
#         image=requests.get(cap_list[1]).content,
#         name=cap_list[2],
#         info=cap_list[3],
#         boats=cap_list[4],
#         profile_link=cap_list[0])
#     session.add(cap)
#     session.commit()
# except requests.exceptions.MissingSchema:
#     cap = Captain(
#         name=cap_list[2],
#         info=cap_list[3],
#         boats=cap_list[4],
#         profile_link=cap_list[0])
#     session.add(cap)
#     session.commit()
# count += 1
# print(count / len(tr) * 100)
