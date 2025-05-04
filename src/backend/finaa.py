import time
import numpy as np
import threading
import queue
import cv2
import speech_recognition as sr
import pandas as pd
import requests
import os
import pygame
from fuzzywuzzy import fuzz, process
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import LearningRateScheduler

# Load Dataset
DATASET_PATH = "C:\\Users\\sivakarthikeyan\\Downloads\\agriculture_questions_complete.csv"  # Ensure the correct path
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError("Dataset file not found!")
df = pd.read_csv(DATASET_PATH)
df["question"] = df["question"].str.lower()

# ElevenLabs API Configuration
ELEVENLABS_API_KEY = "sk_ef244e55f84a5a4f3871725bbf004d3de711a09132d9704e"  # Replace with your actual API key
VOICE_ID = "LcfcDJNUP1GQjkzn1xUU"  # Replace with your preferred ElevenLabs voice

# Ensure 'temp' directory exists for audio storage
audio_dir = "temp"
os.makedirs(audio_dir, exist_ok=True)

# Speech Queue & Lock to synchronize speech output
speech_queue = queue.Queue()
speech_lock = threading.Lock()

# Load Emotion Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
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

# Load pre-trained weights
MODEL_PATH = "C:\\Users\\sivakarthikeyan\\Downloads\\Emotion-detection\\Emotion-detection\\model.h5"
if os.path.exists(MODEL_PATH):
    model.load_weights(MODEL_PATH)
else:
    raise FileNotFoundError("Model file not found!")

# Emotion Labels
emotion_dict = {0: "Confused", 1: "Disgusted", 2: "Sleepy", 3: "Normal", 4: "Neutral", 5: "Disturbed", 6: "Thinking"}

# Initialize Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Speech Recognition Setup
recognizer = sr.Recognizer()

# Speech Processing Function
def speak(text):
    with speech_lock:  # Ensure only one speech request at a time
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {"Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY}
        data = {"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            audio_path = os.path.join(audio_dir, "output.mp3")
            with open(audio_path, "wb") as f:
                f.write(response.content)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
        else:
            print("Error generating speech", response.json())

# Background Speech Thread
def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break  # Exit condition
        speak(text)
        speech_queue.task_done()

speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

# AI Tutor Function
def listen():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Increase noise adjustment time
        print("Listening...")
        
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)  # Increase timeout
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        
        except sr.UnknownValueError:
            print("Sorry, I could not understand. Please repeat.")
            return ""  # Return empty string to avoid crashing
        
        except sr.RequestError:
            print("Check your internet connection.")
            return ""
        
        except sr.WaitTimeoutError:
            print("Listening timed out, try again.")
            return ""

        except Exception as e:
            print(f"Unexpected error: {e}")
            return ""


def get_best_answer(question):
    best_match = process.extractOne(question, df["question"], scorer=fuzz.token_set_ratio)
    if best_match and best_match[1] >= 70:
        return df.loc[df["question"] == best_match[0], "answer"].values[0]
    return "I'm sorry, but I don't have an answer for that."

# Emotion Detection & AI Interaction Loop
# Track Sleepy Count
sleepy_count = 0  

def emotion_detection():
    global sleepy_count  # Allow modification of the counter
    cap = cv2.VideoCapture(0)
    last_emotion = None
    last_emotion_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)

            if time.time() - last_emotion_time > 5:
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                last_emotion = emotion_dict[maxindex]
                last_emotion_time = time.time()
                
                # Handle Emotion Responses
                if last_emotion == "Confused":
                    speech_queue.put("I see that you are confused. Do you need any clarification?")
                elif last_emotion == "Sleepy":
                    global sleepy_count
                    sleepy_count += 1
                    speech_queue.put("Wake up! Let's stay focused.")
                    
                    # If sleepy count reaches 5, suggest taking a break
                    if sleepy_count >= 5:
                        speech_queue.put("You have been feeling sleepy multiple times. Please take a break and come back later.")
                        cap.release()
                        cv2.destroyAllWindows()
                        return  # Exit the function to stop emotion detection
                
                elif last_emotion == "Disturbed":
                    speech_queue.put("Try to stay focused. I'm here to help.")
                
                print(f"Detected Emotion: {last_emotion}")

            if last_emotion:
                cv2.putText(frame, last_emotion, (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
        
        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


# Run Emotion Detection & AI Tutor in Parallel
threading.Thread(target=emotion_detection, daemon=True).start()

while True:
    user_input = listen()
    if "bye" in user_input:
        speech_queue.put("Goodbye! Have a fantastic day!")
        break
    elif user_input:
        response = get_best_answer(user_input)
        speech_queue.put(response)
