import os
import requests
import base64
import random
from typing import List, Dict, Any

def get_tmdb_recommendations(mood: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Fetches movie recommendations from TMDB based on mood.
    """
    if not api_key or api_key == "your_tmdb_api_key_here":
        return []

    # Map internal mood to TMDB Genre IDs
    # Comedy: 35, Animation: 16, Drama: 18, Romance: 10749, Family: 10751, Documentary: 99
    genre_map = {
        "Çok Mutlu": "35,16",       # Comedy, Animation
        "Mutlu": "35",              # Comedy
        "Keyifli": "10751,16,99",   # Family, Animation, Documentary
        "Melankolik": "18,99",      # Drama, Documentary
        "Üzgün": "18,10749"         # Drama, Romance
    }

    genres = genre_map.get(mood, "35") # Default to Comedy

    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": api_key,
        "with_genres": genres,
        "sort_by": "popularity.desc",
        "language": "tr-TR", # Turkish results
        "page": 1
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            # Shuffle and pick top 5
            random.shuffle(results)
            recommendations = []

            for item in results[:5]:
                poster_path = item.get("poster_path")
                image_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

                recommendations.append({
                    "title": item.get("title"),
                    "description": item.get("overview"),
                    "image_url": image_url,
                    "source": "TMDB"
                })
            return recommendations
    except Exception as e:
        print(f"TMDB API Error: {e}")

    return []

def get_spotify_token(client_id: str, client_secret: str) -> str:
    """
    Get Spotify Access Token using Client Credentials Flow.
    """
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(auth_url, headers=headers, data=data, timeout=5)
        if response.status_code == 200:
            return response.json().get("access_token")
    except Exception as e:
        print(f"Spotify Auth Error: {e}")
    return None

def get_spotify_recommendations(mood: str, client_id: str, client_secret: str) -> List[Dict[str, Any]]:
    """
    Fetches music recommendations from Spotify.
    """
    if not client_id or not client_secret or "your_spotify" in client_id:
        return []

    token = get_spotify_token(client_id, client_secret)
    if not token:
        return []

    # Map mood to search queries or seed genres
    mood_queries = {
        "Çok Mutlu": "happy upbeat pop",
        "Mutlu": "happy hits",
        "Keyifli": "chill hits",
        "Melankolik": "melancholy piano",
        "Üzgün": "sad acoustic"
    }

    query = mood_queries.get(mood, "pop")
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 10,
        "market": "TR"
    }

    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get("tracks", {}).get("items", [])

            random.shuffle(tracks)
            recommendations = []

            for track in tracks[:5]:
                album = track.get("album", {})
                images = album.get("images", [])
                image_url = images[0]["url"] if images else None

                artists = ", ".join([a["name"] for a in track.get("artists", [])])

                recommendations.append({
                    "title": track.get("name"),
                    "subtitle": artists, # Artist name as subtitle
                    "image_url": image_url,
                    "preview_url": track.get("preview_url"),
                    "source": "Spotify"
                })
            return recommendations
    except Exception as e:
        print(f"Spotify API Error: {e}")

    return []

def get_google_books_recommendations(mood: str, api_key: str = None) -> List[Dict[str, Any]]:
    """
    Fetches book recommendations from Google Books.
    """
    # Map mood to book categories/queries
    mood_queries = {
        "Çok Mutlu": "subject:comedy",
        "Mutlu": "subject:humor",
        "Keyifli": "subject:adventure",
        "Melankolik": "subject:poetry",
        "Üzgün": "subject:drama"
    }

    query = mood_queries.get(mood, "subject:fiction")
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": 10,
        "langRestrict": "tr", # Try to get Turkish books if available, or just standard results
        "orderBy": "relevance"
    }

    if api_key and "your_google" not in api_key:
        params["key"] = api_key

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])

            random.shuffle(items)
            recommendations = []

            for item in items[:5]:
                info = item.get("volumeInfo", {})
                images = info.get("imageLinks", {})
                image_url = images.get("thumbnail")

                if image_url:
                    # Fix http to https for images
                    image_url = image_url.replace("http://", "https://")

                authors = ", ".join(info.get("authors", []))

                recommendations.append({
                    "title": info.get("title"),
                    "subtitle": authors,
                    "image_url": image_url,
                    "description": info.get("description"),
                    "source": "GoogleBooks"
                })
            return recommendations
    except Exception as e:
        print(f"Google Books API Error: {e}")

    return []
