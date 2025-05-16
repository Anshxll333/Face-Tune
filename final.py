import cv2
from deepface import DeepFace
from pytube import Search
import webbrowser
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

emotion_to_query = {
    'happy': 'party bollywood songs',
    'sad': 'sad bollywood songs',
    'angry': 'moosedrilla by sidhu moosewala',
    'surprise': 'upbeat bollywood songs',
    'fear': 'calm bollywood songs',
    'neutral': 'latest bollywood songs',
    'disgust': 'romantic bollywood songs'
}

def get_youtube_recommendations(emotion):
    query = emotion_to_query.get(emotion, 'latest bollywood songs')
    print(f"Searching YouTube for: {query}")

    search_results = Search(query)
    recommendations = []

    for video in search_results.results[:5]:
        recommendations.append({
            'title': video.title,
            'url': video.watch_url
        })

    return recommendations

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

dominant_emotion = None
emotion_history = []

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face = frame[y:y + h, x:x + w]

            try:
                result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
                emotion = result[0]['dominant_emotion']
                emotion_history.append(emotion)

                # Use the most frequent emotion in the last 10 frames
                if len(emotion_history) > 10:
                    emotion_history.pop(0)
                dominant_emotion = max(set(emotion_history), key=emotion_history.count)

                cv2.putText(frame, f"Emotion: {dominant_emotion}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            except Exception as e:
                print(f"Error in emotion detection: {e}")

        cv2.imshow('Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()

    if dominant_emotion:
        print(f"Detected Emotion: {dominant_emotion}")
        recommendations = get_youtube_recommendations(dominant_emotion)

        print("\nRecommended Songs:")
        for i, song in enumerate(recommendations, start=1):
            print(f"{i}. {song['title']} - {song['url']}")

        if recommendations:
            webbrowser.open(recommendations[0]['url'])
    else:
        print("No emotion detected.")