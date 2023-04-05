import random
import string
from flask import Flask, render_template, request, send_file
from moviepy.editor import *

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi'}

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Render the index template with the audio flag and error flag set to False
# If a file argument is present in the URL query string, send the file as an attachment
@app.route('/')
def index():
    file = request.args.get('file')
    if file:
        file = os.path.join('uploads', file)
        return send_file(file, as_attachment=True)
    else:
        return render_template('index.html', audio=False, error=False)

# Handle file uploads
@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Extract audio from the uploaded video file
        video = VideoFileClip(file_path)
        audio = video.audio

        # Generate a unique filename for the audio file or save the old one
        audio_filename = ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + '.mp3' if not file.filename.rsplit('.', 1)[0] else file.filename.rsplit('.', 1)[0] + '.mp3'
        audio_path = os.path.join('uploads', audio_filename)
        audio.write_audiofile(audio_path)

        # Render the index template with the audio flag set to True and the error flag set to False
        # Also include the filename of the generated audio file, which will be used to download the file
        return render_template('index.html', audio=True, file=audio_filename, error=False)
    else:
        # If the uploaded file is not valid, render the index template with the error flag set to True
        return render_template('index.html', audio=False, error=True)

if __name__ == '__main__':
    app.run(debug=True)
