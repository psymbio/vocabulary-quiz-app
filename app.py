from flask import Flask, jsonify, render_template, abort, url_for, json
import numpy as np
import pickle

app = Flask(__name__)

with open('quizzes.pickle', 'rb') as handle:
    quizzes = pickle.load(handle)

@app.route('/question/<string:quiz>/<int:num_options>', methods=['GET'])
def question(quiz="B333", num_options=4):
    ques = get_question(quiz, num_options)
    
    return jsonify(ques)

@app.route('/quiz/<string:quiz>/<int:num_options>/<int:num_ques>', methods=['GET'])
def quiz(quiz="B333", num_options=4, num_ques=10):
    questions = [get_question(quiz, num_options) for _ in range(num_ques)]
    return jsonify({'questions': questions})


def get_question(quiz="B333", num_options=4):
    words, meanings, D = quizzes[quiz]
    n = len(words)
    ques = np.random.randint(0, n)
    options = np.random.choice(list(range(n)), num_options-1, False, D[ques])
    
    return_dict = {}
    return_dict["question"] = meanings[ques]
    return_dict["answer"] = words[ques]
    return_dict["options"] = [words[i] for i in options]

    return return_dict

@app.route('/',methods = ['POST', 'GET'])
def vocabquiz():
    questions = quiz()
    return render_template('index.html', questions=questions)

if __name__=="__main__":
    app.run(debug=True)