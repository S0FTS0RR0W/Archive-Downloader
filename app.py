from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

#if input is empty throw error to user
def flash_message(message, category='info'):
    return render_template('index.html', message=message, category=category)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        url = request.form['url']
        process = subprocess.Popen(['python', 'Downloader.py', url],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
        output, _ = process.communicate()

        if "No files found" in output:
            message = "No files found for the given URL."
        elif "Error" in output:
            message = "An error occurred."
        else:
            message = f"Started download for: {url}"
    return render_template('index.html', message=message)