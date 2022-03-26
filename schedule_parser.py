import schedule
from bs4 import BeautifulSoup
import requests
from data import db_session
from data.captains import Captain
from data.uboats import Uboat
import threading
import logging


logging.basicConfig(
    filename='db_logs.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)


def run_continuously():
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                scheduler1.run_all()

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def run_continuously2():
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                scheduler2.run_all()

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def cap_parse():
    response = requests.get("https://uboat.net/men/commanders/")
    soup = BeautifulSoup(response.content, 'lxml')

    tr = soup.find_all('tr')

    db_session.global_init("database.db")
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
        print(f'{count / len(tr) * 100} captains')
    logging.info('Captains parse finished')


def uboat_parse():
    db_session.global_init("database.db")
    session = db_session.create_session()
    count = 0
    for number in range(4720):
        parse_error = False
        try:
            no_num = False
            response = requests.get(f"https://uboat.net/boats/u{number}.htm")
            soup = BeautifulSoup(response.content, 'lxml')

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
            print(boat_list[-1])

        if not parse_error:
            if type(boat_list[-1]) == str:
                boat = Uboat(
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
        print(f'{count / 4720 * 100} uboats')

    boat = Uboat(
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
        tactical_number='UIT-25',
        laid_down='1938	Odero-Terni-Orlando, Italy',
        commissioned='10 Sept, 1943	Frgkpt. Werner Striegler',
        commanders='12.43 - 08.44 Frgkpt. Werner Striegler, 09.44 - 02.45 Oblt. Herbert Schrein (in deputize), 02.45 - 05.45 Oblt. Alfred Meier',
        career='3 patrols: 	12.43 - 09.44 12th Flotilla (Bordeaux) front boat, 10.44 - 05.45 33rd Flotilla (Flensburg) front boat',
        successes='None',
        fate='Launched as the Italian submarine Luigi Torelli. Taken over at Kobe, Japan on 10 May, 1945 and commissioned as I-504. Surrendered at Kobe, Japan in August 1945. Sunk by the US Navy on 16 April 1946 in the Kii Suido between the Japanese islands of Honshu and Shikolu.')
    session.add(boat)
    session.commit()

    logging.info('U-boats parse finished')


scheduler1 = schedule.Scheduler()
scheduler2 = schedule.Scheduler()

scheduler1.every().monday.at("00:00").do(cap_parse)
scheduler2.every().monday.at("00:00").do(uboat_parse)


def run():
    global stop_run_continuously
    stop_run_continuously = run_continuously()
    stop_run_continuously = run_continuously2()
