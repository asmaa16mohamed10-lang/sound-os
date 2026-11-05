import json, queue, subprocess
import sounddevice as sd
from vosk import Model, KaldiRecognizer

COMMANDS = {
	"list":["ls"],
	"folder":["pwd"],
	"date":["date"],
	"disk":["df", "-h"],
	"memory":["free", "-h"],
	"who":["whoami"],
}

q = queue.Queue()

def callback(indata, frames, time, status):
	q.put(bytes(indata))

def run_command(text):
	for keyword, cmd in COMMANDS.items():
		if keyword in text:
			print(f">> Running: {' '.join(cmd)}")
			result = subprocess.run(cmd, capture_output=True, text=True)
			print(result.stdout)
			return

	print(">>Command not recognized")

model = Model("model")
rec = KaldiRecognizer(model, 16000)

print("Listening... say a command(say 'exit' to quit)")
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1,callback=callback):

	while True:
		data = q.get()
		if rec.AcceptWaveform(data):
			text = json.loads(rec.Result())["text"]
			if not text:
				continue
			print("You said : ", text)
			if "exit" in text:
				break
			run_command(text)

