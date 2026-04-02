import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper around the scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dicts = [
            {
                "id": s.id, "title": s.title, "artist": s.artist,
                "genre": s.genre, "mood": s.mood, "energy": s.energy,
                "tempo_bpm": s.tempo_bpm, "valence": s.valence,
                "danceability": s.danceability, "acousticness": s.acousticness,
            }
            for s in self.songs
        ]
        ranked = recommend_songs(user_prefs, song_dicts, k)
        id_to_song = {s.id: s for s in self.songs}
        return [id_to_song[r[0]["id"]] for r in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "id": song.id, "title": song.title, "artist": song.artist,
            "genre": song.genre, "mood": song.mood, "energy": song.energy,
            "tempo_bpm": song.tempo_bpm, "valence": song.valence,
            "danceability": song.danceability, "acousticness": song.acousticness,
        }
        _, _, explanation = score_song(user_prefs, song_dict)
        return explanation


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[Dict, float, str]:
    """
    Score a single song against user preferences.

    Scoring recipe:
      +2.0  genre match
      +1.5  mood match
      +1.0  energy proximity  (1 - |song_energy - target_energy|)
      +0.5  valence proximity (1 - |song_valence - target_valence|)  if provided
      +0.75 acousticness bonus when user likes_acoustic and song acousticness > 0.5

    Returns (song, score, reasons_string).
    """
    score = 0.0
    reasons = []

    # Genre match
    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Energy proximity — rewards songs close to the user's target energy
    target_energy = user_prefs.get("energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_points = round(1.0 * (1.0 - energy_gap), 3)
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points:.2f})")

    # Valence proximity — only applied when the user supplies a target_valence
    if "valence" in user_prefs:
        target_valence = user_prefs["valence"]
        valence_gap = abs(song["valence"] - target_valence)
        valence_points = round(0.5 * (1.0 - valence_gap), 3)
        score += valence_points
        reasons.append(f"valence proximity (+{valence_points:.2f})")

    # Acousticness bonus
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.5:
        score += 0.75
        reasons.append("acoustic preference match (+0.75)")

    explanation = ", ".join(reasons) if reasons else "no strong matches"
    return song, round(score, 3), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Score every song and return the top-k results sorted highest score first.

    Uses sorted() so the original songs list is not mutated.
    Returns a list of (song_dict, score, explanation) tuples.
    """
    scored = [score_song(user_prefs, song) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
