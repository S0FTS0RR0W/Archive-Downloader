from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        url = request.form['url']
        subprocess.run(['python', 'Downloader.py', url])
        message = f"Started download for: {url}"
    return render_template('index.html', message=message)