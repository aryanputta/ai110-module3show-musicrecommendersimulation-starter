"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from recommender import load_songs, recommend_songs

SONGS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# ── User profiles ────────────────────────────────────────────────────────────

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.80,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "valence": 0.58,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "valence": 0.35,
    },
    "Moody Late-Night Synthwave": {
        "genre": "synthwave",
        "mood": "moody",
        "energy": 0.78,
        "valence": 0.50,
    },
}


def print_profile_results(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Print a formatted recommendation block for one user profile."""
    separator = "─" * 52
    print(f"\n{'═' * 52}")
    print(f"  Profile : {profile_name}")
    print(f"  Prefs   : genre={user_prefs.get('genre')}, "
          f"mood={user_prefs.get('mood')}, "
          f"energy={user_prefs.get('energy')}")
    print(f"{'═' * 52}")

    results = recommend_songs(user_prefs, songs, k=5)
    if not results:
        print("  No recommendations returned.")
        return

    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why  : {explanation}")

    print(f"\n{separator}")


def main() -> None:
    songs = load_songs(SONGS_PATH)
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        print_profile_results(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
