import os

from flask import render_template, url_for, redirect, flash, session, jsonify, request, abort
from sqlalchemy import or_

from app import app, db, Config
from app.local import *
from app.forms import LoginForm, SignUpForm, RankSearchForm, ProfileForm, AvatarForm
from app.models import User, Profile, Competition
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

'''@app.route are decorators associating the function and given URL  
'''

# all users online
now_user = []
# waiting users: 0 or 1
player_user = []
# player who is gaming
now_play = []


@app.route('/')
@app.route('/index')
# the page for welcome!
def index():
    # check the state of user, whether a new user or logged in user
    if not session.get('USERNAME') is None:
        return render_template('index.html', title=session.get('USERNAME') + '! Welcome')
    else:
        return render_template('index.html', title='Welcome')


@app.route('/log_on', methods=['GET', 'POST'])
# the page for logging in once they want to login or have just signed in
def log_on():
    form = LoginForm()
    # in case the logged in user wants enter the log on page by typing the URL
    if not session.get('USERNAME') is None:
        flash('You have logged in! If you want to sign in other account, please log out first.')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # to check User and email whether in the db
        user_in_db = User.query.filter_by(username=form.username.data).first()
        email_in_db = User.query.filter_by(email=form.username.data).first()
        if not user_in_db and not email_in_db:
            flash('Wrong Username or Email!!')
            return redirect(url_for('log_on'))
        elif user_in_db and (check_password_hash(user_in_db.password_hash, form.password.data)):
            flash('Login successfully!')
            session['USERNAME'] = user_in_db.username
            session['MODE'] = "light"

            if session['USERNAME'] not in now_user:
                now_user.append(session['USERNAME'])
            else:
                session.pop('play', None)

            return redirect(url_for('index'))
        elif email_in_db and (check_password_hash(email_in_db.password_hash, form.password.data)):
            flash('Login successfully!')
            session['USERNAME'] = email_in_db.username
            session['MODE'] = "light"

            if session['USERNAME'] not in now_user:
                now_user.append(session['USERNAME'])
            else:
                session.pop('play', None)
            return redirect(url_for('index'))
        flash('Wrong Password!!')
        return redirect(url_for('log_on'))
    return render_template('logon.html', title='Sign in', form=form)


@app.route('/register', methods=['post', 'get'])
# the page for registering
def register():
    form = SignUpForm()
    # in case the user wants enter the register page by typing the URL
    if not session.get('USERNAME') is None:
        flash('You have logged in! If you want to sign in other account, please log out first.')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # to check User and email whether in the db
        listE = User.query.filter_by(email=form.emailA.data).first()
        listU = User.query.filter_by(username=form.username.data).first()
        if (listE is None) and (listU is None):
            flash('Complete Registration! Have a login first.')
            passw_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.emailA.data, password_hash=passw_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('log_on'))
        else:
            flash('The username or email already exists.')
    return render_template('register.html', title='Sign up', form=form)


@app.route('/logout')
# the page for log out
def logout():
    if session['USERNAME'] in now_user:
        now_user.remove(session['USERNAME'])
    if session['USERNAME'] in player_user:
        player_user.remove(session['USERNAME'])
    plays = [e for e in now_play if e[1] == session['USERNAME']] + [e for e in now_play if e[0] == session['USERNAME']]
    for e in plays:
        try:
            end_play(e[0], e[1])
            now_play.remove(e)
        except:
            pass
    # session.pop('username', None)
    session.clear()
    # session.pop('USERNAME', None)
    flash('Log out Successfully')
    return redirect('index')


@app.route('/rank', methods=['GET', 'POST'])
# the page for ranking list
def rank():
    # to check User whether in the db
    rankUser = User.query.order_by(db.desc(User.rate)).all()
    myRank = {}

    # the user's own wins, losses, winning percentage and ranking
    if not session.get('USERNAME') is None:
        user = session.get('USERNAME')
        thisUser = User.query.filter_by(username=user).first()
        r = rankUser.index(thisUser) + 1
        ma = [thisUser.win, thisUser.lose, thisUser.draw, thisUser.rate, r]
        myRank[thisUser.username] = ma

    form = RankSearchForm()
    if form.validate_on_submit():
        # target player's wins, losses, winning percentage and ranking
        # targetUser = User.query.filter_by(username = form.search.data).all()
        targetUser = User.query.filter(User.username.like('%' + form.search.data + '%')).order_by(
            db.desc(User.rate)).all()
        target = {}
        for t in targetUser:
            r = rankUser.index(t) + 1
            ta = [t.win, t.lose, t.draw, t.rate, r]
            target[t.username] = ta
        return render_template('search.html', title='Search', target=target, myRank=myRank, form=form)

    # top player's wins, losses, winning percentage and ranking
    topUser = User.query.order_by(db.desc(User.rate)).limit(10)
    top = {}
    r = 1
    for t in topUser:
        ta = [t.win, t.lose, t.draw, t.rate, r]
        top[t.username] = ta
        r = r + 1

    return render_template('rank.html', title='Rank', top=top, myRank=myRank, form=form)


@app.route('/introduction')
# the page for introduction
def intro():
    return render_template('intro.html', title='Introduction')


# refer to flask_chess on github by Kechi Zhang
@app.route('/local')
# the page for local mode
def local():
    init_chesses("Player1", "Player2")

    u = "Player2"
    p = "Player1"
    color = get_color(u, p, u)
    if color == 'black':
        color_msg = 'Black First'
        oc_msg = 'White Second'
    elif color == 'white':
        color_msg = 'White Second'
        oc_msg = 'Black First'
    else:
        color_msg = 'Server Error'
        oc_msg = 'Server Error'
    return render_template("local.html", msg=p + "<br>" + oc_msg, message=u + "<br>" + color_msg, title='local mode')


@app.route('/online')
# the page for online mode
def online():
    # in case the unlogged in user wants enter the online page
    if not session.get('USERNAME') is None:
        return redirect(url_for('play_index'))
    else:
        flash('You haven\'t logged in! If you want to play the online mode, please sign in first!')
        return redirect(url_for('index'))


@app.route("/play")
# for online mode matching page with matching button
def play_index():
    user = session['USERNAME']

    playMsg = '''
	<a href="/findPlayer"><input type='button' value='Begin to match!'><a>
	'''

    if 'play' in session:
        playMsg = ''
    print(session)

    return render_template("play.html", pendingjs='', startFindPlayer=playMsg, title='Match')


@app.route('/findPlayer')
# for online mode matching process
def findPlayer():
    # no other player waiting
    if len(player_user) == 0:
        player_user.append(session['USERNAME'])
        pendingjs = '''
		<script type="text/javascript">

		function getPlayer(){
			$.get("/getPair",function(rtnFromSvr){
				if (rtnFromSvr.length == 0)
					$("#pending").html("Matching...");
				else
					window.location.replace("/chessPlay")
				// $("#nowUser").html("There are " + rtnFromSvr + " players now.");
				console.log(rtnFromSvr);
			});
		}
		setInterval("getPlayer()",1000);
		</script>
		'''
        return render_template("play.html", pendingjs=pendingjs, title='Play')
    # already have waiting player
    else:
        player = player_user.pop()
        now_play.append((player, session['USERNAME']))
        session['play'] = player
        init_chesses(player, session['USERNAME'])

        return redirect(url_for("chessPlay"))


@app.route('/getNowUser')
# for get now user
def getNowUser():
    return str(len(now_user))


@app.route('/getPair')
# for get pair
def getPair():
    if session['USERNAME'] not in player_user:
        plays = [e[0] for e in now_play if e[1] == session['USERNAME']] + [e[1] for e in now_play if
                                                                           e[0] == session['USERNAME']]
        other = plays[0]
        session['play'] = other
        return other
    else:
        return ""


@app.route('/chessPlay')
# show players' information
def chessPlay():
    # u self, p other
    u, p = get_players(session)
    color = get_color(u, p, u)
    # differentiate me and the opponent
    if color == 'black':
        color_msg = 'Black First'
        oc_msg = 'White Second'
    elif color == 'white':
        color_msg = 'White Second'
        oc_msg = 'Black First'
    else:
        color_msg = 'Server Error'
        oc_msg = 'Server Error'
    users_in_db = User.query.filter(or_(User.username == u, User.username == p)).all()
    profile = []
    if users_in_db:
        for user in users_in_db:
            pro = Profile.query.filter(Profile.user_id == user.id).first()
            if not pro:
                pro = Profile(profile_photo='/static/uploaded_photo/default.jpg',
                              gender='Unknown',
                              intro='This player is lazy. Doesn\'t have aboutme.')
            else:
                # in case no photo
                if pro.profile_photo == '':
                    pro.profile_photo = '/static/uploaded_photo/default.jpg'
                # since they can delete intro
                if pro.intro == '':
                    pro.intro = 'This player is lazy. Doesn\'t have aboutme.'
            profile.append(pro)
    return render_template("chess.html", msg="Opponent：" + p + "<br>" + oc_msg,
                           message="Myself：" + u + "<br>" + color_msg, users=users_in_db,
                           profile=profile, title='Online Mode')


@app.route('/getColor')
def getColor():
    u, p = get_players(session)
    return get_color(u, p, u)


@app.route('/play_chess')
# get the id of the chess and return
def play_chess():
    xy = request.args['xy']
    print("xy: " + xy)
    print(chesses)
    u, p = get_players(session)
    rst = try_play(u, p, u, xy)
    print(rst)
    return rst


@app.route('/get_chess')
def get_chess():
    u, p = get_players(session)
    return get_new_play(u, p, u)


@app.route('/get_all_black_chess')
def get_all_black_chess():
    u, p = get_players(session)
    return get_all_play(u, p, 'black')


@app.route('/get_all_white_chess')
def get_all_white_chess():
    u, p = get_players(session)
    return get_all_play(u, p, 'white')


@app.route('/end_chess')
# end the play and save information in database
def end_chess():
    # u,p = get_players(session)
    result = request.args['play_rst']
    print("result: " + result)
    # for this user
    user = session.get('USERNAME')
    thisUser = User.query.filter_by(username=user).first()
    uid = thisUser.id
    win = thisUser.win
    lose = thisUser.lose
    draw = thisUser.draw
    print("uid: ")
    print(uid)
    print(win)
    print(lose)
    print(draw)
    # for the opponent
    oppo = session.get('play')
    oppoUser = User.query.filter_by(username=oppo).first()
    ouid = oppoUser.id
    owin = oppoUser.win
    olose = oppoUser.lose
    odraw = oppoUser.draw
    if result == "1":
        re = "win"
        ore = "lose"
        win = win + 1
        olose = olose + 1
        print("win: ")
        print(win)
    elif result == "2":
        re = "lose"
        ore = "win"
        lose = lose + 1
        owin = owin + 1
        print("lose: ")
        print(lose)
    rate = win / (win + lose + draw)
    orate = owin / (owin + olose + odraw)
    print("rate: ")
    print(rate)
    thisUser.win = win
    thisUser.lose = lose
    thisUser.draw = draw
    thisUser.rate = rate
    db.session.commit()
    oppoUser.win = owin
    oppoUser.lose = olose
    oppoUser.draw = odraw
    oppoUser.rate = orate
    db.session.commit()
    # for the competition
    com = Competition.query.count()
    cid = (com // 2) + 1
    dt = datetime.utcnow()
    nc = Competition(id=cid, user_id=uid, result=re, timestamp=dt)
    db.session.add(nc)
    db.session.commit()
    onc = Competition(id=cid, user_id=ouid, result=ore, timestamp=dt)
    db.session.add(onc)
    db.session.commit()
    # end play
    plays = [e for e in now_play if e[1] == session['USERNAME']] + [e for e in now_play if e[0] == session['USERNAME']]
    for e in plays:
        try:
            end_play(e[0], e[1])
            now_play.remove(e)
        except:
            pass
    if 'play' in session:
        session.pop('play', None)
    return '1'


@app.route('/leave')
def leave():
    plays = [e for e in now_play if e[1] == session['USERNAME']] + [e for e in now_play if e[0] == session['USERNAME']]
    for e in plays:
        try:
            end_play(e[0], e[1])
            now_play.remove(e)
        except:
            pass
    if 'play' in session:
        session.pop('play', None)
    return '1'


@app.route('/CheckTurn')
# decide turn
def CheckTurn():
    print("debug")
    u, p = get_players(session)
    color = get_now_color(u, p, u)
    msg = ''
    tu = ''
    if color == '':
        return ''
    elif color == 'black':
        msg += 'Now：Black'

    else:
        msg += 'Now：White'

    if color == get_color(u, p, u):
        msg += '<br>It is your turn'
        tu = '0'
    else:
        msg += '<br>Please wait'
        tu = '1'

    return {"msg": msg, "tu": tu}


@app.route('/profile')
# the page for personal space; idea from lecture 9 DB 3
def profile():
    # in case the unlogged in user wants enter the personal space
    name = session.get('USERNAME')
    if name is None:
        flash('You haven\'t logged in! Please sign in first!')
        return redirect(url_for('index'))

    # db part
    avatar = None
    user_in_db = User.query.filter(User.username == name).first()

    stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
    # if have data, put them into it
    if not stored_profile:
        stored_profile = Profile(gender='Unknown')
    elif not stored_profile.profile_photo is None:
        # in case the user has information but doesn't have avatar
        avatar = stored_profile.profile_photo

    return render_template('profile.html', title=name + "'s Personal Zone",
                           avatar=avatar, profile=stored_profile, user=user_in_db)


@app.route('/edit', methods=['GET', 'POST'])
# the page for editing personal space; idea from lecture 9 DB 3
def edit():
    # in case the unlogged in user wants enter the personal space
    name = session.get('USERNAME')
    if name is None:
        flash('You haven\'t logged in! If you want to play the online mode, please sign in first!')
        return redirect(url_for('index'))

    aForm = AvatarForm()
    # for Avatar update
    if aForm.validate_on_submit():
        # file
        profile_dir = Config.PROFILE_PHOTO_DIR
        file_obj = aForm.photo.data
        # get the file type
        photo_filename = session.get('USERNAME') + '_Avatar.' + file_obj.filename.split('.')[-1]
        # save
        file_obj.save(os.path.join(profile_dir, photo_filename))
        # change to the static path
        photo_filename = "/static/uploaded_photo/" + photo_filename

        # db part
        user_in_db = User.query.filter(User.username == name).first()

        stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
        # if have data, put them into it
        if not stored_profile:
            # the new object the user should have
            profile = Profile(profile_photo=photo_filename, user=user_in_db)
            db.session.add(profile)
        else:
            stored_profile.profile_photo = photo_filename
        db.session.commit()
        flash("Update avatar Successfully!")
        return redirect(url_for('edit'))

    form = ProfileForm()
    # for basic information upload
    if form.validate_on_submit():
        # db part
        user_in_db = User.query.filter(User.username == name).first()
        stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
        # if have data, put them into it
        if not stored_profile:
            # the new object the user should have
            profile = Profile(gender=form.gender.data, intro=form.intro.data,
                              user=user_in_db)
            db.session.add(profile)
            flash("Create profile Successfully!")
        else:
            stored_profile.gender = form.gender.data
            stored_profile.intro = form.intro.data
            flash("Update Successfully!")
            print(stored_profile.id)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        avatar = None
        user_in_db = User.query.filter(User.username == name).first()
        stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
        # if have data, put them into it
        if stored_profile:
            form.gender.data = stored_profile.gender
            form.intro.data = stored_profile.intro
            # in case the user has information but doesn't have avatar
            if not stored_profile.profile_photo is None:
                avatar = stored_profile.profile_photo
        return render_template('edit.html', title="Edit " + name + "'s Personal Zone",
                               aForm=aForm, form=form, avatar=avatar)


## Used for AJAX api

# get records
@app.route('/api/get_records', methods=['POST'])
def get_records():
    name = request.form['name']
    user_in_db = User.query.filter(User.username == name).first()
    if user_in_db:
        # get the competition of player
        record = Competition.query.filter(Competition.user_id == user_in_db.id).all()
        records = []
        # get his each competition component info
        for r in record:
            records.extend(Competition.query.filter(Competition.id == r.id, Competition.user_id != r.user_id).all())
        all = []
        all.append({'returnValue': 200})
        all.append([])
        for r in records:
            # username is in the User
            name = User.query.filter(User.id == r.user_id).first().username
            all[1].append(prepare_for_json_with_name(r, name))
        return jsonify(all)
    else:
        return jsonify(all.append({'returnValue': 304}))


# get information of users in rank
@app.route('/api/get_info', methods=['POST'])
def get_info():
    name = request.form['name']
    user_in_db = User.query.filter(User.username == name).first()
    # get the profile of player
    profile = Profile.query.filter(Profile.user_id == user_in_db.id).first()
    if user_in_db and profile:
        # in case no photo
        if profile.profile_photo == '':
            profile.profile_photo = '/static/uploaded_photo/default.jpg'
        # since they can delete intro
        if profile.intro == '':
            profile.intro = 'This player is lazy. Doesn\'t have aboutme.'
        info = prepare_for_json(profile)
        all = {'info': info, 'returnValue': 200}
        return jsonify(all)
    elif not profile:
        profile = Profile(profile_photo='/static/uploaded_photo/default.jpg',
                          gender='Unknown',
                          intro='This player is lazy. Doesn\'t have aboutme.')
        info = prepare_for_json(profile)
        all = {'info': info, 'returnValue': 200}
        return jsonify(all)
    else:
        all = {'info': None, 'returnValue': 304}
        return jsonify(all)


# for profile
def prepare_for_json_with_name(item, name):
    result = 'lose'
    if item.result == 'lose':
        result = 'win'
    record = {'id': item.id,
              'name': name,
              'result': result,
              'time': item.timestamp}
    return record


# for rank
def prepare_for_json(item):
    record = {'photo': item.profile_photo,
              'gender': item.gender,
              'intro': item.intro}
    return record


# for local mode
@app.route('/getColorl')
def getColorl():
    u, p = get_local_players()
    return get_color(u, p, u)


@app.route('/play_chessl')
def play_chessl():
    xy = request.args['xy']
    print("xy: " + xy)
    print(chesses)
    u, p = get_local_players()
    rst = try_play(u, p, u, xy)
    print(rst)
    change_player()
    return rst


@app.route('/get_chessl')
def get_chessl():
    u, p = get_local_players()
    return get_new_play(u, p, u)


@app.route('/get_all_black_chessl')
def get_all_black_chessl():
    u, p = get_local_players()
    return get_all_play(u, p, 'black')


@app.route('/get_all_white_chessl')
def get_all_white_chessl():
    u, p = get_local_players()
    return get_all_play(u, p, 'white')


@app.route('/end_chessl')
def end_chessl():
    # u,p = get_players(session)

    try:
        end_play("Player1", "Player2")
    except:
        pass
    return '1'


@app.route('/CheckTurnl')
def CheckTurnl():
    print("debug")
    u, p = get_local_players()
    color = get_now_color(u, p, u)
    msg = ''
    tu = ''
    if color == '':
        return ''
    elif color == 'black':
        msg += 'Now：Black'

    else:
        msg += 'Now：White'

    return {"msg": msg, "tu": tu}


# for change dark and light mode
@app.route('/get_mode')
def get_mode():
    if session.get('MODE') is None:
        session['MODE'] = 'light'
    return session.get('MODE')


@app.route('/remember_mode')
def remember_mode():
    mo = request.args['mo']
    if mo == "body":
        mode = "light"
    elif mo == "body_dark":
        mode = "dark"
    session['MODE'] = mode
    return "1"
