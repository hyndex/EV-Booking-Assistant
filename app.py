from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import pandas as pd

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
    'karbianglong',
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
    'guwahati',
    'lucknow'
]
# https://blog.addpipe.com/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/

queue = {'baksa': 0,
         'barpeta': 0,
         'biswanath': 0,
         'bongaigaon': 0,
         'cachar': 0,
         'charaideo': 0,
         'chirang': 0,
         'darrang': 0,
         'dhemaji': 0,
         'dhubri': 0,
         'dibrugarh': 0,
         'dima Hasao': 0,
         'goalpara': 0,
         'golaghat': 0,
         'hailakandi': 0,
         'hojai': 0,
         'jorhat': 0,
         'kamrup': 0,
         'karbianglong': 0,
         'karimganj': 0,
         'kokrajhar': 0,
         'lakhimpur': 0,
         'majuli': 0,
         'morigaon': 0,
         'nagaon': 0,
         'nalbari': 0,
         'sivasagar': 0,
         'sonitpur': 0,
         'tinsukia': 0,
         'udalguri': 0,
         'guwahati': 0,
         'lucknow': 0}


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
            try:
                transcript = recognizer.recognize_google(data, key=None)
            except:
                return render_template('index.html',latitude='26.2006', longitude='92.9376', transcript='Try again')

        for req_city in (transcript.lower().split(' ')):
            print(req_city)
            if req_city in CITIES:
                print(req_city)
                queue[req_city] = queue[req_city]+1
                data = pd.read_csv('loc.csv')
                data['place_name']=data['place_name'].str.lower()
                result = data[data['place_name'].str.contains(req_city)].iloc[0]
                latitude=str(result['latitude']) 
                longitude=str(result['longitude'])
                print(data[data['place_name']==req_city])
                print(latitude, longitude)
                return render_template('index.html', transcript='charger has been booked in ' + req_city+' Your queue is '+str(queue[req_city]),latitude=latitude,longitude=longitude )
        return render_template('index.html', transcript='Charger not available in the requested city',latitude='26.2006', longitude='92.9376')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
