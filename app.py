from flask import Flask, request, render_template, jsonify
from multiprocessing import Manager, Process
import Downloader

app = Flask(__name__)

# Use a manager for shared state
manager = Manager()
download_status = manager.dict()
download_history = manager.list()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': 'URL is required.'}), 400

    # Reset status and history for a new download
    download_status.clear()
    # Clear the list by replacing its content
    download_history[:] = []
    
    # Start the download in a separate process
    p = Process(target=Downloader.download_all_files, args=(url, download_status, download_history))
    p.start()

    return jsonify({'status': 'success', 'message': f'Download initiated for: {url}'})

@app.route('/status')
def status():
    return jsonify(dict(download_status))

@app.route('/history')
def history():
    return jsonify(list(download_history))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)