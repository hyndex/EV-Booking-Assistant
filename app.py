from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)

CITIES = [
    'baksa',
    'barpeta',
    'biswanath',
    'bongaigaon',
    'cachar',
    'charaideo',
    'chirang',
    'darrang',
    'dhemaji',
    'dhubri',
    'dibrugarh',
    'dima Hasao',
    'goalpara',
    'golaghat',
    'hailakandi',
    'hojai',
    'jorhat',
    'kamrup',
    'karbi anglong',
    'karimganj',
    'kokrajhar',
    'lakhimpur',
    'majuli',
    'morigaon',
    'nagaon',
    'nalbari',
    'sivasagar',
    'sonitpur',
    'tinsukia',
    'udalguri',
    ]
# https://blog.addpipe.com/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/
@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    for req_city in (transcript.lower().split(' ')):
        if req_city in CITIES:
            print(req_city)
            return render_template('index.html', transcript='charger has been booked in '+req_city)
    return render_template('index.html', transcript='Charger not avialable in the requested city')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
