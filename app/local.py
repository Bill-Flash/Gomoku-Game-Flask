# refer to flask_chess on github by Kechi Zhang
chesses = {}
local = ["Player1", "Player2", "Player1"]

def init_chesses(player1,player2):
    chess = {'black':player1,'white':player2,'record':{'black':[],'white':[]},'now':'black'}
    chesses[(player1,player2)] = chess

# process of play chess
def try_play(player1,player2,player,xy):
    pair = (player1,player2)
    if pair not in chesses:
        pair = (player2,player1)
    print("pair: ")
    print(pair)
    print(pair in chesses)
    if pair not in chesses:
        print("not in : -1")
        return "-1"

    color = 'white'
    if chesses[pair]['black'] == player:
        color = 'black'

    if chesses[pair]['now'] == color:
        chesses[pair]['record'][color].append(xy)
        if color == 'white':
            chesses[pair]['now'] = 'black'
        else:
            chesses[pair]['now'] = 'white'
        print("wzq: 1")
        return "1"
    else:
        print("wzq: 0")
        return "0"

def end_play(player1,player2):
    pair = (player1,player2)
    if pair not in chesses:
        pair = (player2,player1)
    if pair in chesses:
        chesses.pop(pair)
    return "1"

def get_color(player1,player2,p):
    pair = (player1,player2)
    if pair not in chesses:
        pair = (player2,player1)
    if pair not in chesses:
        return ''
    else:
        if chesses[pair]['black'] == p:
            return 'black'
        else:
            return 'white'

def get_players(s):
    u = ''
    p = ''
    try:
        u = s['USERNAME']
        p = s['play']
    except:
        pass
    return u,p

# for local mode
def get_local_players():
    u = ''
    p = ''
    try:
        # u = s['USERNAME']
        # p = s['play']
        u = local[1]
        p = local[0]
    except:
        pass
    return u,p

def get_new_play(player1,player2,player):
    pair = (player1,player2)
    if pair not in chesses:
        pair = (player2,player1)
    if pair not in chesses:
        return "-2"

    color = 'white'
    anti_color = 'black'
    if chesses[pair]['black'] == player:
        color = 'black'
        anti_color = 'white'

    if chesses[pair]['now'] == anti_color:
        return "-1"
    elif len(chesses[pair]['record'][anti_color]) == 0:
        return ""
    else:
        return str(chesses[pair]['record'][anti_color][-1])

def get_all_play(player1,player2,c):
    pair = (player1,player2)
    if pair not in chesses:
        pair = (player2,player1)
    if pair not in chesses:
        return "-2"

    return str(chesses[pair]['record'][c]).replace('[','').replace(']','')


def get_now_color(player1,player2,p):
    pair = (player1,player2)
    if pair not in chesses:
        pair = (player2,player1)
    if pair not in chesses:
        return ''
    else:
        return chesses[pair]['now']

# for local mode
def change_player():
    local[2] = local[0]
    local[0] = local[1]
    local[1] = local[2]