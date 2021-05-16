from tkinter import *
from tkinter import messagebox

import api
import json
import random
import pdb

root = Tk()
root.title('ss dummy client')
root.geometry('640x640')
root.resizable(False, False)

target_url = ''
user_token = ''
user_credit = 0

game_coin = 0
game_point = 0
game_spin = 0

active_game_pk = 0

# 0 : 대기 / 1 : 돌아감
game_coin_state = 0

# 0 : 대기 / 1 : 돌아감
game_spin_state = 0


game_speed = 10


def cmd_btn_connect():
    global target_url
    target_url = url_entry.get()
    response = api.connect(target_url, entry_ID.get() )
    res_dict = json.loads(response.text)

    global user_token
    user_token = res_dict['token']

    global user_credit
    user_credit = res_dict['credit']

    entry_ID['state'] = 'disabled'
    label_Credit['text'] = 'credit : ' + str(user_credit)
    btn_connect['state'] = 'disabled'
    url_entry['state']   = 'disabled'
    gamenumber_entry['state'] = 'normal'

    refresh_gamelist()


def refresh_gamelist():
    response = api.get_game_list(target_url, user_token)
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        games_dict = res_dict['games']

        list_Games.delete(0, END)

        if len(games_dict) > 0:
            for key, val in games_dict.items():
                list_Games.insert(END, val)
        else:
            list_Games.insert(0, '진행중인 게임이 없습니다')


def cmd_btn_create_game():
    response = api.create_game(target_url, 100, user_token)
    res_dict = json.loads(response.text)
    print(res_dict)

    if res_dict['result'] == 'success':
        # new_game_dict = { 'pk': res_dict['pk'], 'coin': res_dict['coin'], 'point': res_dict['point']}
        refresh_gamelist()
    else:
        put_coin_log(res_dict['desc'])

        # global user_credit
        # user_credit -= 10000
        # label_Credit['text'] = 'credit : ' + str(user_credit)


def cmd_btn_insert_credit():
    game_pk = gamenumber_entry.get()
    credit = 10000
    response = api.insert_credit(target_url, game_pk, credit, user_token)
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        global user_credit, game_coin
        user_credit = res_dict['user_credit']
        game_coin = res_dict['game_coin']

        label_Credit['text'] = 'credit : ' + str(user_credit)
        label_game_coin['text'] = 'coin : ' + str(game_coin)


def cmd_btn_resume_game():
    global active_game_pk
    active_game_pk = gamenumber_entry.get()

    response = api.resume_game(target_url, active_game_pk, user_token)
    res_dict = json.loads(response.text)
    print(res_dict)

    if res_dict['result'] == 'success':
        global game_coin, game_point, game_spin
        game_coin   = res_dict['coin']
        game_point  = res_dict['point']
        game_spin   = res_dict['spin_count']

        label_game_coin['text'] = 'coin : ' + str(game_coin)
        label_game_point['text'] = 'point : ' + str(game_point)
        label_game_spin['text'] = 'spin : ' + str(game_spin)

        gamenumber_entry['state'] = 'disabled'


def cmd_btn_begin_game():
    global game_coin_state

    if game_coin > 0:
        game_coin_state = 1
        btn_begin_game['state'] = 'disabled'
        btn_stop_game['state'] = 'normal'
        game_process_coin()


def cmd_btn_stop_game():
    global game_coin_state
    game_coin_state = 0
    btn_begin_game['state'] = 'normal'
    btn_stop_game['state'] = 'disabled'


def game_process_coin():
    response = api.spend_coin(target_url, active_game_pk, user_token)
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        global game_coin, game_coin_state
        game_coin = res_dict['game_coin']
        label_game_coin['text'] = 'coin : ' + str(game_coin)

        game_event = res_dict['game_event']
        if game_event:
            put_coin_log(game_event)

        if game_coin_state == 1:
            if game_coin > 0:
                root.after(40 * game_speed, game_process_coin)
                rand_coin_time = random.randrange(10, 200)
                root.after(rand_coin_time * game_speed, game_process_coin_result)
            else:
                game_coin_state = 0


def game_process_coin_result():
    result_list = ['spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none',  'spin', 'spin', 'none',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none',  'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'gage', 'spin', 'spin', 'point_2',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'gage', 'spin', 'spin', 'point_2',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'gage', 'spin', 'spin', 'point_2',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'gage', 'spin', 'spin', 'point_2',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'point_1',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'none',
                   'spin', 'spin', 'none', 'spin', 'spin', 'none', 'spin', 'spin', 'gage', 'spin', 'spin', 'point_3',]

    result = random.choice(result_list)

    response = api.coin_result(target_url, active_game_pk, result, user_token )
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        global game_point, game_spin
        game_point  = res_dict['point']
        game_spin   = res_dict['spin_count']

        label_game_point['text'] = 'point : ' + str(game_point)
        label_game_spin['text'] = 'spin : ' + str(game_spin)

        put_coin_log(result)


def begin_spin_watch_thread():
    if game_spin_state == 0:
        if game_spin > 0:
            game_process_begin_spin()

    root.after(5* game_speed,begin_spin_watch_thread)


def game_process_begin_spin():
    response = api.begin_spin(target_url, active_game_pk, user_token )
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        global game_spin
        game_spin = res_dict['spin_count']
        label_game_spin['text'] = 'spin : ' + str(game_spin)

        global game_spin_state
        game_spin_state = 1
        label_spin_state['text'] = '릴 상태 : 스핀'

        if res_dict['prize'] >= 5000:
            root.after(150 * game_speed, game_process_end_spin)
        else:
            root.after(20 * game_speed, game_process_end_spin)

        prize_type    = res_dict['prize_type']
        point   = res_dict['prize']
        reel_event = res_dict['reel_event']

        put_spin_log(prize_type + ' ' + str(point) + ' ' + reel_event)


def game_process_end_spin():
    response = api.end_spin(target_url, active_game_pk, user_token)
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        global game_point
        game_point  = res_dict['point']
        label_game_point['text'] = 'point : ' + str(game_point)

        global game_spin_state
        game_spin_state = 0
        label_spin_state['text'] = '릴 상태 : 대기'


def cmd_btn_point_return():
    response = api.gift_to_point(target_url, active_game_pk, user_token)
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        global game_coin, game_point
        game_coin = res_dict['coin']
        label_game_coin['text'] = 'coin : ' + str(game_coin)
        game_point = res_dict['point']
        label_game_point['text'] = 'point : ' + str(game_point)


def cmd_btn_close_game():
    response = api.close_game(target_url, active_game_pk, user_token)
    res_dict = json.loads(response.text)

    if res_dict['result'] == 'success':
        global user_credit
        user_credit = res_dict['user_credit']
        label_Credit['text'] = 'credit : ' + str(user_credit)

        gamenumber_entry['state'] = 'normal'
        messagebox.showinfo('titan', 'game winlose : ' + str(res_dict['game_winlose']) )
        refresh_gamelist()


def put_coin_log(log):
    if list_coin_log.size() > 30:
        list_coin_log.delete(0, END)

    list_coin_log.insert(0, log)


def put_spin_log(log):
    if list_spin_log.size() > 30:
        list_spin_log.delete(0, END)

    # if log != '0':
    #     list_spin_log.insert(0, log)

    list_spin_log.insert(0, log)


# UI
url_entry = Entry(root, width=30)
url_entry.place(x=10,y=10)
# url_entry.insert(0,"http://titan-admin-eb-env.eba-yyfhid9w.ap-northeast-2.elasticbeanstalk.com")
# url_entry.insert(0,"http://127.0.0.1:8000")
url_entry.insert(0,"http://tit7080.com")


label_ID = Label(root, text="ID ")
label_ID.place( x=10, y=38)
entry_ID = Entry(root,width=20)
entry_ID.place(x=30,y=38)
entry_ID.insert(0,'테스트회원3')

btn_connect = Button(root, width=10, height=1, text="connect", command=cmd_btn_connect)
btn_connect.place(x=220,y=35)


frame_game_list = Frame(root)
scrollbar_game_list = Scrollbar(frame_game_list)
scrollbar_game_list.pack(side='right', fill='y')
list_Games = Listbox(frame_game_list, selectmode='browse', width=40, height=5, yscrollcommand= scrollbar_game_list.set)
list_Games.pack(side='left')
scrollbar_game_list['command'] = list_Games.yview
frame_game_list.place(x=10, y=70)

btn_refresh_game_list = Button(root, width=10, height=1, text="리스트갱신", command=refresh_gamelist )
btn_refresh_game_list.place(x=10,y=160)

btn_create_game = Button(root, width=10, height=1, text="게임만들기", command=cmd_btn_create_game )
btn_create_game.place(x=100,y=160)


gamenumber_entry = Entry(root, width=3)
gamenumber_entry['state'] = 'disabled'
gamenumber_entry.place(x=190, y=164)


btn_resueme_game = Button(root, width=10, height=1, text="게임참가", command=cmd_btn_resume_game )
btn_resueme_game.place(x=220,y=160)


label_Credit = Label(root, text='Credit : ')
label_Credit.place(x=10, y=203)

btn_insert_credit = Button(root, width=10, height=1, text="크레딧 투입", command=cmd_btn_insert_credit )
btn_insert_credit.place(x=120, y=200)



btn_point_return = Button(root, width=10, height=1, text="포인트투입", command=cmd_btn_point_return )
btn_point_return.place(x=220, y=200)


btn_begin_game = Button(root, width=10, height=1, text="게임시작", command=cmd_btn_begin_game )
btn_begin_game.place(x=10, y=240)

btn_stop_game = Button(root, width=10, height=1, text="게임 정지", command=cmd_btn_stop_game, state='disabled' )
btn_stop_game.place(x=100, y=240)


label_game_coin = Label(root, text='coin : ')
label_game_coin.place(x=10,y=280)
label_game_point = Label(root, text='point : ')
label_game_point.place(x=120,y=280)
label_game_spin = Label(root, text='spin : ')
label_game_spin.place(x=240,y=280)


frame_coin_log = Frame(root)
scrollbar_coin_log = Scrollbar(frame_coin_log)
scrollbar_coin_log.pack(side='right', fill='y')
list_coin_log = Listbox(frame_coin_log, selectmode='browse', width=18, height=15, yscrollcommand = scrollbar_coin_log.set)
list_coin_log.pack( side='left')
scrollbar_coin_log['command'] = list_coin_log.yview
frame_coin_log.place(x=10, y=320)

frame_spin_log = Frame(root)
scrollbar_spin_log = Scrollbar(frame_spin_log)
scrollbar_spin_log.pack(side='right', fill='y')
list_spin_log = Listbox(frame_spin_log, selectmode='browse', width=18, height=15, yscrollcommand = scrollbar_spin_log.set)
list_spin_log.pack( side='left')
scrollbar_spin_log['command'] = list_spin_log.yview
frame_spin_log.place(x=160, y=320)

label_spin_state = Label(root, text='릴상태 : ')
label_spin_state.place(x=180, y=565)

btn_close_game = Button(root, width=40, height=1, text="게임종료", command=cmd_btn_close_game )
btn_close_game.place(x=20, y=600)

'''
# scenario test
'''


def cmd_btn_test_prize():
    build_event_scenario(int(prize_entry.get()))


def build_event_scenario(target_prize):
    is_sudden = False

    if target_prize == 0:
        if random.randrange(0, 100) < 10:
            is_sudden = True
    elif target_prize >= 50000:
        if random.randrange(0, 100) < 20:
            is_sudden = True

    if is_sudden:
        scenario = build_event_scenario_sudden(target_prize)
    else:
        scenario = build_event_scenario_step(target_prize)

    prize_scenario = build_prize_scenario(target_prize, scenario['reel_event'])

    cmd_btn_clear_scenario_log()

    for key, val in scenario.items():
        put_scenario_log(key + ' : ' + str(val))

    for key, val in prize_scenario.items():
        put_scenario_log(key + ' : ' + str(val))


def cmd_btn_test_prize_sudden():
    target_prize = int(prize_entry.get())
    scenario = build_event_scenario_sudden(target_prize)
    prize_scenario = build_prize_scenario(target_prize, scenario['reel_event'])

    cmd_btn_clear_scenario_log()

    for key, val in scenario.items():
        put_scenario_log(key + ' : ' + str(val))

    for key, val in prize_scenario.items():
        put_scenario_log(key + ' : ' + str(val))

    # testval = prize_scenario['0']
    # print(testval)
    # prize_list =list(testval.values())
    # print(prize_list[0])


def cmd_btn_test_prize_step():
    target_prize = int(prize_entry.get())
    scenario = build_event_scenario_step(target_prize)
    prize_scenario = build_prize_scenario(target_prize, scenario['reel_event'])

    cmd_btn_clear_scenario_log()

    for key, val in scenario.items():
        put_scenario_log(key + ' : ' + str(val))

    for key, val in prize_scenario.items():
        put_scenario_log(key + ' : ' + str(val))


def build_event_scenario_sudden(target_prize):
    # 0은 잠수함 번개 뻥으로 가야하는데 이건 최소한으로 해야한다. 통계 낼 방법을 생각해봐야겠는데
    scenario = dict()
    scenario['count'] = 0
    scenario['offset'] = 0
    scenario['prize'] = target_prize
    scenario['reel_event'] = 'None'

    target_step    = 0

    if target_prize == 0:
        use_reel_event = True
    elif target_prize >= 500000:
        use_reel_event = False
    else:
        if random.randrange(0, 100) < 50:
            use_reel_event = False
        else:
            use_reel_event = True

    if use_reel_event:
        if random.randrange(0, 100) < 50:
            scenario['reel_event'] = 'submarine'
        else:
            scenario['reel_event'] = 'lightning'
    else:
        if target_prize < 500000:
            target_step = 1
        else:
            target_step = 2

    offset = 0

    use_night = False
    if random.randrange(0, 100) < 50:
        use_night = True

    steps_string_list = ['night', 'shark', 'whale_1', ]
    need_space_dict = {'night': 15, 'shark': 82, 'whale_1': 90}

    steps_long_string_list = ['night', 'shark', 'whale_2']
    need_long_space_dict = {'night': 15, 'shark': 82, 'whale_2': 150}

    if use_night:
        step_string = steps_string_list[0]
        scenario[str(offset)] = step_string
        offset += need_space_dict[step_string]
        offset += random.randrange(16, 32)

    if scenario['reel_event'] == 'None':
        if target_step == 1:
            step_string = steps_string_list[target_step]
            scenario[str(offset)] = step_string
            offset += need_space_dict[step_string]
            offset += random.randrange(3, 5)

        if target_step == 2:
            if target_prize >= 1500000:
                step_string = steps_long_string_list[target_step]
                scenario[str(offset)] = step_string
                offset += need_long_space_dict[step_string]
            elif target_prize >= 1000000:
                if random.randrange(0, 100) < 20:
                    step_string = steps_long_string_list[target_step]
                    scenario[str(offset)] = step_string
                    offset += need_long_space_dict[step_string]
                else:
                    step_string = steps_string_list[target_step]
                    scenario[str(offset)] = step_string
                    offset += need_space_dict[step_string]
            else:
                step_string = steps_string_list[target_step]
                scenario[str(offset)] = step_string
                offset += need_space_dict[step_string]

            offset += random.randrange(3, 5)

    scenario['count'] = offset
    return scenario


def build_event_scenario_step(target_prize):
    scenario = dict()
    scenario['count'] = 0
    scenario['offset'] = 0
    scenario['prize'] = target_prize
    scenario['reel_event'] = 'None'

    if target_prize == 0:
        seed = random.randrange(100)
        if seed < 50:
            target_step = 1
        elif seed < 80:
            target_step = 2
        else:
            target_step = 3
    else:
        if target_prize >= 500000:
            target_step = 5
        elif target_prize >= 100000:
            target_step = 4
        elif target_prize >= 30000:
            target_step = 3
        else:   # 2, 1
            if random.randrange(0, 100) < 80:
                target_step = 2
            else:
                target_step = 1

    steps_string_list = ['night', 'turtle_1', 'jellyfish', 'shark', 'whale_1']
    need_space_dict = {'night': 15, 'turtle_1': 72, 'jellyfish': 130, 'shark': 82, 'whale_1': 90}

    steps_long_string_list = ['night', 'turtle_2', 'jellyfish', 'shark', 'whale_2']
    need_long_space_dict = {'night': 15, 'turtle_2': 110, 'jellyfish': 130, 'shark': 82, 'whale_2': 150}

    current_step = 0
    offset = 0

    while current_step < target_step:
        # skip turtle
        if current_step == 1 and target_step >= 4:
            rand_seed = random.randrange(0, 100)
            if rand_seed < 20:# skip turtle
                offset += random.randrange(10, 20)
                current_step += 1
                continue
            # turtle_2
            elif rand_seed < 50:
                step_string = steps_long_string_list[current_step]
                scenario[str(offset)] = step_string
                offset += need_long_space_dict[step_string]
                offset += random.randrange(10, 20)
                current_step += 1
                continue
        # whale_2
        elif current_step == 4 and target_prize >= 1500000:
            step_string = steps_long_string_list[current_step]
            scenario[str(offset)] = step_string
            offset += need_long_space_dict[step_string]
            offset += random.randrange(10, 20)
            current_step += 1
            continue
        elif current_step == 4 and target_prize >= 1000000:
            if random.randrange(0, 100) < 20:
                step_string = steps_long_string_list[current_step]
                scenario[str(offset)] = step_string
                offset += need_long_space_dict[step_string]
                offset += random.randrange(10, 20)
                current_step += 1
                continue

        step_string = steps_string_list[current_step]
        scenario[str(offset)] = step_string
        offset += need_space_dict[step_string]
        current_step += 1

        if current_step < target_step:  # has next step
            offset += random.randrange(16, 32)
        else:
            offset += random.randrange(3, 5)

    # chain turtle, jellyfish
    if target_prize == 0:
        if target_step == 2 or target_step == 3:
            if random.randrange(0, 100) < 20:
                offset += random.randrange(3, 5)
                step_string = steps_string_list[(target_step-1)]
                scenario[str(offset)] = step_string
                offset += need_space_dict[step_string]
                offset += random.randrange(3, 5)

    scenario['count'] = offset

    return scenario


opening_reel_type_table = (
    (2500000,   'dolphin_center',   5,   20000),    (2000000,   'dolphin_center',   4,   20000),    (1500000,   'dolphin_center',   3,   20000),
    (1000000,   'dolphin_center',   2,   20000),    (1000000,   'dolphin',          4,   20000),    (500000,    'dolphin_center',   1,   20000),
    (500000,    'dolphin',          2,   20000),    (400000,    'bar_center',       4,   20000),    (300000,    'bar_center',       3,   20000),
    (250000,    'bar',              5,   20000),    (250000,    'seven_center',     5,   20000),    (200000,    'bar_center',       2,   20000),
    (200000,    'bar',              4,   20000),    (200000,    'seven_center',     4,   20000),    (150000,    'bar',              3,   20000),
    (150000,    'seven_center',     3,   20000),    (100000,    'bar_center',       1,   20000),    (100000,    'bar',              2,   20000),
    (100000,    'seven_center',     2,   20000),    (100000,    'seven',            4,   20000),    (50000,     'bar',              1,   20000),
    (50000,     'seven_center',     1,   20000),    (50000,     'seven',            2,   20000),    (30000,     'star',             3,   20000),
    (30000,     'target_center',    3,   10000),    (20000,     'star_center',      1,   20000),    (20000,     'star',             2,   20000),
    (20000,     'target_center',    2,   10000),    (10000,     'target_center',    1,   10000),    (10000,     'target',           2,   10000),
)


def build_prize_scenario(target_prize, reel_event):
    prize_scenario = dict()
    prize_scenario['count'] = 0
    prize_scenario['offset'] = 0
    prize_scenario['total_prize'] = target_prize
    prize_scenario['remain_prize'] = target_prize
    prize_scenario['reel_event'] = reel_event
    index = 0

    global opening_reel_type_table

    if target_prize == 0:
        if reel_event != 'None':
            item = random.choice(opening_reel_type_table)
            prize_scenario[str(index)] = {item[1]: 0}
            index += 1

        index += random.randrange(3, 6)
        prize_scenario[str(index)] = {'day': 0}
        prize_scenario['count'] = index
        return prize_scenario

    usable_prize_list = []

    for li in opening_reel_type_table:
        if target_prize == li[0]:
            usable_prize_list.append(li)

    item = random.choice(usable_prize_list)

    prize_scenario[str(index)] = {item[1]: item[3]}

    remain_prize = target_prize
    remain_prize -= item[3]

    index += 1

    clam_string_table = ('not_use', 'clam_0', 'clam_1', 'clam_2', 'clam_3', 'clam_4')
    clam_string = clam_string_table[item[2]]

    for i in range(0,5):
        prize_scenario[str(index)] = {'clam_0': 0}
        index += 1

    clam_insert_index = random.randrange(3, 6)

    if clam_string == 'clam_3':
        clam_prize = 1500
    elif clam_string == 'clam_4':
        clam_prize = 7500
    else:
        clam_prize = 0

    prize_scenario[str(clam_insert_index)] = {clam_string: clam_prize}

    usable_prize_table = [5000, 10000, 20000, 20000, 20000, 20000, 20000]

    while remain_prize > 0:
        prize = random.choice(usable_prize_table)

        if prize != 0 and prize <= remain_prize:
            prize_scenario[str(index)] = {'anything': prize}
            remain_prize -= prize

            if random.randrange(0, 10) < 3:
                index += 2
            else:
                index += 1

    index += random.randrange(3, 6)
    prize_scenario[str(index)] = {'day': 0}
    prize_scenario['count'] = index

    return prize_scenario


prize_entry = Entry(root, width=10)
prize_entry.place(x=320,y=10)
btn_test_prize = Button(root, width=6, height=1, text="build", command=cmd_btn_test_prize )
btn_test_prize.place(x=420, y=10)
btn_test_prize_sudden = Button(root, width=6, height=1, text="sudden", command=cmd_btn_test_prize_sudden )
btn_test_prize_sudden.place(x=480,y=10)
btn_test_prize_step = Button(root, width=6, height=1, text="step", command=cmd_btn_test_prize_step )
btn_test_prize_step.place(x=540,y=10)


frame_scenario_log = Frame(root)
scrollbar_scenario_log = Scrollbar(frame_scenario_log)
scrollbar_scenario_log.pack(side='right', fill='y')
list_scenario_log = Listbox(frame_scenario_log, selectmode='browse', width=25, height=30, yscrollcommand = scrollbar_scenario_log.set)
list_scenario_log.pack( side='left')
scrollbar_scenario_log['command'] = list_scenario_log.yview
frame_scenario_log.place(x=320, y=40)


def cmd_btn_clear_scenario_log():
    list_scenario_log.delete(0, END)


def put_scenario_log(log):
    list_scenario_log.insert(END, log)


btn_clear_scenario_log = Button(root, width=5, height=1, text="c", command=cmd_btn_clear_scenario_log )
btn_clear_scenario_log.place(x=550, y=40)


def cmd_btn_test_scenario():
    result = 0
    count = 0
    cost = 0
    num_games = 10000000

    prize_dict = {'1': 0, '2': 0, '3': 0, '5': 0, '10': 0, '15': 0, '20': 0, '25': 0, '30': 0, '40': 0,
                  '50': 0, '100': 0, '150': 0, '200': 0, '250': 0}
    import pdb
    for i in range(0, num_games):
        prize = build_random_scenario()
        cost += 100

        if prize > 0:
            result += prize
            count += 1

            key = str(int(prize/10000))
            prize_dict[key] += 1

    put_scenario_log(str(num_games/count))
    put_scenario_log(str(count) + " / " + str(result))
    put_scenario_log(str(cost) + " / " + str((result/cost)*100.0))

    for key, val in prize_dict.items() :
        put_scenario_log( key + " : " + str(val) )


btn_test_scenario_log = Button(root, width=5, height=1, text="T", command=cmd_btn_test_scenario )
btn_test_scenario_log.place(x=550, y=80)

prize_table = []

for i in range(0, 10):
    prize_table.append(10000)
for i in range(0, 20):
    prize_table.append(20000)
for i in range(0, 50):
    prize_table.append(30000)
for i in range(0, 80):
    prize_table.append(50000)
for i in range(0, 100):
    prize_table.append(100000)
for i in range(0, 110):
    prize_table.append(150000)
for i in range(0, 120):
    prize_table.append(200000)
for i in range(0, 120):
    prize_table.append(250000)
for i in range(0, 80):
    prize_table.append(300000)
for i in range(0, 50):
    prize_table.append(400000)
for i in range(0, 20):
    prize_table.append(500000)
for i in range(0, 10):
    prize_table.append(1000000)
for i in range(0, 3):
    prize_table.append(1500000)
for i in range(0, 2):
    prize_table.append(2000000)
for i in range(0, 1):
    prize_table.append(2500000)


def build_random_scenario():
    global prize_table

    prize = 0

    if random.randrange(0, 3000) == 77:
        prize = random.choice(prize_table)

    return prize


begin_spin_watch_thread()

root.mainloop()







