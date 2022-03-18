import random
import os
import time
import shelve
import datetime as dt
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, RadioField
from wtforms import validators



NUM_CHARTS_INSTR = 2
NUM_CHARTS_TASK = 1
NUM_CHARTS_BETWEEN_BREAKS = 0
ERRORS_ALLOWED_INSTR = 4
ERROR_NO_TERMS_ACCEPTED = "You must accept the terms of the study to continue"
ERROR_DEMO_SURVEY = "Please, fill in the survey again answering all the questions. Make sure that you introduce a valid age and a valid display size (if you know it)"
ERROR_NO_OPTION = "Please, select a value for both Num of Clusters and Value"
ERROR_VALUES = "Please, introduce a number for both Num of Clusters and Value in the range [0, 100]."
ERROR_EVAL_SURVEY = "Please, fill in the survey again answering at least the three first questions."

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///respostes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'la contrassenya es un parametre secret'
db = SQLAlchemy(app)

class AnswersData(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    date                = db.Column(db.String(32))      # '2017-05-10'
    time                = db.Column(db.String(32))      # '08:12:47.292000'
    user                = db.Column(db.Integer)         # User id -->> FALTA get this from the url parameters
    task                = db.Column(db.String(255))     # Task being performed
    age                 = db.Column(db.Integer)         # Age
    gender              = db.Column(db.String(255))     # Gender
    education           = db.Column(db.String(255))     # Education level
    eyesight            = db.Column(db.String(255))     # Eyesight
    display             = db.Column(db.String(32))      # Inches of the display
    understood          = db.Column(db.String(32))      # Understanding
    easiness            = db.Column(db.String(32))      # Easiness of the tasks
    satisfied           = db.Column(db.String(32))      # Satisfaction on the time spent
    comments            = db.Column(db.String(1000))    # Additional comments
    chart               = db.Column(db.String(255))     # Image shown
    A_num_clust         = db.Column(db.Integer)         # Task A: Number of Clusters in the Chart
    A_ANS_num_clus      = db.Column(db.Integer)         # Task A: number of Clusters ANSWERED
    B_value_marker      = db.Column(db.Integer)         # B: Value of the marked cell
    B_ANS_value_marker  = db.Column(db.Integer)         # B: Value ANSWERED
    #FALTA --> rgb_color???
    C_value_to_click    = db.Column(db.Integer)         # B: Value to pinpoint "click"
    C_ANS_value_clicked = db.Column(db.Integer)         # B: Value to pinpoint "click"
    #FALTA --> rgb_color???
    error_A             = db.Column(db.Integer)         # Error A (Real Clusters - Num answered)
    error_B             = db.Column(db.Integer)         # Error B (Real Cell Value - Value answered)
    error_C             = db.Column(db.Integer)         # Error C (Real Value asked - Cell's Value clicked)
    abs_error_A         = db.Column(db.Integer)         # Absolute error A
    abs_error_B         = db.Column(db.Integer)         # Absolute error B
    abs_error_C         = db.Column(db.Integer)         # Absolute error B
    #error o diferencia en RGB del
    time_spent          = db.Column(db.String(32))      # Time spent to answer
    prolific_code       = db.Column(db.String(32))      # Prolific's  code FALTA --> I THINK I MAY NOT NEED THIS




class intrChart: #Charts used in the introduction
    def __init__(self, chart, A_numClus, B_valMark, C_valClick, A_optionsClus, B_optionsVal):
        self.chart = chart
        self.A_numClus = A_numClus
        self.B_valMark = B_valMark
        self.C_valClick = C_valClick
        self.A_optionsClus = A_optionsClus
        self.B_optionsVal = B_optionsVal


class taskChart: #Charts used in tasks
    def __init__(self, chart, A_numClus, B_valMark, C_valClick):
        self.chart = chart
        self.A_numClus = A_numClus
        self.B_valMark = B_valMark
        self.C_valClick = C_valClick


#Input instructions
charts_instr = [intrChart('0heatmap7_Blues_marker_35_0', 0, 35, 14,['1', '4', '0', '3'], ['22', '28', '35', '40']),
                intrChart('1heatmap5_Blues_marker_31_0', 1, 31, 5, ['0', '2', '3', '1'], ['23', '30', '31', '42']),
                intrChart('1heatmap5_Blues_marker_31_transposed_0', 1, 31, 42 ,['1', '4', '3', '2'], ['31', '27', '23', '38']),
                intrChart('2heatmap6_Viridis_marker_23_0', 2, 23, 2, ['0', '2', '3', '1'], ['12', '17', '25', '23']),
                intrChart('2heatmap8_Blues_marker_27_0', 2, 27, 23,['4', '1', '3', '2'], ['31', '21', '19', '27'])]

#Input task
charts_task = [taskChart('0heatmap7_Blues_marker_35_0', 0, 35, 14),
                taskChart('1heatmap5_Blues_marker_31_0', 1, 31, 5),
                taskChart('1heatmap5_Blues_marker_31_transposed_0', 1, 31, 42),
                taskChart('2heatmap6_Viridis_marker_23_0', 2, 23, 2),
                taskChart('2heatmap8_Blues_marker_27_0', 2, 27, 23)]


# We have to use a dictionary for each user to preserve the global values when more than one
# person are doing the test remotely at the same time

# Dictionary to control users and randomize images
# dict_users[key][0] = charts task1 random order
# dict_users[key][1] = charts task2 random order
# dict_users[key][2] = start time used for each users
# dict_users[key][3] = errors of the user in task 1 (instructions)
# dict_users[key][4] = the user is currently in a break
def modifyDictUsers(dictio, key_dict, elem, new_value_elem):
    if dictio.__contains__(key_dict):
        elem0 = dictio[key_dict][0]
        elem1 = dictio[key_dict][1]
        elem2 = dictio[key_dict][2]
        elem3 = dictio[key_dict][3]
        elem4 = dictio[key_dict][4]

        del dictio[key_dict]

        if elem == 0:
            dictio[key_dict] = [new_value_elem, elem1, elem2, elem3, elem4]
        elif elem == 1:
            dictio[key_dict] = [elem0, new_value_elem, elem2, elem3, elem4]
        elif elem == 2:
            dictio[key_dict] = [elem0, elem1, new_value_elem, elem3, elem4]
        elif elem == 3:
            dictio[key_dict] = [elem0, elem1, elem2, new_value_elem, elem4]
        else:
            dictio[key_dict] = [elem0, elem1, elem2, elem3, new_value_elem]

    return dictio

# Check that the control charts do not appear next to the original ones
# Repetim Charts com a "tasca trampa" per veure si responen amb cap
def random_order_valid(random_charts_task):
    order_ok = True
    for i in range(0, NUM_CHARTS_TASK-1):
        if random_charts_task[i].chart == random_charts_task[i+1].chart:
            order_ok = False
    return order_ok


@app.route('/')
def homepage():
    #global charts_instr, charts_task, DICT_USERS
    db.create_all()  # make our sqlalchemy tables


    # Dictionary to control users and randomize images
    # dict_users[key][0] = charts task1 random order
    # dict_users[key][1] = charts task2 random order
    # dict_users[key][2] = start time used for each users
    # dict_users[key][3] = erros of the user in task 1 (instructions)
    # dict_users[key][4] = the user is currently in a break
    DICT_USERS = shelve.open('persistent_info_users')

    # We create the user id and randomize the images for both tasks
    random.seed(time.time())
    user = random.randint(0,100000000)

    # Check that the user does not exist
    while DICT_USERS.__contains__(str(user)):
        user = random.randint(0,100000000)

    random.seed(int(user))
    charts_instr_user = charts_instr
    charts_task_user = charts_task

    random.shuffle(charts_instr_user)
    random.shuffle(charts_task_user)

    while not random_order_valid(charts_task_user):
        random.shuffle(charts_task_user)

    # Add the pair <key, values> to the dictionary.
    DICT_USERS[str(user)]=[charts_instr_user, charts_task_user, dt.datetime.now(), 0, False]

    # for key in DICT_USERS:
    #     print('user: '+key)
    #     for i in range(0, 12):
    #         print(DICT_USERS[key][0][i].chart)

    DICT_USERS.close()

    return redirect('/index/0?u='+str(user));

#####------------------------------------------------------------CAL REPASSAR--------------------------------------------------------
##FALTA

#aux is a value that I won't use
@app.route('/index/<int:aux>')
def index(aux):
    user = request.args.get('u', '')
    return render_template("index.html", user=user)


#aux is a value that I won't use
@app.route('/validateIndex/<int:aux>', methods=['POST','GET'])
def validateIndex(aux):
    user = request.args.get('u', '')

    if 'checkboxTerms' in request.form and request.form['checkboxTerms'] and len(request.form['checkboxTerms']) > 0:
        answersData = AnswersData()
        answersData.date = str(dt.datetime.now().date())
        answersData.time = str(dt.datetime.now().time())
        answersData.user = user
        answersData.task = 'terms_accepted'
        answersData.age = -1
        answersData.gender = '-'
        answersData.education = '-'
        answersData.eyesight = '-'
        answersData.display = '-'
        answersData.understood = '-'
        answersData.easiness = '-'
        answersData.satisfied = '-'
        answersData.comments = '-'

        answersData.chart = '-'
        answersData.A_num_clust = -1
        answersData.A_ANS_num_clus = -1
        answersData.B_value_marker = -1
        answersData.B_ANS_value_marker = -1
        answersData.C_value_to_click = -1
        answersData.C_ANS_value_clicked = -1
        answersData.error_A = -1
        answersData.error_B = -1
        answersData.error_C = -1
        answersData.abs_error_A = -1
        answersData.abs_error_B = -1
        answersData.abs_error_C = -1

        answersData.time_spent = '-'
        answersData.prolific_code = '-'

        db.session.add(answersData)
        db.session.commit()

        #return redirect('/instr/0?u='+str(user))
        return redirect('/demoForm/0?u='+str(user))
    else:
        return render_template("index.html", user=user, error=ERROR_NO_TERMS_ACCEPTED)


#aux is a value that I won't use
@app.route('/demoForm/<int:aux>')
def demoForm(aux):
    user = request.args.get('u', '')
    return render_template("demoForm.html", user=user)


#aux is a value that I won't use
@app.route('/validateDemoForm/<int:aux>', methods=['POST','GET'])
def validateDemoForm(aux):
    user = request.args.get('u', '')

    meattherequirements = True
    allFieldsCompleted = True
    age = -1;
    ageOk = False
    gender = ""
    genderOk = False
    education = ""
    educationOk = False
    eyesight = ""
    eyesightOk = False
    display = "Don't know"
    displayOk = True


    if 'age' in request.form and len(request.form['age']) > 0:
        age = int(request.form['age'])
        if age < 18:
            meattherequirements = False
        elif age >= 0 and age <= 150:
            ageOk = True
    else:
        allFieldsCompleted = False

    if 'gender' in request.form and request.form['gender'] and len(request.form['gender']) > 0:
        gender = request.form['gender']
        if gender != "":
            genderOk = True
    else:
        allFieldsCompleted = False

    if 'education' in request.form and request.form['education'] and len(request.form['education']) > 0:
        education = request.form['education']
        if education != "":
            educationOk = True
    else:
        allFieldsCompleted = False

    if 'eyesight' in request.form and request.form['eyesight'] and len(request.form['eyesight']) > 0:
        eyesight = request.form['eyesight']
        if eyesight != "":
            eyesightOk = True
    else:
        allFieldsCompleted = False

    if 'display' in request.form and len(request.form['display']) > 0:
        if float(request.form['display']) <= 0.0 or float(request.form['display']) > 100.0:
            displayOk = False
        else:
            display = request.form['display']


    if allFieldsCompleted and meattherequirements and ageOk and genderOk and educationOk and eyesightOk and displayOk:
        answersData = AnswersData()
        answersData.date = str(dt.datetime.now().date())
        answersData.time = str(dt.datetime.now().time())
        answersData.user = user
        answersData.task = 'demographic_survey'
        answersData.age = age
        answersData.gender = gender
        answersData.education = education
        answersData.eyesight = eyesight
        answersData.display = display

        answersData.understood = '-'
        answersData.easiness = '-'
        answersData.satisfied = '-'
        answersData.comments = '-'

        answersData.chart = '-'
        answersData.A_num_clust = -1
        answersData.A_ANS_num_clus = -1
        answersData.B_value_marker = -1
        answersData.B_ANS_value_marker = -1
        answersData.C_value_to_click = -1
        answersData.C_ANS_value_clicked = -1
        answersData.error_A = -1
        answersData.error_B = -1
        answersData.error_C = -1
        answersData.abs_error_A = -1
        answersData.abs_error_B = -1
        answersData.abs_error_C = -1

        answersData.time_spent = '-'
        answersData.prolific_code = '-'

        db.session.add(answersData)
        db.session.commit()

        return redirect('/labelInstr/0?u='+str(user))
    elif not meattherequirements:
        return redirect('/labelEndFailure/0?u='+str(user))
    else:
        return render_template("demoForm.html", user=user, error=ERROR_DEMO_SURVEY)

#aux is a value that I won't use
@app.route('/labelInstr/<int:aux>')
def labelInstr(aux):
    user = request.args.get('u', '')
    return render_template("labelInstructions.html", user=user)

#aux is a value that I won't use
@app.route('/startInstr/<int:aux>', methods=['POST','GET'])
def startInstr(aux):
    DICT_USERS = shelve.open('persistent_info_users')
    user = request.args.get('u', '')
    # Begin to compute time just before starting the first chart
    DICT_USERS = modifyDictUsers(DICT_USERS, str(user), 2, dt.datetime.now())
    #DICT_USERS[str(user)][2] = dt.datetime.now()
    DICT_USERS.close()
    return redirect('/instr/0?u='+str(user))


@app.route('/instr/<int:question_id>')
def instructions(question_id):
    DICT_USERS = shelve.open('persistent_info_users')
    user = request.args.get('u', '')

    if question_id == NUM_CHARTS_INSTR:
        if DICT_USERS[str(user)][3] > ERRORS_ALLOWED_INSTR:
            DICT_USERS.close()
            return redirect('/labelEndFailure/0?u='+str(user))
        else:
            DICT_USERS.close()
            return redirect('/labelTask/0?u='+str(user))
    else:
        img_name = DICT_USERS[str(user)][0][question_id].chart
        options_A = DICT_USERS[str(user)][0][question_id].options_A
        options_B = DICT_USERS[str(user)][0][question_id].options_B

        # for key in DICT_USERS:
        #     print('user: '+key)
        #     for i in range(0, 12):
        #         print(DICT_USERS[key][0][i].chart)

        DICT_USERS.close()
        return render_template("instructions.html", img_name=img_name, question_id=question_id, user=user,
                                options_A=options_A, options_B=options_B)


@app.route('/validateInstr/<int:question_id>', methods=['POST','GET'])
def saveAnswersInstr(question_id):
    DICT_USERS = shelve.open('persistent_info_users')
    user = request.args.get('u', '')

    if 'radioGroupA' in request.form and request.form['radioGroupA'] and len(request.form['radioGroupA']) > 0 and 'radioGroupB' in request.form and request.form['radioGroupB'] and len(request.form['radioGroupB']) > 0:
        # Save the answers in the DB
        val_radio_A = int(request.form['radioGroupA'])
        val_radio_B = int(request.form['radioGroupB'])

        # Compute elapsed time in seconds
        stop_time = dt.datetime.now()
        elapsed_time = stop_time - DICT_USERS[str(user)][2]

        answersData = AnswersData()
        answersData.date = str(dt.datetime.now().date())
        answersData.time = str(dt.datetime.now().time())
        answersData.user = user
        answersData.task = 'task 1'
        answersData.age = -1
        answersData.gender = '-'
        answersData.education = '-'
        answersData.eyesight = '-'
        answersData.display = '-'
        answersData.understood = '-'
        answersData.easiness = '-'
        answersData.satisfied = '-'
        answersData.comments = '-'

        answersData.chart = DICT_USERS[str(user)][0][question_id].chart
        answersData.A_num_clust = DICT_USERS[str(user)][0][question_id].val_A
        answersData.A_ANS_num_clus = val_radio_A
        answersData.B_value_marker = DICT_USERS[str(user)][0][question_id].val_B
        answersData.B_ANS_value_marker = val_radio_B
        answersData.error_A = val_radio_A - DICT_USERS[str(user)][0][question_id].val_A
        answersData.error_B = val_radio_B - DICT_USERS[str(user)][0][question_id].val_B
        answersData.abs_error_A = abs(val_radio_A - DICT_USERS[str(user)][0][question_id].val_A)
        answersData.abs_error_B = abs(val_radio_B - DICT_USERS[str(user)][0][question_id].val_B)

        answersData.time_spent = str(elapsed_time.total_seconds())+' sec'
        answersData.prolific_code = '-'

        db.session.add(answersData)
        db.session.commit()

        if answersData.abs_error_A > 10 or answersData.abs_error_B > 10:
            errors_instr = DICT_USERS[str(user)][3] + 1
            DICT_USERS = modifyDictUsers(DICT_USERS, str(user), 3, errors_instr)
            #DICT_USERS[str(user)][3] = DICT_USERS[str(user)][3] + 1

        # Restart time just before starting the next chart
        DICT_USERS = modifyDictUsers(DICT_USERS, str(user), 2, dt.datetime.now())
        #DICT_USERS[str(user)][2] = dt.datetime.now()
        DICT_USERS.close()
        return redirect('/instr/'+str(question_id+1)+'?u='+str(user))
    else:
        img_name = DICT_USERS[str(user)][0][question_id].chart
        options_A = DICT_USERS[str(user)][0][question_id].options_A
        options_B = DICT_USERS[str(user)][0][question_id].options_B
        DICT_USERS.close()
        return render_template("instructions.html", img_name=img_name, question_id=question_id, user=user,
                                options_A=options_A, options_B=options_B, error=ERROR_NO_OPTION)

#aux is a value that I won't use
@app.route('/labelTask/<int:aux>')
def labelTask(aux):
    user = request.args.get('u', '')
    return render_template("labelTask.html", user=user)

#aux is a value that I won't use
@app.route('/startTask/<int:aux>', methods=['POST','GET'])
def startTask(aux):
    DICT_USERS = shelve.open('persistent_info_users')
    user = request.args.get('u', '')
    # Begin to compute time just before starting the first chart
    DICT_USERS = modifyDictUsers(DICT_USERS, str(user), 2, dt.datetime.now())
    #DICT_USERS[str(user)][2] = dt.datetime.now()
    DICT_USERS.close()
    return redirect('/task/0?u='+str(user))

@app.route('/task/<int:question_id>', methods=['POST','GET'])
def task(question_id):
    DICT_USERS = shelve.open('persistent_info_users')
    user = request.args.get('u', '')

    if question_id == NUM_CHARTS_TASK:
        DICT_USERS.close()
        return redirect('/evalForm/0?u='+str(user))
    elif not DICT_USERS[str(user)][4] and question_id != 0 and question_id % NUM_CHARTS_BETWEEN_BREAKS == 0:
        DICT_USERS = modifyDictUsers(DICT_USERS, str(user), 4, True)
        #DICT_USERS[str(user)][4] = True;
        DICT_USERS.close()
        return redirect('/breakTime/'+str(question_id)+'?u='+str(user))
    else:
        if DICT_USERS[str(user)][4]:
            DICT_USERS = modifyDictUsers(DICT_USERS, str(user), 4, False)
            DICT_USERS[str(user)][4] = False

        img_name = DICT_USERS[str(user)][1][question_id].chart
        DICT_USERS.close()
        return render_template("task.html", img_name=img_name, question_id=question_id, user=user)


@app.route('/validateTask/<int:question_id>', methods=['POST','GET'])
def saveAnswersTask(question_id):
    DICT_USERS = shelve.open('persistent_info_users')
    user = request.args.get('u', '')

    if 'numberA' in request.form and len(request.form['numberA']) > 0 and 'numberB' in request.form and len(request.form['numberB']) > 0:
        val_number_A = int(request.form['numberA'])
        val_number_B = int(request.form['numberB'])

        if val_number_A >=0 and val_number_A <= 100 and val_number_B >=0 and val_number_B <= 100:
            # Compute elapsed time in seconds
            stop_time = dt.datetime.now()
            elapsed_time = stop_time - DICT_USERS[str(user)][2]

            # Save the answers in the DB
            answersData = AnswersData()
            answersData.date = str(dt.datetime.now().date())
            answersData.time = str(dt.datetime.now().time())
            answersData.user = user
            answersData.task = 'task 2'
            answersData.age = -1
            answersData.gender = '-'
            answersData.education = '-'
            answersData.eyesight = '-'
            answersData.display = '-'
            answersData.understood = '-'
            answersData.easiness = '-'
            answersData.satisfied = '-'
            answersData.comments = '-'

            answersData.chart = DICT_USERS[str(user)][1][question_id].chart
            answersData.A_num_clust = DICT_USERS[str(user)][1][question_id].val_A
            answersData.A_ANS_num_clus = val_number_A
            answersData.B_value_marker = DICT_USERS[str(user)][1][question_id].val_B
            answersData.B_ANS_value_marker = val_number_B
            answersData.error_A = val_number_A - DICT_USERS[str(user)][1][question_id].val_A
            answersData.error_B = val_number_B - DICT_USERS[str(user)][1][question_id].val_B
            answersData.abs_error_A = abs(val_number_A - DICT_USERS[str(user)][1][question_id].val_A)
            answersData.abs_error_B = abs(val_number_B - DICT_USERS[str(user)][1][question_id].val_B)

            answersData.time_spent = str(elapsed_time.total_seconds())+' sec'
            answersData.prolific_code = '-'
            db.session.add(answersData)
            db.session.commit()

            # Restart time just before starting the next chart
            DICT_USERS = modifyDictUsers(DICT_USERS, str(user), 2, dt.datetime.now())
            #DICT_USERS[str(user)][2] = dt.datetime.now()
            DICT_USERS.close()
            return redirect('/task/'+str(question_id+1)+'?u='+str(user))

    img_name = DICT_USERS[str(user)][1][question_id].chart
    DICT_USERS.close()
    return render_template("task.html", img_name=img_name, question_id=question_id, user=user,
                            error=ERROR_VALUES)


@app.route('/breakTime/<int:question_id>', methods=['POST','GET'])
def breakTime(question_id):
    user = request.args.get('u', '')
    progress = int((float(question_id)/float(NUM_CHARTS_TASK))*100.0)
    return render_template("labelBreak.html", question_id=question_id, user=user, progress=progress)


#aux is a value that I won't use
@app.route('/evalForm/<int:aux>')
def evalForm(aux):
    user = request.args.get('u', '')
    return render_template("evalForm.html", user=user)


#aux is a value that I won't use
@app.route('/validateEvalForm/<int:aux>', methods=['POST','GET'])
def validateEvalForm(aux):
    user = request.args.get('u', '')

    allFieldsCompleted = True
    udnerstood = "";
    understoodOk = False
    easiness = ""
    easinessOk = False
    satisfied = ""
    satisfiedOk = False
    comments = '-'

    if 'understood' in request.form and request.form['understood'] and len(request.form['understood']) > 0:
        understood = request.form['understood']
        if understood != "":
            understoodOk = True
    else:
        allFieldsCompleted = False

    if 'easiness' in request.form and request.form['easiness'] and len(request.form['easiness']) > 0:
        easiness = request.form['easiness']
        if easiness != "":
            easinessOk = True
    else:
        allFieldsCompleted = False

    if 'satisfied' in request.form and request.form['satisfied'] and len(request.form['satisfied']) > 0:
        satisfied = request.form['satisfied']
        if satisfied != "":
            satisfiedOk = True
    else:
        allFieldsCompleted = False

    if 'comments' in request.form and request.form['comments'] and len(request.form['comments']) > 0:
        comments = request.form['comments']

    if allFieldsCompleted and understoodOk and easinessOk and satisfiedOk :
        answersData = AnswersData()
        answersData.date = str(dt.datetime.now().date())
        answersData.time = str(dt.datetime.now().time())
        answersData.user = user
        answersData.task = 'personal_evaluation'
        answersData.age = -1
        answersData.gender = '-'
        answersData.education = '-'
        answersData.eyesight = '-'
        answersData.display = '-'
        answersData.understood = understood
        answersData.easiness = easiness
        answersData.satisfied = satisfied
        answersData.comments = comments

        answersData.chart = '-'
        answersData.A_num_clust = -1
        answersData.A_ANS_num_clus = -1
        answersData.B_value_marker = -1
        answersData.B_ANS_value_marker = -1
        answersData.C_value_to_click = -1
        answersData.C_ANS_value_clicked = -1
        answersData.error_A = -1
        answersData.error_B = -1
        answersData.error_C = -1
        answersData.abs_error_A = -1
        answersData.abs_error_B = -1
        answersData.abs_error_C = -1

        answersData.time_spent = '-'
        answersData.prolific_code = '-'
        db.session.add(answersData)
        db.session.commit()

        return redirect('/labelEndSuccess/0?u='+str(user))
    else:
        return render_template("evalForm.html", user=user, error=ERROR_EVAL_SURVEY)


#aux is a value that I won't use
@app.route('/labelEndSuccess/<int:aux>')
def labelEndSuccess(aux):
    user = request.args.get('u', '')
    prolific_code = random.randint(0,100000000)

    # Write the code in the DB
    answersData = AnswersData()
    answersData.date = str(dt.datetime.now().date())
    answersData.time = str(dt.datetime.now().time())
    answersData.user = user
    answersData.task = 'prolific_code'
    answersData.age = -1
    answersData.gender = '-'
    answersData.education = '-'
    answersData.eyesight = '-'
    answersData.display = '-'
    answersData.understood = '-'
    answersData.easiness = '-'
    answersData.satisfied = '-'
    answersData.comments = '-'

    answersData.chart = '-'
    answersData.A_num_clust = -1
    answersData.A_ANS_num_clus = -1
    answersData.B_value_marker = -1
    answersData.B_ANS_value_marker = -1
    answersData.C_value_to_click = -1
    answersData.C_ANS_value_clicked = -1
    answersData.error_A = -1
    answersData.error_B = -1
    answersData.error_C = -1
    answersData.abs_error_A = -1
    answersData.abs_error_B = -1
    answersData.abs_error_C = -1

    answersData.time_spent = '-'
    answersData.prolific_code = str(prolific_code)
    db.session.add(answersData)
    db.session.commit()

    return render_template("labelEndSuccess.html", user=user, prolific_code=prolific_code)

#aux is a value that I won't use
@app.route('/labelEndFailure/<int:aux>')
def labelEndFailure(aux):
    user = request.args.get('u', '')
    return render_template("labelEndFailure.html", user=user)


if __name__ == "__main__":
    #random.seed(time.time())
    app.run(debug=True)
    app.run()
