from flask import Flask, render_template, request, jsonify
import vosk, sounddevice as sd, queue, json, pyttsx3
import argostranslate.translate
import os

# argostranslate.package,


import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


app = Flask(__name__)

q = queue.Queue()
vosk.SetLogLevel(-1)

# Language configs
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh"
}

MODEL_PATHS = {
    "en": "models/vosk-model-small-en-us-0.15",
    "hi": "models/vosk-model-small-hi-0.22",
    "es": "models/vosk-model-small-es-0.42",
    "de": "models/vosk-model-small-de-0.21",
    "ja": "models/vosk-model-small-ja-0.22",
    "zh": "models/vosk-model-small-cn-0.22"
}

installed_languages = argostranslate.translate.get_installed_languages()
lang_dict = {lang.code: lang for lang in installed_languages}

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize_speech(recognizer):
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "")

def translate_chain(text, source, target):
    if source == target:
        return text
    try:
        if source != "en" and target != "en":
            inter = lang_dict[source].get_translation(lang_dict["en"]).translate(text)
            return lang_dict["en"].get_translation(lang_dict[target]).translate(inter)
        else:
            return lang_dict[source].get_translation(lang_dict[target]).translate(text)
    except:
        return "[Translation Failed]"

def speak_text(text, lang):
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        if lang in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source = data['source']
    target = data['target']
    source_code = LANGUAGES[source]
    target_code = LANGUAGES[target]

    model_path = MODEL_PATHS[source_code]
    if not os.path.exists(model_path):
        return jsonify({"error": f"Model for {source} not found!"})

    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)
    recognized = recognize_speech(recognizer)
    translated = translate_chain(recognized, source_code, target_code)
    speak_text(translated, target_code)

    return jsonify({"recognized": recognized, "translated": translated})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)

    # app.run(debug=True)
