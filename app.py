from flask import Flask, render_template, request, jsonify
from emojilist import emojis
import emoji, random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    message = request.form['message']

    # create suggestions
    num = random.randint(1, 10)
    suggestions = [emoji.emojize(emojis[i]) for i in random.sample(xrange(len(emojis)), num)]

    return jsonify({'suggestions' : suggestions})

if __name__ == '__main__':
    app.run(debug = True)
