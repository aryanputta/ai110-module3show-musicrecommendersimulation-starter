# Music Recommender Simulation

## Project Summary

A content-based music recommender was built in Python that matches songs from a catalog to a user's taste profile. Each song is scored against the user's preferred genre, mood, energy level, valence, and acoustic preference. The top-scoring songs are returned as ranked recommendations with plain-language explanations attached to each result.

---

## How The System Works

### Real-World Recommenders

Streaming platforms like Spotify and YouTube rely on two main approaches working in parallel. Collaborative filtering surfaces songs that users with similar listening histories have enjoyed — no knowledge of the audio itself is needed. Content-based filtering takes the opposite path: songs are described by measurable attributes (tempo, energy, mood) and a user's preferences are matched directly against those attributes.

This simulation focuses on content-based filtering. Because there are no other users in the dataset, songs are ranked purely by how closely their features align with the target profile.

### Features Used

Each `Song` object holds:

| Feature | Type | Role |
|---|---|---|
| `genre` | string | Primary categorical match |
| `mood` | string | Secondary categorical match |
| `energy` | float 0–1 | Proximity to user's target energy |
| `valence` | float 0–1 | Proximity to user's target positivity |
| `acousticness` | float 0–1 | Bonus when user prefers acoustic sound |
| `tempo_bpm` | float | Stored but not used in scoring (future work) |
| `danceability` | float | Stored but not used in scoring (future work) |

Each `UserProfile` stores:

- `favorite_genre` — the genre the user most prefers
- `favorite_mood` — the mood the user wants to feel
- `target_energy` — a 0–1 value representing the desired intensity
- `likes_acoustic` — a boolean for whether organic/acoustic sound is preferred
- *(optional)* `valence` — target positivity level, if supplied

### Algorithm Recipe

A score is computed for every song in the catalog:

```
score = 0

if song.genre == user.genre  →  +2.0   (genre match)
if song.mood  == user.mood   →  +1.5   (mood match)
energy_points = 1.0 × (1 − |song.energy − user.energy|)  →  up to +1.0
valence_points = 0.5 × (1 − |song.valence − user.valence|) →  up to +0.5
if user.likes_acoustic and song.acousticness > 0.5  →  +0.75
```

Genre was weighted highest because a user who wants rock rarely enjoys ambient regardless of energy. Mood was placed second because it captures the emotional context. Energy is a continuous penalty rather than a binary reward, so songs are not simply rewarded for being "loud" but for being *close* to what the user wants.

All songs are then sorted highest-to-lowest and the top-k results are returned.

### Data Flow

```
User Profile (genre, mood, energy, ...)
        │
        ▼
For every song in songs.csv:
    score_song(user_prefs, song)  →  (song, score, reasons)
        │
        ▼
sorted(all_scored, key=score, reverse=True)
        │
        ▼
Top-k Recommendations with explanations
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Mac / Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python3 -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Terminal Output Screenshots

### Profile 1 — High-Energy Pop

```
════════════════════════════════════════════════════
  Profile : High-Energy Pop
  Prefs   : genre=pop, mood=happy, energy=0.85
════════════════════════════════════════════════════

  #1  Sunrise City  —  Neon Echo
       Genre: pop | Mood: happy | Energy: 0.82
       Score: 4.95
       Why  : genre match (+2.0), mood match (+1.5), energy proximity (+0.97), valence proximity (+0.48)

  #2  Gym Hero  —  Max Pulse
       Genre: pop | Mood: intense | Energy: 0.93
       Score: 3.40
       Why  : genre match (+2.0), energy proximity (+0.92), valence proximity (+0.48)

  #3  Rooftop Lights  —  Indigo Parade
       Genre: indie pop | Mood: happy | Energy: 0.76
       Score: 2.90
       Why  : mood match (+1.5), energy proximity (+0.91), valence proximity (+0.49)
```

### Profile 2 — Chill Lofi

```
════════════════════════════════════════════════════
  Profile : Chill Lofi
  Prefs   : genre=lofi, mood=chill, energy=0.38
════════════════════════════════════════════════════

  #1  Library Rain  —  Paper Lanterns
       Genre: lofi | Mood: chill | Energy: 0.35
       Score: 5.71
       Why  : genre match (+2.0), mood match (+1.5), energy proximity (+0.97), valence proximity (+0.49), acoustic preference match (+0.75)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi | Mood: chill | Energy: 0.42
       Score: 5.70
       Why  : genre match (+2.0), mood match (+1.5), energy proximity (+0.96), valence proximity (+0.49), acoustic preference match (+0.75)
```

### Profile 3 — Deep Intense Rock

```
════════════════════════════════════════════════════
  Profile : Deep Intense Rock
  Prefs   : genre=rock, mood=intense, energy=0.92
════════════════════════════════════════════════════

  #1  Storm Runner  —  Voltline
       Genre: rock | Mood: intense | Energy: 0.91
       Score: 4.92
       Why  : genre match (+2.0), mood match (+1.5), energy proximity (+0.99), valence proximity (+0.43)

  #2  Iron Cathedral  —  Darkforge
       Genre: metal | Mood: intense | Energy: 0.94
       Score: 2.92
       Why  : mood match (+1.5), energy proximity (+0.98), valence proximity (+0.43)
```

### Profile 4 — Moody Late-Night Synthwave

```
════════════════════════════════════════════════════
  Profile : Moody Late-Night Synthwave
  Prefs   : genre=synthwave, mood=moody, energy=0.78
════════════════════════════════════════════════════

  #1  Neon Heartbeat  —  Pulse Grid
       Genre: synthwave | Mood: moody | Energy: 0.8
       Score: 4.97
       Why  : genre match (+2.0), mood match (+1.5), energy proximity (+0.98), valence proximity (+0.49)

  #2  Night Drive Loop  —  Neon Echo
       Genre: synthwave | Mood: moody | Energy: 0.75
       Score: 4.96
       Why  : genre match (+2.0), mood match (+1.5), energy proximity (+0.97), valence proximity (+0.49)
```

---

## Experiments

**Weight shift — doubling energy, halving genre:**
When the genre weight was reduced from +2.0 to +1.0 and energy proximity was doubled, high-intensity songs from non-matching genres (like "Iron Cathedral" for the rock profile) moved up significantly. The recommendations became more energetically accurate but less genre-coherent. This made the "rock" profile feel like a "loud music" profile rather than a rock one.

**Feature removal — removing the mood check:**
Removing the mood match from scoring caused "Gym Hero" (mood: intense) to appear in the "happy pop" top-5 despite its mood mismatch. This confirmed that mood was doing real work in the scoring logic, not just adding noise.

**Adversarial edge case — conflicting preferences (energy: 0.9, mood: chill):**
No song in the catalog scores above ~2.0 for this profile because high-energy songs are rarely labeled "chill." The system returned technically correct results but the top song had a score of only 2.1 — much lower than any aligned profile. This exposes a limitation: the system has no way to handle contradictory preferences gracefully.

---

## Limitations and Risks

- The catalog contains 20 songs, which is too small to serve diverse users fairly. The rock profile has only one matching song.
- Genre strings must match exactly (case-insensitive). "Indie Pop" and "Pop" are treated as completely different even though they share obvious overlap.
- The system treats all users as if they have the same scoring shape. A user who cares only about energy and nothing about genre gets the same scoring formula as one who is genre-obsessed.
- There is no diversity mechanism — the top-5 results for lofi often include 3 songs by the same artist (LoRoom).
- Tempo and danceability are stored but never used, meaning a user who wants to dance slowly has no way to express that.

---

## Reflection

See [model_card.md](model_card.md) for the full model card and personal reflection.

The most important thing learned from building this was that recommendations are not magic — they are arithmetic. A number is computed for each song, and the highest numbers win. Every apparent "intelligence" in the output traces back to a weight that was set manually. This makes the system transparent and explainable, but it also means it can only capture preferences that were anticipated when the weights were designed. Real platforms like Spotify have millions of implicit signals (skip rate, repeat plays, playlist adds) that this simulation has no access to, which is exactly why collaborative filtering exists alongside content-based approaches.
