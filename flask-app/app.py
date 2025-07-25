from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)


def is_malicious(input_text):
    patterns = [
        r"<.*?>", r"script", r"(?:--|\bOR\b|\bAND\b)",
        r"(?:DROP|SELECT|INSERT|DELETE|UPDATE)\b"
    ]
    return any(re.search(p, input_text, re.IGNORECASE) for p in patterns)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form.get('search', '')
        if is_malicious(search_term):
            # stay on page, clear input
            return render_template('index.html', search_term='')
        return redirect(url_for('result', term=search_term))
    return render_template('index.html', search_term='')


@app.route('/result')
def result():
    term = request.args.get('term', '')
    return render_template('result.html', term=term)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
