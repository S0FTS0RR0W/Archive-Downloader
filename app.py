import json
import os
from flask import Flask, render_template, request, jsonify
from threading import Thread
from Downloader import download_all_files

app = Flask(__name__)

# --- Settings Management ---
SETTINGS_FILE = 'settings.json'

# Default settings
settings = {
    'max_workers': 5
}

def load_settings():
    """Loads settings from the JSON file."""
    global settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings.update(json.load(f))

def save_settings():
    """Saves current settings to the JSON file."""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# --- Download State Management ---
# (In a real app, you'd want a more robust way to track tasks)
download_history = []
is_downloading = False

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html', history=download_history, is_downloading=is_downloading)

@app.route('/download', methods=['POST'])
def start_download():
    """Starts a new download process in the background."""
    global is_downloading, download_history
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required.'}), 400

    if is_downloading:
        return jsonify({'error': 'A download is already in progress.'}), 400

    # Clear history for the new download session
    download_history.clear()
    is_downloading = True

    # Run the download in a background thread
    def download_wrapper(url, history, workers):
        global is_downloading
        try:
            download_all_files(url, history, max_workers=workers)
        finally:
            is_downloading = False

    thread = Thread(target=download_wrapper, args=(url, download_history, settings['max_workers']))
    thread.start()

    return jsonify({'message': 'Download started.'})

@app.route('/status')
def status():
    """Provides the current download status and history."""
    return jsonify({'is_downloading': is_downloading, 'history': download_history})

@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    """Handles viewing and updating settings."""
    if request.method == 'POST':
        try:
            workers = int(request.form.get('max_workers'))
            if workers > 0:
                settings['max_workers'] = workers
                save_settings()
                return render_template('settings.html', settings=settings, message='Settings saved!')
            else:
                return render_template('settings.html', settings=settings, error='Max workers must be a positive number.')
        except (ValueError, TypeError):
            return render_template('settings.html', settings=settings, error='Invalid value for max workers.')

    return render_template('settings.html', settings=settings)


if __name__ == '__main__':
    load_settings()
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    # Note: use_reloader=False is important for this simple background thread model
    app.run(debug=True, use_reloader=False)