import sounddevice as sd
import numpy as np
import whisper
import queue
import threading

model = whisper.load_model("small")
RATE = 16000
CHUNK = 2048

audio_q = queue.Queue()

def audio_callback(indata, frames, time, status):
    audio_q.put(indata.copy())

def transcribe_loop():
    buffer = np.zeros((0,1), dtype=np.float32)
    print("开始实时识别...")

    while True:
        chunk = audio_q.get()
        buffer = np.concatenate([buffer, chunk])

        if len(buffer) >= RATE * 2:  # 每 2 秒识别一次
            audio = buffer.flatten()
            buffer = np.zeros((0,1), dtype=np.float32)

            result = model.transcribe(audio, language="zh")
            print(result["text"])

def main():
    threading.Thread(target=transcribe_loop, daemon=True).start()

    with sd.InputStream(samplerate=RATE, channels=1, callback=audio_callback):
        print("Listening...")
        while True:
            sd.sleep(1000)

if __name__ == "__main__":
    main()
