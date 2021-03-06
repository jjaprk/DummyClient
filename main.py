import copy
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
    response = api.create_game(target_url, gamecost_variable.get(), user_token)
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
entry_ID.insert(0,'테스트회원2')

btn_connect = Button(root, width=10, height=1, text="connect", command=cmd_btn_connect)
btn_connect.place(x=220,y=35)


frame_game_list = Frame(root)
scrollbar_game_list = Scrollbar(frame_game_list)
scrollbar_game_list.pack(side='right', fill='y')
list_Games = Listbox(frame_game_list, selectmode='browse', width=40, height=5, yscrollcommand= scrollbar_game_list.set)
list_Games.pack(side='left')
scrollbar_game_list['command'] = list_Games.yview
frame_game_list.place(x=10, y=70)

# btn_refresh_game_list = Button(root, width=10, height=1, text="리스트갱신", command=refresh_gamelist )
# btn_refresh_game_list.place(x=10,y=160)
game_cost_list = ['100', '200', '400', '800']

gamecost_variable = StringVar(root)
gamecost_variable.set(game_cost_list[0])

Dropdown_cost = OptionMenu(root, gamecost_variable, *game_cost_list)
Dropdown_cost.place(x=10, y=160)

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
    build_event_scenario(int(prize_entry.get()), int(gamecost_variable.get()))


def build_event_scenario(target_prize, game_cost):
    is_sudden = False

    if target_prize == 0:
        if random.randrange(0, 100) < 5:
            is_sudden = True
    elif target_prize >= (1000 * game_cost):
        if random.randrange(0, 100) < 20:
            is_sudden = True

    if is_sudden:
        scenario = build_event_scenario_sudden(target_prize, game_cost)
    else:
        scenario = build_event_scenario_step(target_prize, game_cost)

    prize_scenario = build_prize_scenario(target_prize, int(gamecost_variable.get()), scenario['reel_event'])

    cmd_btn_clear_scenario_log()

    for key, val in scenario.items():
        put_scenario_log(key + ' : ' + str(val))

    for key, val in prize_scenario.items():
        put_scenario_log(key + ' : ' + str(val))


def cmd_btn_test_prize_sudden():
    target_prize = int(prize_entry.get())
    scenario = build_event_scenario_sudden(target_prize, int(gamecost_variable.get()))
    prize_scenario = build_prize_scenario(target_prize, int(gamecost_variable.get()), scenario['reel_event'])

    cmd_btn_clear_scenario_log()

    for key, val in scenario.items():
        put_scenario_log(key + ' : ' + str(val))

    for key, val in prize_scenario.items():
        put_scenario_log(key + ' : ' + str(val))


def cmd_btn_test_prize_step():
    target_prize = int(prize_entry.get())
    scenario = build_event_scenario_step(target_prize, int(gamecost_variable.get()))
    prize_scenario = build_prize_scenario(target_prize, int(gamecost_variable.get()), scenario['reel_event'])

    cmd_btn_clear_scenario_log()

    for key, val in scenario.items():
        put_scenario_log(key + ' : ' + str(val))

    for key, val in prize_scenario.items():
        put_scenario_log(key + ' : ' + str(val))


event_scenario_steps_game_count = {
    'night': 5, 'turtle_1': 26, 'turtle_2': 50, 'turtle_3': 82,
    'jellyfish_1': 36, 'jellyfish_2': 72, 'jellyfish_3': 106,
    'shark': 25, 'whale_1': 42, 'whale_2': 95
}


def build_event_scenario_sudden(target_prize, game_cost):
    scenario = dict()
    scenario['count'] = 0
    scenario['offset'] = 0
    scenario['prize'] = target_prize
    scenario['reel_event'] = 'None'

    target_step    = 0

    if target_prize == 0:
        use_reel_event = True
    elif target_prize >= (5000 * game_cost):
        use_reel_event = False
    elif target_prize <= (1000 * game_cost):
        use_reel_event = True
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
        if target_prize < (5000 * game_cost):
            target_step = 1
        else:
            target_step = 2

    offset = 0

    use_night = False
    if random.randrange(0, 100) < 70:
        use_night = True

    if use_night:
        scenario[str(offset)] = 'night'
        offset += event_scenario_steps_game_count['night']
        offset += (20 + random.randrange(0, 20))

    if scenario['reel_event'] == 'None':
        if target_step == 1:
            scenario[str(offset)] = 'shark'
            offset += event_scenario_steps_game_count['shark']
            offset += 2

        if target_step == 2:
            if target_prize >= (15000 * game_cost):
                step_string = 'whale_2'
            else:
                step_string = 'whale_1'

            scenario[str(offset)] = step_string
            offset += event_scenario_steps_game_count[step_string]
            offset += 2

    scenario['count'] = offset
    return scenario


event_scenario_steps_table = [
    [0, 'night'],
    [0, 'night'],
    [0, 'night'],
    [0, 'night'],
    [0, 'night', 'turtle_1'],
    [0, 'night', 'turtle_1'],
    [0, 'night', 'turtle_1', 'jellyfish_1'],

    [10000, 'night', 'turtle_1'],
    [10000, 'night', 'turtle_2'],
    [20000, 'night', 'turtle_2'],
    [30000, 'night', 'turtle_2'],
    [30000, 'night', 'turtle_3'],

    [50000, 'night', 'turtle_3'],
    [50000, 'night', 'turtle_2', 'jellyfish_2'],

    [100000, 'night', 'turtle_3', 'jellyfish_2'],

    [150000, 'night', 'turtle_3', 'jellyfish_3'],
    [150000, 'night', 'turtle_1', 'jellyfish_1', 'shark'],
    [200000, 'night', 'turtle_1', 'jellyfish_1', 'shark'],
    [200000, 'night', 'turtle_2', 'jellyfish_2', 'shark'],
    [200000, 'night', 'turtle_3', 'jellyfish_1', 'shark'],
    [250000, 'night', 'turtle_1', 'jellyfish_1', 'shark'],
    [250000, 'night', 'turtle_1', 'jellyfish_3', 'shark'],
    [300000, 'night', 'turtle_3', 'jellyfish_2', 'shark'],
    [400000, 'night', 'turtle_3', 'jellyfish_3', 'shark'],

    [500000, 'night', 'turtle_1', 'jellyfish_1', 'shark', 'whale_1'],
    [500000, 'night', 'turtle_1', 'jellyfish_1', 'shark', 'whale_1'],
    [1000000, 'night', 'turtle_1', 'jellyfish_1', 'shark', 'whale_1'],
    [1000000, 'night', 'turtle_1', 'jellyfish_1', 'shark', 'whale_1'],
    [1500000, 'night', 'turtle_1', 'jellyfish_1', 'shark', 'whale_2'],

    [1000000, 'night', 'turtle_2', 'jellyfish_2', 'shark', 'whale_1'],
    [1500000, 'night', 'turtle_2', 'jellyfish_2', 'shark', 'whale_2'],
    [2000000, 'night', 'turtle_2', 'jellyfish_2', 'shark', 'whale_2'],

    [1500000, 'night', 'turtle_3', 'jellyfish_2', 'shark', 'whale_2'],
    [2000000, 'night', 'turtle_3', 'jellyfish_2', 'shark', 'whale_2'],
    [2500000, 'night', 'turtle_3', 'jellyfish_2', 'shark', 'whale_2'],

    [1500000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [1500000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2000000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2000000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2000000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2000000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2500000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2500000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2500000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
    [2500000, 'night', 'turtle_3', 'jellyfish_3', 'shark', 'whale_2'],
]


def build_event_scenario_step(target_prize, game_cost):
    scenario = dict()
    scenario['count'] = 0
    scenario['offset'] = 0
    scenario['prize'] = target_prize
    scenario['reel_event'] = 'None'

    # choice event scenario
    scenario_prize = int((target_prize / game_cost)*100)

    event_script_list = None

    random.seed(a=None)
    while event_script_list is None:
        event = random.choice(event_scenario_steps_table)

        if event[0] == scenario_prize:
            event_script_list = event.copy()
            event_script_list.pop(0)
            break

    offset = 0

    for step in event_script_list:
        # skip turtles
        if step in ['turtle_1', 'turtle_2', 'turtle_3']:
            if scenario_prize >= 500000 and random.randrange(0, 100) < 30:
                continue
            elif scenario_prize >= 300000 and random.randrange(0, 100) < 20:
                continue
            elif scenario_prize >= 100000 and random.randrange(0, 100) < 10:
                continue

        scenario[str(offset)] = step
        offset += event_scenario_steps_game_count[step]

        if step in ['whale_1', 'whale_2']:
            offset += 2
        else:
            offset += (20 + random.randrange(0, 20))

    scenario['count'] = offset

    return scenario


opening_reel_type_table_origin = [
    [25000,   'dolphin_center',   5,   200],    [20000,   'dolphin_center',   4,   200],    [15000,   'dolphin_center',   3,   200],
    [10000,   'dolphin_center',   2,   200],    [10000,   'dolphin',          4,   200],    [5000,    'dolphin_center',   1,   200],
    [5000,    'dolphin',          2,   200],    [4000,    'bar_center',       4,   200],    [3000,    'bar_center',       3,   200],
    [2500,    'bar',              5,   200],    [2500,    'seven_center',     5,   200],    [2000,    'bar_center',       2,   200],
    [2000,    'bar',              4,   200],    [2000,    'seven_center',     4,   200],    [1500,    'bar',              3,   200],
    [1500,    'seven_center',     3,   200],    [1000,    'bar_center',       1,   200],    [1000,    'bar',              2,   200],
    [1000,    'seven_center',     2,   200],    [1000,    'seven',            4,   200],    [500,     'bar',              1,   200],
    [500,     'seven_center',     1,   200],    [500,     'seven',            2,   200],    [300,     'star',             3,   200],
    [300,     'target_center',    3,   100],    [200,     'star_center',      1,   200],    [200,     'star',             2,   200],
    [200,     'target_center',    2,   100],    [100,     'target_center',    1,   100],    [100,     'target',           2,   100],
]


def build_prize_scenario(target_prize, game_cost, reel_event):
    global opening_reel_type_table_origin

    opening_reel_type_table = copy.deepcopy(opening_reel_type_table_origin)

    for item in opening_reel_type_table:
        item[0] *= game_cost
        item[3] *= game_cost

    prize_scenario = dict()
    prize_scenario['count'] = 0
    prize_scenario['offset'] = 0
    prize_scenario['total_prize'] = target_prize
    prize_scenario['remain_prize'] = target_prize
    prize_scenario['reel_event'] = reel_event
    index = 0

    if target_prize == 0:
        if reel_event != 'None':
            item = opening_reel_type_table[random.randrange(6, 20)]
            prize_scenario[str(index)] = {item[1]: 0}
            index += 1

        index += 1
        prize_scenario[str(index)] = {'day': 0}
        prize_scenario['count'] = (index + 1)
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
        clam_prize = (15 * game_cost)
    elif clam_string == 'clam_4':
        clam_prize = (75 * game_cost)
    else:
        clam_prize = 0

    prize_scenario[str(clam_insert_index)] = {clam_string: clam_prize}

    usable_prize_table = [50, 100, 200, 200, 200, 200, 200]

    for i in range(0, len(usable_prize_table)):
        usable_prize_table[i] *= game_cost

    while remain_prize > 0:
        prize = random.choice(usable_prize_table)

        if prize != 0 and prize <= remain_prize:
            prize_scenario[str(index)] = {'anything': prize}
            remain_prize -= prize

            if random.randrange(0, 10) < 2:
                index += 2
            else:
                index += 1

    index += 2
    prize_scenario[str(index)] = {'day': 0}
    prize_scenario['count'] = (index+1)

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

    prize_dict = dict()
    game_cost = int(gamecost_variable.get())

    for i in range(0, num_games):
        prize = build_random_scenario(game_cost)
        cost += game_cost

        if prize > 0:
            result += prize
            count += 1

            key = str(int(prize/10000))
            if key in prize_dict:
                prize_dict[key] = (prize_dict[key] + 1)
            else:
                prize_dict[key] = 1

    put_scenario_log(str(num_games/count))
    put_scenario_log(str(count) + " / " + str(result))
    put_scenario_log(str(cost) + " / " + str((result/cost)*100.0))

    prize_list = list()
    for key, val in prize_dict.items():
        prize_list.append((int(key), val))

    prize_list.sort()
    # sort_dict = sorted( prize_dict.items())

    for item in prize_list:
        put_scenario_log(str(item[0]) + " : " + str(item[1]) )


btn_test_scenario_log = Button(root, width=5, height=1, text="T", command=cmd_btn_test_scenario )
btn_test_scenario_log.place(x=550, y=80)


scenario_common_prize_table = []

for i in range(0, 800):
    scenario_common_prize_table.append(1)
for i in range(0, 400):
    scenario_common_prize_table.append(2)
for i in range(0, 80):
    scenario_common_prize_table.append(3)
for i in range(0, 40):
    scenario_common_prize_table.append(4)
for i in range(0, 20):
    scenario_common_prize_table.append(5)
for i in range(0, 5):
    scenario_common_prize_table.append(10)
for i in range(0, 4):
    scenario_common_prize_table.append(15)
for i in range(0, 3):
    scenario_common_prize_table.append(20)
for i in range(0, 2):
    scenario_common_prize_table.append(25)
for i in range(0, 1):
    scenario_common_prize_table.append(30)


def getCommonPrize(game_cost):
    global scenario_common_prize_table

    prize = {'anything': 0}

    if random.randrange(0, 101) > 91:
        prize['anything'] = (random.choice(scenario_common_prize_table) * game_cost)

    return prize


def cmd_btn_test_common_prize():
    result = 0
    count = 0
    cost = 0
    num_games = 10000000

    game_cost = int(gamecost_variable.get())

    for i in range(0, num_games):
        prize = getCommonPrize(game_cost)['anything']
        cost += game_cost

        if prize > 0:
            result += prize
            count += 1

    put_scenario_log(str(num_games/count))
    put_scenario_log(str(count) + " / " + str(result))
    put_scenario_log(str(cost) + " / " + str((result/cost)*100.0))


btn_test_common_prize_log = Button(root, width=5, height=1, text="CP", command=cmd_btn_test_common_prize )
btn_test_common_prize_log.place(x=550, y=130)

prize_table = []

for i in range(0, 100):
    prize_table.append(100)
for i in range(0, 200):
    prize_table.append(200)
for i in range(0, 500):
    prize_table.append(300)
for i in range(0, 800):
    prize_table.append(500)
for i in range(0, 500):
    prize_table.append(1000)
for i in range(0, 350):
    prize_table.append(1500)
for i in range(0, 250):
    prize_table.append(2000)
for i in range(0, 120):
    prize_table.append(2500)
for i in range(0, 100):
    prize_table.append(3000)
for i in range(0, 60):
    prize_table.append(4000)
for i in range(0, 40):
    prize_table.append(5000)
for i in range(0, 8):
    prize_table.append(10000)
for i in range(0, 3):
    prize_table.append(15000)
# for i in range(0, 2):
#     prize_table.append(20000)
# for i in range(0, 1):
#     prize_table.append(25000)


def build_random_scenario(game_cost):
    global prize_table

    prize = 0

    if random.randrange(0, 1000) == 77:
        prize = random.choice(prize_table)

    return prize * game_cost


begin_spin_watch_thread()

root.mainloop()







