# Model Card — VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is designed to suggest 3–5 songs from a small catalog based on a user's stated preference for genre, mood, energy level, and optionally acoustic sound and valence. It was built for classroom exploration of how recommendation systems work at a conceptual level.

It is not intended for real users, real products, or any context where the quality or fairness of recommendations carries meaningful consequences.

---

## 3. How the Model Works

Every song in the catalog is given a score based on how closely it matches what the user said they want.

Two types of features are considered. Categorical features (genre and mood) produce a fixed bonus when they match exactly — genre is worth the most because it reflects the broadest category of taste. Numerical features (energy and valence) are scored by proximity: a song that is *close* to the user's target gets a high score; a song that is far away gets a low score. This means the system does not simply reward loud or upbeat songs — it rewards songs that are *the right distance* from wherever the user wants to be.

All 20 songs are scored this way, then sorted from highest to lowest. The top songs are returned with a short note explaining which factors contributed to the score.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. Ten songs were included in the starter file; ten more were added to improve genre diversity.

Genres represented: pop, indie pop, lofi, rock, metal, edm, ambient, jazz, synthwave, hip-hop, folk, country, r&b.

Moods represented: happy, chill, intense, relaxed, focused, moody.

Each song has nine attributes: genre, mood, energy (0–1), tempo_bpm, valence (0–1), danceability (0–1), and acousticness (0–1).

Gaps in the data: there are no classical songs, no songs with mood labels like "sad" or "nostalgic," and only one song tagged as "rock." The dataset reflects a Western popular music bias and skews toward electronic and low-energy categories.

---

## 5. Strengths

The system works well for profiles that align cleanly with well-represented genres. A "Chill Lofi" user receives results that feel immediately right — three lofi songs in the top four, all with matching mood and energy close to target. The explanation string attached to each result makes the scoring fully transparent, which is rare in real recommender systems.

The continuous energy scoring is a genuine strength: songs are not just rewarded for being loud or quiet but for being *close* to what the user specified. This means two very different users (one wanting very low energy, one wanting very high energy) will receive different results even if their genre and mood preferences overlap.

---

## 6. Limitations and Bias

**Catalog size bias:** Rock has only one song in the catalog. The rock profile's top result is strong (Storm Runner, score 4.92), but positions 2–5 are filled by metal and EDM songs that do not actually match the rock genre. A user who wanted rock variety would receive a worse experience than a lofi user, purely because the data was not balanced.

**Genre string matching is brittle:** "Pop" and "Indie Pop" are treated as completely separate categories. A user who prefers pop gets zero genre-match credit for "Rooftop Lights" or "Golden Hour," even though those songs would feel natural to a pop listener.

**No diversity mechanism:** The scoring logic always picks the closest songs, which means the top-5 for Chill Lofi includes three songs by the same artist (LoRoom). A real platform would add a diversity penalty to surface variety.

**Contradictory preferences produce low-quality results silently:** When a user specifies energy 0.9 and mood "chill," no song satisfies both. The system returns results anyway without warning the user that no good match exists.

**Two features are unused:** Tempo and danceability are loaded but never scored. A user whose primary preference is rhythm (e.g., they want to dance) cannot express that through the current profile structure.

---

## 7. Evaluation

Four user profiles were tested:

| Profile | Top Result | Score | Felt right? |
|---|---|---|---|
| High-Energy Pop | Sunrise City | 4.95 | Yes — genre + mood + energy all matched |
| Chill Lofi | Library Rain | 5.71 | Yes — exactly the expected lofi study sound |
| Deep Intense Rock | Storm Runner | 4.92 | Yes — only one rock song existed, it ranked first |
| Moody Late-Night Synthwave | Neon Heartbeat | 4.97 | Yes — both synthwave songs rose to the top |

One experiment was run: the genre weight was reduced from 2.0 to 1.0 while energy proximity was doubled. The result was that "Gym Hero" moved into the rock profile's top-3 because of its high energy, despite being a pop song. This confirmed that the genre weight is doing important work in keeping recommendations genre-coherent.

A second test removed the mood match entirely. Without it, "Gym Hero" (intense mood) appeared in the "happy pop" profile's results at rank 3, which felt wrong. Mood was restored.

An adversarial profile was tested with energy 0.9 and mood "chill." The system returned technically valid results but peak scores barely exceeded 2.0, and none of the songs would genuinely satisfy that preference combination. No warning was shown to the user.

---

## 8. Future Work

1. **Add a "no good match" warning.** When the highest score in a ranking falls below a threshold (e.g., 2.5), the system should tell the user that its results are low-confidence rather than silently returning mediocre suggestions.

2. **Include tempo and danceability in scoring.** Adding tempo proximity as a third continuous feature would help distinguish a slow jazz listener from a fast jazz listener, and would make the "dance" use case expressible.

3. **Add a diversity penalty.** After ranking, apply a mild penalty to any song whose artist already appears in the top-k results. This would reduce the LoRoom domination in the lofi profile and produce more varied output.

---

## 9. Personal Reflection

The biggest learning moment came when the adversarial "high-energy chill" profile was tested. The expectation was that the system would fail interestingly — perhaps recommending something wildly off-base. Instead, it returned a technically valid but quietly useless list with no indication that anything was wrong. That silence revealed something important: a scoring function always produces a number, even when the question being asked makes no sense. Real recommender systems face this problem constantly. A user whose behavior is contradictory (skipping everything but never pressing dislike) gives the model conflicting signals, and the model just keeps guessing anyway.

Using AI tools during development was helpful for structuring the scoring logic and catching edge cases, but the tool's first suggestion for energy scoring simply rewarded high-energy songs regardless of what the user wanted. The proximity formula — 1 minus the absolute gap — had to be reasoned through manually before it made sense. That moment of catching the AI's assumption and replacing it with something more accurate was the clearest illustration of why human judgment remains necessary even when the code compiles and runs without errors.

What still surprises is how much the results "feel" intelligent given how simple the math is. Four additions and a sort. Yet the Chill Lofi profile reliably surfaces exactly the kind of music a person studying would put on. The apparent intelligence is entirely a product of the features chosen and the weights assigned to them — both of which are human decisions made before a single line of code runs.
