
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "quizmaster123"

# Quiz questions
questions = {

    "Computer Science": [
        {
            "question": "Which language is used for web page structure?",
            "options": ["Python", "HTML", "Java", "SQL"],
            "answer": "HTML"
        },
        {
            "question": "What does CPU stand for?",
            "options": [
                "Central Processing Unit",
                "Computer Personal Unit",
                "Central Program Utility",
                "Control Processing Unit"
            ],
            "answer": "Central Processing Unit"
        },
        {
            "question": "Which function displays output in Python?",
            "options": ["input()", "print()", "output()", "show()"],
            "answer": "print()"
        }
    ],

    "Physics": [
        {
            "question": "What is the SI unit of electric current?",
            "options": ["Volt", "Ohm", "Ampere", "Watt"],
            "answer": "Ampere"
        },
        {
            "question": "What is the speed of light in vacuum?",
            "options": [
                "3 × 10^8 m/s",
                "3 × 10^6 m/s",
                "3 × 10^5 m/s",
                "3 × 10^3 m/s"
            ],
            "answer": "3 × 10^8 m/s"
        }
    ],

    "Chemistry": [
        {
            "question": "What is the chemical formula of water?",
            "options": ["CO2", "H2O", "O2", "NaCl"],
            "answer": "H2O"
        },
        {
            "question": "What is the pH of pure water at 25°C?",
            "options": ["5", "7", "9", "14"],
            "answer": "7"
        }
    ],

    "Mathematics": [
        {
            "question": "What is the derivative of x²?",
            "options": ["x", "2x", "x²", "2"],
            "answer": "2x"
        },
        {
            "question": "What is the value of sin 90°?",
            "options": ["0", "1", "-1", "1/2"],
            "answer": "1"
        }
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    subject = request.form.get("subject")

    if subject not in questions:
        return redirect(url_for("home"))

    session["subject"] = subject
    session["answers"] = []

    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    subject = session.get("subject")

    if subject not in questions:
        return redirect(url_for("home"))

    quiz_questions = questions[subject]
    answers = session.get("answers", [])

    if request.method == "POST":

        selected = request.form.get("answer")
        current = len(answers)

        if current >= len(quiz_questions):
            return redirect(url_for("result"))

        valid_options = quiz_questions[current]["options"]

        if selected not in valid_options:
            return redirect(url_for("quiz"))

        answers.append(selected)
        session["answers"] = answers

        if len(answers) == len(quiz_questions):
            return redirect(url_for("result"))

    current = len(answers)

    return render_template(
        "quiz.html",
        question=quiz_questions[current],
        number=current + 1,
        total=len(quiz_questions),
        subject=subject
    )


@app.route("/result")
def result():

    subject = session.get("subject")

    if subject not in questions:
        return redirect(url_for("home"))

    quiz_questions = questions[subject]
    answers = session.get("answers", [])

    if len(answers) != len(quiz_questions):
        return redirect(url_for("quiz"))

    score = 0

    for i in range(len(quiz_questions)):
        if answers[i] == quiz_questions[i]["answer"]:
            score += 1

    percentage = (score / len(quiz_questions)) * 100

    return render_template(
        "result.html",
        questions=quiz_questions,
        answers=answers,
        score=score,
        total=len(quiz_questions),
        percentage=percentage,
        subject=subject
    )


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
