from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import os
import cv2
from fer import FER
import tempfile
import shutil

app = FastAPI()

# Veri Yükleme ve Hazırlık
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Global değişkenler
netflix_data = None
spotify_data = None
spotify_normalized_features = None
detector = None

def load_data():
    global netflix_data, spotify_data, spotify_normalized_features, detector
    try:
        print(f"Loading data from {DATA_DIR}...")
        netflix_path = os.path.join(DATA_DIR, 'netflix.csv')
        spotify_path = os.path.join(DATA_DIR, 'spotify.csv')

        if os.path.exists(netflix_path):
            netflix_data = pd.read_csv(netflix_path)
            print("Netflix data loaded.")
        else:
            print(f"File not found: {netflix_path}")

        if os.path.exists(spotify_path):
            spotify_data = pd.read_csv(spotify_path, encoding="ISO-8859-1")
            print("Spotify data loaded.")

            # Spotify özellik çıkarımı
            spotify_features_cols = ['danceability_%', 'energy_%', 'valence_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']
            if all(col in spotify_data.columns for col in spotify_features_cols):
                spotify_features = spotify_data[spotify_features_cols]
                scaler = MinMaxScaler()
                spotify_normalized_features = scaler.fit_transform(spotify_features)
            else:
                print("Warning: Missing columns in Spotify data.")
        else:
             print(f"File not found: {spotify_path}")

        # FER Dedektörünü başlat (MTCNN yerine varsayılan opencv haarcascade kullanıyoruz, daha hafif)
        print("Loading Face Detector...")
        detector = FER()
        print("Face Detector loaded.")

    except Exception as e:
        print(f"Error loading data: {e}")

# Uygulama başlarken verileri yükle
load_data()

class MoodInput(BaseModel):
    feeling: int
    activity: int
    energy: int
    social: int

def calculate_mood(feeling, activity, energy, social):
    total_score = feeling + activity + energy + social
    if total_score >= 30:
        return "Çok Mutlu"
    elif 20 <= total_score < 30:
        return "Mutlu"
    elif 15 <= total_score < 20:
        return "Keyifli"
    elif 10 <= total_score < 15:
        return "Melankolik"
    else:
        return "Üzgün"

def filter_contents(data, mood):
    if data is None:
        return pd.DataFrame()

    filtered_data = pd.DataFrame()
    # case insensitive search and handle NaN
    if mood == "Çok Mutlu" or mood == "Mutlu":
        filtered_data = data[data['listed_in'].str.contains("Comedy", na=False) | data['listed_in'].str.contains("Animation", na=False)]
    elif mood == "Üzgün":
        filtered_data = data[data['listed_in'].str.contains("Drama", na=False) | data['listed_in'].str.contains("Romantic", na=False) | data['listed_in'].str.contains("Comedy", na=False)]
    elif mood == "Keyifli":
        filtered_data = data[data['listed_in'].str.contains("Family", na=False) | data['listed_in'].str.contains("Documentary", na=False) | data['listed_in'].str.contains("Animation", na=False)]
    elif mood == "Melankolik":
        filtered_data = data[
            data['listed_in'].str.contains("Art House", na=False) | data['listed_in'].str.contains("Independent", na=False) | data['listed_in'].str.contains("Drama", na=False)]

    if filtered_data.empty:
        # Fallback if no specific filter matches or empty result, just return random sample
        return data.sample(n=min(5, len(data)))

    return filtered_data.sample(n=min(5, len(filtered_data)))

def recommend_music(data, features, mood, num_recommendations=5):
    if data is None or features is None:
        return pd.DataFrame()

    if len(features) == 0:
        return pd.DataFrame()

    seed_indices = []

    if mood in ["Çok Mutlu", "Mutlu"]:
        subset = data[(data['valence_%'] > 60) & (data['energy_%'] > 50)]
    elif mood == "Üzgün":
        subset = data[data['valence_%'] < 40]
    elif mood == "Keyifli":
        subset = data[(data['valence_%'] >= 40) & (data['valence_%'] <= 70)]
    elif mood == "Melankolik":
        subset = data[(data['energy_%'] < 50) & (data['valence_%'] < 50)]
    else:
        subset = data

    if not subset.empty:
        seed_song = subset.sample(n=1)
        seed_index = seed_song.index[0]
    else:
        seed_index = np.random.randint(0, len(features))

    cosine_similarities = cosine_similarity(features[seed_index:seed_index + 1], features)
    similar_indices = cosine_similarities.argsort().flatten()[-(num_recommendations + 1):-1]
    similar_indices = similar_indices[::-1]

    return data.iloc[similar_indices]

@app.post("/analyze-face")
def analyze_face(file: UploadFile = File(...)):
    try:
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            shutil.copyfileobj(file.file, temp_image)
            temp_image_path = temp_image.name

        # Resmi oku
        image = cv2.imread(temp_image_path)

        # Dosyayı sil (artık bellekte)
        os.remove(temp_image_path)

        if image is None:
             return {"error": "Resim okunamadı"}

        # FER ile analiz et
        emotion, score = detector.top_emotion(image)

        if not emotion:
            return {"mood": "Nötr", "mapped_mood": "Keyifli", "feeling_score": 5}

        # Duygu eşleştirmesi
        mapped_mood = "Keyifli"
        feeling_score = 5

        if emotion == "happy":
            mapped_mood = "Mutlu"
            feeling_score = 8
        elif emotion == "sad":
            mapped_mood = "Üzgün"
            feeling_score = 3
        elif emotion == "angry" or emotion == "disgust" or emotion == "fear":
             mapped_mood = "Melankolik"
             feeling_score = 2
        elif emotion == "neutral":
             mapped_mood = "Keyifli"
             feeling_score = 6
        elif emotion == "surprise":
             mapped_mood = "Çok Mutlu"
             feeling_score = 9

        return {
            "mood": emotion,
            "mapped_mood": mapped_mood,
            "feeling_score": feeling_score
        }

    except Exception as e:
        print(f"Face analysis error: {e}")
        return {"error": str(e)}

@app.post("/recommend")
def get_recommendations(input_data: MoodInput):
    mood = calculate_mood(input_data.feeling, input_data.activity, input_data.energy, input_data.social)

    films = filter_contents(netflix_data, mood)
    songs = recommend_music(spotify_data, spotify_normalized_features, mood)

    film_list = []
    if not films.empty:
        films = films.fillna("")
        film_list = films[['title', 'listed_in']].to_dict(orient='records')

    song_list = []
    if not songs.empty:
        songs = songs.fillna("")
        song_list = songs[['track_name', 'artist(s)_name']].to_dict(orient='records')

    return {
        "mood": mood,
        "films": film_list,
        "songs": song_list
    }

@app.get("/")
def read_root():
    return {"message": "MindMingle API is running. Send POST request to /recommend"}
