from bottle import redirect, route, run, jinja2_view, static_file, request
from scripts import get_questions 
from time import time
import pandas as pd
import os

@route('/thankyou')
@jinja2_view('thankyou.html')
def thankyou():
    return

# Static CSS Files
@route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/css')

@route('/')
@jinja2_view('index.html')
def questionnaire():
    # tmp save
    now = time()
    top_words = ['pig', 'cow', 'horse', 'milk', 'crops', 'chicken', 'tractor']
    return {'range': range(len(top_words)), 'multi_choice': [('farm', 0),('animal', 0),('journalism', 0)], 'top_words': top_words, 'now': now}

@route('/', method='POST')
def begin_questionnaire():
    redirect("/questionnaire")

@route('/questionnaire')
@jinja2_view('questionnaire.html')
def questionnaire():
    questions = get_questions(None, 10)
    # tmp save
    now = time()
    questions.to_pickle(f"tmp_{now}.pickle")
    multi_choices = questions['multi_choice'].tolist()
    top_words = [[(x," ".join(y.split("_"))) for (x,y) in g] for g in questions['top_words'].tolist()]
    print(top_words)
    return {'range': range(len(top_words)), 'multi_choice': multi_choices, 'top_words': top_words, 'index': [str(x) for x in questions.index.tolist()], 'now': now}

@route('/questionnaire', method='POST')
def submit_questionnaire():
    IS_INTRUDER = 0
    selected = []
    is_correct = []
    tmp_hash = request.forms['timestamp']
    questions = pd.read_pickle(f"tmp_{tmp_hash}.pickle")
    for i, (index, choice_label) in enumerate(request.forms.items()):
        if i == 0:
            continue
        multi_choice = questions.iloc[int(index)]['multi_choice']
        for mc_label, is_intruder in multi_choice:
            if mc_label == choice_label:
                    choice_correct = is_intruder == IS_INTRUDER
        selected.append(choice_label)
        is_correct.append(choice_correct)
    questions['human_choice'] = selected
    questions['is_correct'] = is_correct
    now = time()
    questions.to_pickle(f"{now}_questionnaire.pickle")
    questions.to_csv(f"{now}_questionnaire.csv")
    # remove tmp
    os.remove(f"tmp_{tmp_hash}.pickle")
    redirect("/thankyou")

run(host='localhost')