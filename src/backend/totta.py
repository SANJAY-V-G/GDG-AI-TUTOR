import os
import cv2
import time
import json
import queue
import asyncio
import threading
import numpy as np
import pandas as pd
import websockets
import pygame
import speech_recognition as sr
from gtts import gTTS
from fuzzywuzzy import fuzz, process
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras import Input

# === Setup ===
audio_dir = "temp"
os.makedirs(audio_dir, exist_ok=True)

recognizer = sr.Recognizer()
clients = set()
speech_queue = queue.Queue()
speech_lock = threading.Lock()
pygame.mixer.init()

# === Load Dataset ===
df = pd.read_csv("C:\\Users\\Dell\\Downloads\\agriculture_questions_complete.csv")
df["question"] = df["question"].str.lower()

# === Load Emotion Model ===
emotion_dict = {0: "Confused", 1: "Disgusted", 2: "Sleepy", 3: "Normal", 4: "Neutral", 5: "Disturbed", 6: "Thinking"}
model = Sequential([
    Input(shape=(48, 48, 1)),
    Conv2D(32, (3, 3), activation='relu'),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])
model.load_weights("C:\\Users\\Dell\\Desktop\\Emotion-detection\\model.h5")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
sleepy_count = 0

# === Helper Functions ===
def get_best_answer(question):
    best_match = process.extractOne(question, df["question"], scorer=fuzz.token_set_ratio)
    if best_match and best_match[1] >= 70:
        return df.loc[df["question"] == best_match[0], "answer"].values[0]
    return "I'm sorry, but I don't have an answer for that."

def speak(text):
    with speech_lock:
        tts = gTTS(text=text, lang='en')
        path = os.path.join(audio_dir, "output.mp3")
        tts.save(path)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

def listen():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            return recognizer.recognize_google(audio).lower()
        except:
            return ""

def emotion_detection():
    global sleepy_count
    cap = cv2.VideoCapture(0)
    last_emotion_time = time.time()
    last_emotion = None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            if time.time() - last_emotion_time > 10:
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                last_emotion = emotion_dict[maxindex]
                last_emotion_time = time.time()
                for ws in clients:
                    asyncio.run_coroutine_threadsafe(
                        ws.send(json.dumps({"type": "emotion", "emotion": last_emotion})),
                        asyncio.get_event_loop()
                    )
                if last_emotion == "Confused" or last_emotion == "Thinking":
                    speech_queue.put("did you understand?")
                elif last_emotion == "Sleepy":
                    sleepy_count += 1
                    speech_queue.put("Please stay awake and focused.")
                    if sleepy_count >= 5:
                        speech_queue.put("You seem tired. Please take a break.")
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                elif last_emotion == "Disturbed":
                    speech_queue.put("Is something bothering you?")
            if last_emotion:
                cv2.putText(frame, last_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def speech_worker():
    while True:
        msg = speech_queue.get()
        if msg is None:
            break
        speak(msg)
        speech_queue.task_done()

# === WebSocket Logic ===
async def handle_client(websocket):
    clients.add(websocket)
    print("Client connected.")
    try:
        while True:
            await websocket.send(json.dumps({"type": "control", "action": "pause"}))
            user_input = listen()
            await websocket.send(json.dumps({"type": "speech", "text": user_input}))

            if not user_input:
                await websocket.send(json.dumps({"type": "control", "action": "resume"}))
                await asyncio.sleep(2)
                continue

            if "bye" in user_input:
                response = "Goodbye! Have a fantastic day!"
                await websocket.send(json.dumps({"type": "response", "text": response}))
                speak(response)
                break
            else:
                answer = get_best_answer(user_input)
                await websocket.send(json.dumps({"type": "response", "text": answer}))
                speak(answer)

            await websocket.send(json.dumps({"type": "control", "action": "resume"}))
            await asyncio.sleep(2)
    except Exception as e:
        print("Client error:", e)
    finally:
        clients.remove(websocket)
        print("Client disconnected.")

# === Main ===
async def main():
    print("WebSocket server starting on ws://localhost:8000")
    async with websockets.serve(handle_client, "localhost", 8000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    threading.Thread(target=emotion_detection, daemon=True).start()
    threading.Thread(target=speech_worker, daemon=True).start()
    asyncio.run(main())
