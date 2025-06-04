from flask import Flask, render_template, request, redirect, url_for
import os

try:
    import whisper
except ImportError:
    whisper = None

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    transcript = None
    if whisper:
        model = whisper.load_model('base')
        result = model.transcribe(filepath, language='bg')
        transcript = result.get('text')
    else:
        transcript = 'Whisper is not installed.'

    return render_template('index.html', transcript=transcript)

if __name__ == '__main__':
    app.run(debug=True)
