from flask import Flask, request, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': 'URL is required.'}), 400

    process = subprocess.Popen(['python', 'Downloader.py', url],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    output, _ = process.communicate()

    if "No files found" in output:
        message = "No files found for the given URL."
        status = "info"
    elif "Error" in output:
        message = "An error occurred while processing the URL."
        status = "error"
    else:
        message = f"Download started for: {url}"
        status = "success"
        
    return jsonify({'status': status, 'message': message})