from bs4 import BeautifulSoup
import requests
from data import db_session
from data.captains import Captain
from data.uboats import Uboat
from threading import Thread
# import logging
import sqlite3
import os


# logging.basicConfig(
#     filename='db_logs.log',
#     format='%(asctime)s %(levelname)s %(name)s %(message)s'
# )


def write_captains():
    """Функция для сохранения фотографий капитанов"""
    db_sess = db_session.create_session()
    caps = db_sess.query(Captain).all()
    count_ = 0
    for i in caps:
        if i.image and f'static/img/{count_}.png' not in os.listdir(
                'static/img'):
            name = f'{count_}.png'
            with open(f'static/img/{name}', 'wb') as f:
                f.write(i.image)
        count_ += 1


def cap_parse():
    """Функция парсинга капитанов"""
    response = requests.get("https://uboat.net/men/commanders/")
    soup = BeautifulSoup(response.content, 'lxml')

    tr = soup.find_all('tr')

    if response.status_code == 200 and len(tr) > 10:
        # Подключение к БД
        con = sqlite3.connect("db/database.db")

        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""DELETE from caps""")

        con.commit()
        con.close()

        db_session.global_init("database.db")
        session = db_session.create_session()
        print('Captains parse started')

        count = 1
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
                    id=count,
                    image=requests.get(cap_list[1]).content,
                    name=cap_list[2],
                    info=cap_list[3],
                    boats=cap_list[4],
                    profile_link=cap_list[0])
                session.add(cap)
                session.commit()
            except requests.exceptions.MissingSchema:
                cap = Captain(
                    id=count,
                    name=cap_list[2],
                    info=cap_list[3],
                    boats=cap_list[4],
                    profile_link=cap_list[0])
                session.add(cap)
                session.commit()
            count += 1

        print('Captains parse finished')
        write_captains()

        # logging.info('Captains parse finished')
    else:
        print('No response from uboat.net captains page')
        # logging.warning('No response from uboat.net captains page')


def uboat_parse_cycle(number, session):
    global count
    parse_error = False
    no_num = False
    response = requests.get(f"https://uboat.net/boats/u{number}.htm")
    soup = BeautifulSoup(response.content, 'lxml')

    p = soup.find_all('p')

    if "<p>Here we've created a compilation of all the 1,153* U-boats that were commissioned into the Kriegsmarine before and during World War Two. Each boat has a complete history file, including construction facts, commanders, flotillas, successes and final fates.</p>" not in p:
        try:
            tr = soup.find_all('tr')

            tac_num = f'U-{number}'

            ordered = tr[1].text[7:]
            laid_down = tr[2].text[9:]
            launched = tr[3].text[8:]
            commissioned = tr[4].text[12:]
            while True:
                fail = False
                try:
                    for i in range(len(commissioned)):
                        if commissioned[i].isdigit() and commissioned[i + 1].isalpha():
                            fail = True
                            commissioned = commissioned.replace(commissioned[i] + commissioned[i + 1], commissioned[i] + ' ' + commissioned[i + 1])
                            break
                except IndexError:
                    pass
                if not fail:
                    break
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
            for i in range(len(tr)):
                if 'Career' in tr[i].text:
                    career = tr[i].text[6:]
                elif 'Successes' in tr[i].text:
                    successes = tr[i].text[9:]
                elif 'Fate' in tr[i].text:
                    fate = tr[i].text[6:-1]
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
            while '\xa0' in career:
                career = career.replace('\xa0', ' ')
            p = soup.find_all('p')
            coords = soup.find_all('script')
            for i in coords:
                if 'L.marker' in i.text:
                    index = i.text.find('L.marker([', -600)
                    a = i.text[index:index + 22]
                    coord2 = a.split(',')[0][-5:]
                    coord1 = a.split(',')[1][1:]
                    if coord1[-1] == ']':
                        coord1 = coord1[:-1]
                    coords = f'{coord1}, {coord2}'

            boat_list = (tac_num, ordered, laid_down, launched, commissioned, commanders, career, successes, fate, coords)
        except IndexError:
            parse_error = True

        if not parse_error:
            if type(boat_list[-1]) == str:
                boat = Uboat(
                    id=count,
                    tactical_number=boat_list[0],
                    ordered=boat_list[1],
                    laid_down=boat_list[2],
                    launched=boat_list[3],
                    commissioned=boat_list[4],
                    commanders=boat_list[5],
                    career=boat_list[6],
                    successes=boat_list[7],
                    fate=boat_list[8],
                    coords=boat_list[9])
                session.add(boat)
                session.commit()
            else:
                boat = Uboat(
                    id=count,
                    tactical_number=boat_list[0],
                    ordered=boat_list[1],
                    laid_down=boat_list[2],
                    launched=boat_list[3],
                    commissioned=boat_list[4],
                    commanders=boat_list[5],
                    career=boat_list[6],
                    successes=boat_list[7],
                    fate=boat_list[8])
                session.add(boat)
                session.commit()
            count += 1


def uboat_parse():
    response = requests.get("https://uboat.net/boats/listing.html")
    soup = BeautifulSoup(response.content, 'lxml')
    a = soup.find_all('a')
    if response.status_code == 200 and len(a) > 20:
        # Подключение к БД
        con = sqlite3.connect("db/database.db")

        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""DELETE from uboats""")

        con.commit()
        con.close()

        db_session.global_init("database.db")
        session = db_session.create_session()
        print('U-boats parse started')

        global count
        count = 1
        for number in range(1408):
            uboat_parse_cycle(number, session)

        for number in range(2320, 2372):
            uboat_parse_cycle(number, session)

        for number in range(2500, 2553):
            uboat_parse_cycle(number, session)

        for number in range(3000, 3045):
            uboat_parse_cycle(number, session)

        for number in range(3500, 3531):
            uboat_parse_cycle(number, session)

        for number in range(4700, 4713):
            uboat_parse_cycle(number, session)

        boat = Uboat(
            id=count,
            tactical_number='UD-5',
            laid_down='1938	Rotterdam, Netherlands',
            commissioned='30 Jan 1942	Frgkpt. Bruno Mahn',
            commanders='11.41 - 01.43 KptzS. Bruno Mahn, 12.42 - 01.43 Oblt. Klaus-Dietrich Konig (in deputize), 01.43 - 02.43 Kptlt. Horst-Tessen von Kameke, 02.43 - 05.45 Kptlt. Hans-Ulrich Scheltz',
            career='2 patrols: 11.41 - 08.42 5th Flotilla (Kiel) training, 08.42 - 01.43 10th Flotilla (Lorient) front boat, 01.43 - 05.45 U-Abwehrschule (Bergen) school boat',
            successes='Sank the British steamer Primrose Hill on 29 Oct, 1942 (7,628 tons)',
            fate='Built as the Dutch submarine O 27 but had not been launched when it was captured by the Germans at the Rotterdam yard on 14 May, 1940. Launched 26, Sept 1941 and commissioned into the German Navy on 30 Jan 1942. Surrendered at Bergen, Norway on 9 May 1945. Transferred from Bergen, Norway to Britain on 31 May 1945. Returned from Dundee, Scotland to the Netherlands on 13 July, 1945 and recommissioned as the Dutch submarine O 27. Stricken 14 Nov, 1959 and broken up in 1961.')
        session.add(boat)
        session.commit()
        boat = Uboat(
            id=count + 1,
            tactical_number='UIT-24',
            laid_down='1938	Odero-Terni-Orlando, Italy',
            commissioned='10 Sept, 1943	Oblt. Heinrich Pahls',
            commanders='12.43 - 05.45	Oblt. Heinrich Pahls',
            career='6 patrols: 12.43 - 09.44 12th Flotilla (Bordeaux) front boat, 10.44 - 05.45 33rd Flotilla (Flensburg) front boat',
            successes='None',
            fate='Launched as the Italian submarine Comandante Capellini on 13 March, 1939. Taken over by the Germans, following the Italian capitulation, at Sabang in the Far East on 10 Sept, 1943. Taken over by Japan at Kobe and recommissioned as I-503 or I-505 on 10 May, 1945. Surrendered at Kobe, Japan. Sunk by the US Navy on 16 April 1946 in the Kii Suido between the Japanese islands of Honshu and Shikolu.')
        session.add(boat)
        session.commit()
        boat = Uboat(
            id=count + 2,
            tactical_number='UIT-25',
            laid_down='1938	Odero-Terni-Orlando, Italy',
            commissioned='10 Sept, 1943	Frgkpt. Werner Striegler',
            commanders='12.43 - 08.44 Frgkpt. Werner Striegler, 09.44 - 02.45 Oblt. Herbert Schrein (in deputize), 02.45 - 05.45 Oblt. Alfred Meier',
            career='3 patrols: 	12.43 - 09.44 12th Flotilla (Bordeaux) front boat, 10.44 - 05.45 33rd Flotilla (Flensburg) front boat',
            successes='None',
            fate='Launched as the Italian submarine Luigi Torelli. Taken over at Kobe, Japan on 10 May, 1945 and commissioned as I-504. Surrendered at Kobe, Japan in August 1945. Sunk by the US Navy on 16 April 1946 in the Kii Suido between the Japanese islands of Honshu and Shikolu.')
        session.add(boat)
        session.commit()

        print('U-boats parse finished')
        # logging.info('U-boats parse finished')
    else:
        print('No response from uboat.net U-boats list page')
        # logging.warning('No response from uboat.net U-boats list page')


thread_cap_parse = Thread(target=cap_parse)
thread_uboat_parse = Thread(target=uboat_parse)


def run():
    global thread_cap_parse, thread_uboat_parse
    try:
        thread_cap_parse.start()
        thread_uboat_parse.start()
    except RuntimeError:
        pass
    thread_cap_parse.join()
    thread_uboat_parse.join()
