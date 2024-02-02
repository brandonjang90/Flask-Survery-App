from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "password-please"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def show_survey():
    """Return homepage."""

    return render_template("start.html", survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    """ """
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def collect_answers():

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/finish")
    
    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route('/questions/<int:qid>')
def show_question(qid):

    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        return redirect("/")
    if (len(responses)) == len(survey.questions):
        return redirect("/finish")
    
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect (f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("questions.html", question_num = qid, question = question)

@app.route("/finish")
def finish():
    return render_template("endpage.html")