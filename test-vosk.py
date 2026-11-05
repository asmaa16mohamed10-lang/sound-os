import wave, json
from vosk import Model, KaldiRecognizer

wf = wave.open("test3.wav", "rb")
model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())

while True:
	data = wf.readframes(4000)
	if len(data) == 0:
		break
	rec.AcceptWaveform(data)

print(json.loads(rec.FinalResult())["text"])
