# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and YouTube build a model of your taste from everything you do — skips, replays, likes, time of day — and use that signal to surface content you haven't heard yet. Most production systems combine two approaches: collaborative filtering (finding users who behave like you and borrowing their taste) and content-based filtering (matching song attributes directly to your preferences). This simulation focuses on the content-based side. Rather than tracking user behavior over time, it takes a snapshot of what a user says they want — their preferred genre, mood, energy level, and whether they lean acoustic — and scores every song in the catalog against that profile. The goal is to surface the most relevant match, not just the most popular song. Each feature is weighted differently based on how much it actually distinguishes songs from one another, so mood and energy carry more influence than valence, which has a narrower range across the catalog.

### Song Features

Each `Song` object stores the following attributes used in scoring:

| Feature | Type | Role in scoring |
|---|---|---|
| `genre` | string | Categorical match against user's preferred genre |
| `mood` | string | Matched against user's list of preferred moods |
| `energy` | float (0–1) | Gaussian proximity to user's target energy level |
| `tempo_bpm` | float | Stored on the song; not directly scored (correlated with energy) |
| `valence` | float (0–1) | Gaussian proximity to user's target valence |
| `danceability` | float (0–1) | Gaussian proximity to user's target danceability |
| `acousticness` | float (0–1) | Directional score based on whether user prefers acoustic or not |

### UserProfile Fields

Each `UserProfile` stores what the user wants:

| Field | Type | Maps to |
|---|---|---|
| `favorite_genre` | string | Matched against `song.genre` |
| `favorite_moods` | List[str] | Matched against `song.mood` — any match scores 1.0 |
| `target_energy` | float (0–1) | Gaussian proximity against `song.energy` |
| `likes_acoustic` | bool | If True, rewards high `acousticness`; if False, rewards low |
| `target_valence` | float (0–1) | Gaussian proximity against `song.valence` |
| `target_danceability` | float (0–1) | Gaussian proximity against `song.danceability` |

### Scoring and Ranking

Each song receives a weighted score between 0 and 1:

- **Categorical features** (mood, genre) use binary matching: 1.0 for a match, 0.0 otherwise
- **Numeric features** (energy) use Gaussian proximity: songs closer to the user's target score higher, with a smooth dropoff the further they are
- **Directional features** (acousticness) score based on alignment with a boolean preference rather than proximity to a target value

Feature weights reflect how much each feature distinguishes songs in the catalog:

```
score = 0.25 × mood_match + 0.20 × energy_proximity + 0.20 × acoustic_alignment + 0.15 × genre_match + 0.12 × danceability_proximity + 0.08 × valence_proximity
```

Songs are ranked by score descending and the top `k` are returned.

---

### Algorithm Recipe

This is the step-by-step process the system follows every time it runs:

1. **Load the catalog** — Read `songs.csv` and parse every row into a `Song` object. All 18 songs are held in memory.
2. **Read the user profile** — Pull genre, moods, target energy, acoustic preference, target valence, and target danceability from `user_prefs`.
3. **Score every song** — For each song, run it through 6 independent judges and sum their weighted outputs:
   - **Mood (×0.25):** Is `song.mood` in the user's mood list? → `1.0` or `0.0`
   - **Energy (×0.20):** Gaussian proximity between `song.energy` and `target_energy` — perfect match = 1.0, drops off smoothly with distance
   - **Acousticness (×0.20):** If `likes_acoustic=True` → reward `song.acousticness`; if `False` → reward `1 − song.acousticness`
   - **Genre (×0.15):** Does `song.genre` match `favorite_genre`? → `1.0` or `0.0`
   - **Danceability (×0.12):** Gaussian proximity between `song.danceability` and `target_danceability`
   - **Valence (×0.08):** Gaussian proximity between `song.valence` and `target_valence`
4. **Rank** — Sort all scored songs from highest to lowest score.
5. **Slice** — Return the top `k` songs (default 5).
6. **Explain** — For each result, generate a human-readable string reporting which judges fired and what the key scores were.

The Gaussian proximity formula used for numeric features:

```
gaussian(song_val, target) = exp( -((song_val - target)² / (2 × σ²)) )   where σ = 0.2
```

---

### System Flowchart

The diagram below shows how a single song moves from the CSV file to the final ranked output:

```mermaid
flowchart TD
    A([songs.csv]) --> B[load_songs\nparse each row into a Song object]
    B --> C[(Song catalog\n18 songs in memory)]

    U([user_prefs dict]) --> V[Build UserProfile\ngenre · moods · energy\nacoustic · valence · danceability]

    C --> D
    V --> D

    D[Pick one Song from catalog] --> E

    subgraph E [score_song — 6 judges]
        J1[Mood × 0.25\nsong.mood in user.favorite_moods?]
        J2[Energy × 0.20\nGaussian distance vs target_energy]
        J3[Acoustic × 0.20\nlikes_acoustic → directional score]
        J4[Genre × 0.15\nsong.genre == favorite_genre?]
        J5[Danceability × 0.12\nGaussian distance vs target_danceability]
        J6[Valence × 0.08\nGaussian distance vs target_valence]
    end

    E --> F[Sum weighted scores\nfinal_score between 0.0 and 1.0]
    F --> G{More songs\nin catalog?}
    G -- Yes --> D
    G -- No --> H[Sort all songs by score descending]
    H --> I[Slice top k results]
    I --> J[explain_recommendation for each song]
    J --> K([Printed output\nTitle · Score · Because...])
```

---

### Known Biases and Limitations

- **Mood dominance:** With a weight of 0.25, mood is the single strongest signal. A rock song that matches the user's mood will outscore a hip-hop song that only matches genre — even if the user strongly prefers hip-hop. This is intentional but worth knowing.
- **Genre is a hard filter at low weight:** Genre uses binary matching (1.0 or 0.0) but carries only 0.15 weight. A song in a different genre can still score well on all other features and appear in the top 5. This creates cross-genre recommendations that may feel unexpected.
- **No catalog diversity enforcement:** The system can return 5 songs by the same artist or in the same genre if they all score highly. There is no diversity injection.
- **Acoustic preference is one-directional:** `likes_acoustic` is a boolean, not a target value. A user who wants a *slightly* acoustic sound gets the same scoring function as one who wants *fully* acoustic.
- **Small catalog amplifies bias:** With only 18 songs, a missing mood-genre combination (e.g., no hip-hop song with mood "intense") means the top result may not actually match what the user wants — even with a perfect profile.

---

### Sample Terminal Output

Profile used: Nine Vicious (hip-hop, moods: intense + uplifting, energy: 0.85, no acoustic)

```
Loaded songs: 18

============================================================
  TOP RECOMMENDATIONS
  Profile: hip-hop | moods: ['intense', 'uplifting']
============================================================

#1  Gold Chain Dreams  --  Verse Theory
    Genre: hip-hop  |  Mood: uplifting  |  Score: 0.94
    Breakdown:
      • Mood matched (uplifting): +0.25
      • Energy proximity (0.78 vs 0.85): +0.19
      • Acoustic alignment (0.12): +0.18
      • Genre matched (hip-hop): +0.15
      • Danceability proximity (0.84 vs 0.82): +0.12
      • Valence proximity (0.85 vs 0.68): +0.06

#2  Gym Hero  --  Max Pulse
    Genre: pop  |  Mood: intense  |  Score: 0.81
    Breakdown:
      • Mood matched (intense): +0.25
      • Energy proximity (0.93 vs 0.85): +0.18
      • Acoustic alignment (0.05): +0.19
      • Genre no match (pop != hip-hop): +0.00
      • Danceability proximity (0.88 vs 0.82): +0.11
      • Valence proximity (0.77 vs 0.68): +0.07

#3  Storm Runner  --  Voltline
    Genre: rock  |  Mood: intense  |  Score: 0.76
    Breakdown:
      • Mood matched (intense): +0.25
      • Energy proximity (0.91 vs 0.85): +0.19
      • Acoustic alignment (0.10): +0.18
      • Genre no match (rock != hip-hop): +0.00
      • Danceability proximity (0.66 vs 0.82): +0.09
      • Valence proximity (0.48 vs 0.68): +0.05

#4  Sunrise City  --  Neon Echo
    Genre: pop  |  Mood: happy  |  Score: 0.54
    Breakdown:
      • Mood no match (happy not in ['intense', 'uplifting']): +0.00
      • Energy proximity (0.82 vs 0.85): +0.20
      • Acoustic alignment (0.18): +0.16
      • Genre no match (pop != hip-hop): +0.00
      • Danceability proximity (0.79 vs 0.82): +0.12
      • Valence proximity (0.84 vs 0.68): +0.06

#5  Neon Surge  --  Gridlock
    Genre: edm  |  Mood: euphoric  |  Score: 0.51
    Breakdown:
      • Mood no match (euphoric not in ['intense', 'uplifting']): +0.00
      • Energy proximity (0.95 vs 0.85): +0.18
      • Acoustic alignment (0.06): +0.19
      • Genre no match (edm != hip-hop): +0.00
      • Danceability proximity (0.93 vs 0.82): +0.10
      • Valence proximity (0.91 vs 0.68): +0.04

============================================================
```

---

### System Evaluation — All Profiles

Six profiles were run to evaluate the recommender, including two adversarial edge cases.

#### Profile 2 — High-Energy Pop

```
============================================================
  PROFILE 2 -- High-Energy Pop
  Profile: pop | moods: ['happy', 'euphoric']
============================================================

#1  Sunrise City  --  Neon Echo
    Genre: pop  |  Mood: happy  |  Score: 0.94
    Breakdown:
      • Mood matched (happy): +0.25
      • Energy proximity (0.82 vs 0.90): +0.18
      • Acoustic alignment (0.18): +0.16
      • Genre matched (pop): +0.15
      • Danceability proximity (0.79 vs 0.88): +0.11
      • Valence proximity (0.84 vs 0.85): +0.08

#2  Neon Surge  --  Gridlock
    Genre: edm  |  Mood: euphoric  |  Score: 0.82
    Breakdown:
      • Mood matched (euphoric): +0.25
      • Energy proximity (0.95 vs 0.90): +0.19
      • Acoustic alignment (0.06): +0.19
      • Genre no match (edm != pop): +0.00
      • Danceability proximity (0.93 vs 0.88): +0.12
      • Valence proximity (0.91 vs 0.85): +0.08

#3  Gym Hero  --  Max Pulse
    Genre: pop  |  Mood: intense  |  Score: 0.73
    Breakdown:
      • Mood no match (intense not in ['happy', 'euphoric']): +0.00
      • Energy proximity (0.93 vs 0.90): +0.20
      • Acoustic alignment (0.05): +0.19
      • Genre matched (pop): +0.15
      • Danceability proximity (0.88 vs 0.88): +0.12
      • Valence proximity (0.77 vs 0.85): +0.07

#4  Rooftop Lights  --  Indigo Parade
    Genre: indie pop  |  Mood: happy  |  Score: 0.73
    Breakdown:
      • Mood matched (happy): +0.25
      • Energy proximity (0.76 vs 0.90): +0.16
      • Acoustic alignment (0.35): +0.13
      • Genre no match (indie pop != pop): +0.00
      • Danceability proximity (0.82 vs 0.88): +0.11
      • Valence proximity (0.81 vs 0.85): +0.08

#5  Gold Chain Dreams  --  Verse Theory
    Genre: hip-hop  |  Mood: uplifting  |  Score: 0.54
    Breakdown:
      • Mood no match (uplifting not in ['happy', 'euphoric']): +0.00
      • Energy proximity (0.78 vs 0.90): +0.17
      • Acoustic alignment (0.12): +0.18
      • Genre no match (hip-hop != pop): +0.00
      • Danceability proximity (0.84 vs 0.88): +0.12
      • Valence proximity (0.85 vs 0.85): +0.08

============================================================
```

#### Profile 3 — Chill Lofi

```
============================================================
  PROFILE 3 -- Chill Lofi
  Profile: lofi | moods: ['chill', 'focused']
============================================================

#1  Library Rain  --  Paper Lanterns
    Genre: lofi  |  Mood: chill  |  Score: 0.97
    Breakdown:
      • Mood matched (chill): +0.25
      • Energy proximity (0.35 vs 0.38): +0.20
      • Acoustic alignment (0.86): +0.17
      • Genre matched (lofi): +0.15
      • Danceability proximity (0.58 vs 0.55): +0.12
      • Valence proximity (0.60 vs 0.58): +0.08

#2  Focus Flow  --  LoRoom
    Genre: lofi  |  Mood: focused  |  Score: 0.95
    Breakdown:
      • Mood matched (focused): +0.25
      • Energy proximity (0.40 vs 0.38): +0.20
      • Acoustic alignment (0.78): +0.16
      • Genre matched (lofi): +0.15
      • Danceability proximity (0.60 vs 0.55): +0.12
      • Valence proximity (0.59 vs 0.58): +0.08

#3  Midnight Coding  --  LoRoom
    Genre: lofi  |  Mood: chill  |  Score: 0.93
    Breakdown:
      • Mood matched (chill): +0.25
      • Energy proximity (0.42 vs 0.38): +0.20
      • Acoustic alignment (0.71): +0.14
      • Genre matched (lofi): +0.15
      • Danceability proximity (0.62 vs 0.55): +0.11
      • Valence proximity (0.56 vs 0.58): +0.08

#4  Spacewalk Thoughts  --  Orbit Bloom
    Genre: ambient  |  Mood: chill  |  Score: 0.78
    Breakdown:
      • Mood matched (chill): +0.25
      • Energy proximity (0.28 vs 0.38): +0.18
      • Acoustic alignment (0.92): +0.18
      • Genre no match (ambient != lofi): +0.00
      • Danceability proximity (0.41 vs 0.55): +0.09
      • Valence proximity (0.65 vs 0.58): +0.08

#5  Coffee Shop Stories  --  Slow Stereo
    Genre: jazz  |  Mood: relaxed  |  Score: 0.56
    Breakdown:
      • Mood no match (relaxed not in ['chill', 'focused']): +0.00
      • Energy proximity (0.37 vs 0.38): +0.20
      • Acoustic alignment (0.89): +0.18
      • Genre no match (jazz != lofi): +0.00
      • Danceability proximity (0.54 vs 0.55): +0.12
      • Valence proximity (0.71 vs 0.58): +0.06

============================================================
```

#### Profile 4 — Deep Intense Rock

```
============================================================
  PROFILE 4 -- Deep Intense Rock
  Profile: rock | moods: ['intense', 'angry']
============================================================

#1  Storm Runner  --  Voltline
    Genre: rock  |  Mood: intense  |  Score: 0.97
    Breakdown:
      • Mood matched (intense): +0.25
      • Energy proximity (0.91 vs 0.93): +0.20
      • Acoustic alignment (0.10): +0.18
      • Genre matched (rock): +0.15
      • Danceability proximity (0.66 vs 0.65): +0.12
      • Valence proximity (0.48 vs 0.40): +0.07

#2  Collapse the Sky  --  Iron Fault
    Genre: metal  |  Mood: angry  |  Score: 0.81
    Breakdown:
      • Mood matched (angry): +0.25
      • Energy proximity (0.97 vs 0.93): +0.20
      • Acoustic alignment (0.04): +0.19
      • Genre no match (metal != rock): +0.00
      • Danceability proximity (0.52 vs 0.65): +0.10
      • Valence proximity (0.30 vs 0.40): +0.07

#3  Gym Hero  --  Max Pulse
    Genre: pop  |  Mood: intense  |  Score: 0.72
    Breakdown:
      • Mood matched (intense): +0.25
      • Energy proximity (0.93 vs 0.93): +0.20
      • Acoustic alignment (0.05): +0.19
      • Genre no match (pop != rock): +0.00
      • Danceability proximity (0.88 vs 0.65): +0.06
      • Valence proximity (0.77 vs 0.40): +0.01

#4  Night Drive Loop  --  Neon Echo
    Genre: synthwave  |  Mood: moody  |  Score: 0.47
    Breakdown:
      • Mood no match (moody not in ['intense', 'angry']): +0.00
      • Energy proximity (0.75 vs 0.93): +0.13
      • Acoustic alignment (0.22): +0.16
      • Genre no match (synthwave != rock): +0.00
      • Danceability proximity (0.73 vs 0.65): +0.11
      • Valence proximity (0.49 vs 0.40): +0.07

#5  Sunrise City  --  Neon Echo
    Genre: pop  |  Mood: happy  |  Score: 0.44
    Breakdown:
      • Mood no match (happy not in ['intense', 'angry']): +0.00
      • Energy proximity (0.82 vs 0.93): +0.17
      • Acoustic alignment (0.18): +0.16
      • Genre no match (pop != rock): +0.00
      • Danceability proximity (0.79 vs 0.65): +0.09
      • Valence proximity (0.84 vs 0.40): +0.01

============================================================
```

#### Profile 5 (Edge Case) — Conflicted Listener (high energy + sad mood)

**What we expected to see:** A user who wants `energy: 0.90` but `moods: ['sad', 'melancholic']` should expose tension in the system — sad songs tend to be low energy, so mood and energy judges will pull in opposite directions.

**What happened:** `Hollow Hours` (soul/sad, energy=0.48) scored #1 at 0.74 because mood + genre both fired (+0.40 combined), but the energy judge only contributed +0.02. Songs with energy near 0.90 ranked #3–#5 but had zero mood match. The system resolves the conflict by always prioritizing the highest-weight feature (mood) over numeric proximity.

```
============================================================
  PROFILE 5 (EDGE CASE) -- Conflicted Listener
  Profile: soul | moods: ['sad', 'melancholic']
============================================================

#1  Hollow Hours  --  Marene
    Genre: soul  |  Mood: sad  |  Score: 0.74
    Breakdown:
      • Mood matched (sad): +0.25
      • Energy proximity (0.48 vs 0.90): +0.02
      • Acoustic alignment (0.65): +0.13
      • Genre matched (soul): +0.15
      • Danceability proximity (0.55 vs 0.50): +0.12
      • Valence proximity (0.38 vs 0.30): +0.07

#2  Porch Light  --  Dusty Elm
    Genre: folk  |  Mood: melancholic  |  Score: 0.61
    Breakdown:
      • Mood matched (melancholic): +0.25
      • Energy proximity (0.31 vs 0.90): +0.00
      • Acoustic alignment (0.88): +0.18
      • Genre no match (folk != soul): +0.00
      • Danceability proximity (0.45 vs 0.50): +0.12
      • Valence proximity (0.44 vs 0.30): +0.06

#3  Collapse the Sky  --  Iron Fault
    Genre: metal  |  Mood: angry  |  Score: 0.40
    Breakdown:
      • Mood no match (angry not in ['sad', 'melancholic']): +0.00
      • Energy proximity (0.97 vs 0.90): +0.19
      • Acoustic alignment (0.04): +0.01
      • Genre no match (metal != soul): +0.00
      • Danceability proximity (0.52 vs 0.50): +0.12
      • Valence proximity (0.30 vs 0.30): +0.08

#4  Storm Runner  --  Voltline
    Genre: rock  |  Mood: intense  |  Score: 0.36
    Breakdown:
      • Mood no match (intense not in ['sad', 'melancholic']): +0.00
      • Energy proximity (0.91 vs 0.90): +0.20
      • Acoustic alignment (0.10): +0.02
      • Genre no match (rock != soul): +0.00
      • Danceability proximity (0.66 vs 0.50): +0.09
      • Valence proximity (0.48 vs 0.30): +0.05

#5  Library Rain  --  Paper Lanterns
    Genre: lofi  |  Mood: chill  |  Score: 0.31
    Breakdown:
      • Mood no match (chill not in ['sad', 'melancholic']): +0.00
      • Energy proximity (0.35 vs 0.90): +0.00
      • Acoustic alignment (0.86): +0.17
      • Genre no match (lofi != soul): +0.00
      • Danceability proximity (0.58 vs 0.50): +0.11
      • Valence proximity (0.60 vs 0.30): +0.03

============================================================
```

#### Profile 6 (Edge Case) — Genre Ghost (jazz fan who wants intense mood)

**What we expected to see:** No jazz song in the catalog has `mood: intense` or `mood: euphoric`, so genre and mood can never both fire for the same song. The system should be "tricked" into recommending non-jazz songs.

**What happened:** Confirmed — the genre score (+0.15) never fired for any top-5 result. The entire top 5 is non-jazz. The system is essentially a mood+energy recommender at this point, genre is invisible. This exposes a real limitation: with only 18 songs, missing genre-mood combinations mean the genre weight is wasted.

```
============================================================
  PROFILE 6 (EDGE CASE) -- Genre Ghost (Jazz + Intense)
  Profile: jazz | moods: ['intense', 'euphoric']
============================================================

#1  Gym Hero  --  Max Pulse
    Genre: pop  |  Mood: intense  |  Score: 0.77
    Breakdown:
      • Mood matched (intense): +0.25
      • Energy proximity (0.93 vs 0.80): +0.16
      • Acoustic alignment (0.05): +0.19
      • Genre no match (pop != jazz): +0.00
      • Danceability proximity (0.88 vs 0.75): +0.10
      • Valence proximity (0.77 vs 0.70): +0.08

#2  Storm Runner  --  Voltline
    Genre: rock  |  Mood: intense  |  Score: 0.75
    Breakdown:
      • Mood matched (intense): +0.25
      • Energy proximity (0.91 vs 0.80): +0.17
      • Acoustic alignment (0.10): +0.18
      • Genre no match (rock != jazz): +0.00
      • Danceability proximity (0.66 vs 0.75): +0.11
      • Valence proximity (0.48 vs 0.70): +0.04

#3  Neon Surge  --  Gridlock
    Genre: edm  |  Mood: euphoric  |  Score: 0.72
    Breakdown:
      • Mood matched (euphoric): +0.25
      • Energy proximity (0.95 vs 0.80): +0.15
      • Acoustic alignment (0.06): +0.19
      • Genre no match (edm != jazz): +0.00
      • Danceability proximity (0.93 vs 0.75): +0.08
      • Valence proximity (0.91 vs 0.70): +0.05

#4  Gold Chain Dreams  --  Verse Theory
    Genre: hip-hop  |  Mood: uplifting  |  Score: 0.54
    Breakdown:
      • Mood no match (uplifting not in ['intense', 'euphoric']): +0.00
      • Energy proximity (0.78 vs 0.80): +0.20
      • Acoustic alignment (0.12): +0.18
      • Genre no match (hip-hop != jazz): +0.00
      • Danceability proximity (0.84 vs 0.75): +0.11
      • Valence proximity (0.85 vs 0.70): +0.06

#5  Sunrise City  --  Neon Echo
    Genre: pop  |  Mood: happy  |  Score: 0.54
    Breakdown:
      • Mood no match (happy not in ['intense', 'euphoric']): +0.00
      • Energy proximity (0.82 vs 0.80): +0.20
      • Acoustic alignment (0.18): +0.16
      • Genre no match (pop != jazz): +0.00
      • Danceability proximity (0.79 vs 0.75): +0.12
      • Valence proximity (0.84 vs 0.70): +0.06

============================================================
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Do the Results Feel Right? (Musical Intuition Check)

**Profile 3 — Chill Lofi** produced the most intuitive results. All three lofi songs in the catalog (`Library Rain`, `Focus Flow`, `Midnight Coding`) ranked #1–#3 with scores 0.97, 0.95, and 0.93. Every judge fired correctly — mood matched, energy was close, acousticness rewarded high-acoustic songs. This felt exactly right: if you're studying late at night and want lofi, those are exactly the songs you'd want. `#4 Spacewalk Thoughts` (ambient/chill) also made sense as a genre-adjacent recommendation.

**Profile 1 — Nine Vicious** also felt right. `Gold Chain Dreams` is the only hip-hop song with mood `uplifting`, so it correctly surfaced first. `Gym Hero` (pop/intense) at #2 felt like a fair cross-genre recommendation — it shares the energy and vibe even if the genre label is different. Real Spotify does this too.

**Profile 4 — Deep Intense Rock** felt slightly off at #3. `Gym Hero` (pop/intense, energy=0.93) outscored every non-rock option because its energy and acousticness were near-perfect matches — even though a rock fan asking for "angry" songs probably doesn't want a pop gym track. The system has no concept of genre family proximity.

---

### Why Does Gold Chain Dreams Rank #1 for the Nine Vicious Profile?

`Gold Chain Dreams` (hip-hop, uplifting, energy=0.78) scored **0.94** — the highest possible for this catalog and profile. Here's exactly why each judge contributed:

| Judge | Song value | User target | Contribution | Why |
|---|---|---|---|---|
| Mood (×0.25) | uplifting | ['intense', 'uplifting'] | **+0.25** | Exact match in mood list — full weight fires |
| Energy (×0.20) | 0.78 | 0.85 | **+0.19** | Gaussian: distance = 0.07, near-perfect proximity |
| Acousticness (×0.20) | 0.12 | False (no acoustic) | **+0.18** | `1 - 0.12 = 0.88` acoustic score, user dislikes acoustic |
| Genre (×0.15) | hip-hop | hip-hop | **+0.15** | Exact genre match — full weight fires |
| Danceability (×0.12) | 0.84 | 0.82 | **+0.12** | Distance = 0.02, essentially perfect |
| Valence (×0.08) | 0.85 | 0.68 | **+0.06** | Distance = 0.17, Gaussian score reduced but still contributes |

All 6 judges contributed positively. It's the only song in the catalog where mood AND genre both fire together for this profile — that combination (+0.40 combined) is nearly impossible to beat even with perfect numeric scores on other features.

---

### Recurring Song Problem — Gym Hero Shows Up Everywhere

After running all 6 profiles, `Gym Hero` (pop/intense, energy=0.93, acousticness=0.05) appeared in **4 out of 6** top-5 lists. `Storm Runner` and `Sunrise City` each appeared in 4 as well.

**Why Gym Hero keeps appearing:**
- `energy=0.93` is one of the highest in the catalog — it scores near-perfectly for any high-energy profile
- `acousticness=0.05` is the second-lowest in the catalog — it earns near-maximum acoustic alignment for every user who sets `likes_acoustic=False`
- `mood=intense` matches a wide range of profiles
- These three features together = a floor score of roughly 0.50–0.60 before genre or danceability even fire

**Is the genre weight too strong or too weak?** Genre weight is actually fine at 0.15 — the problem is the **catalog is too small**. With only 1 rock song, 1 hip-hop song, and 1 metal song, a pop song at extreme feature values (high energy, low acoustic) will always leak into non-pop results. A larger catalog with more genre diversity would naturally push genre-mismatched songs further down the list.

---

### Experiment A — Weight Shift (energy ×2, genre ÷2)

**Change made:** `energy: 0.20 → 0.40`, `genre: 0.15 → 0.075`. All other weights unchanged. Weights summed to 1.125, so scores slightly exceeded 1.0 — expected and acceptable for a sensitivity test.

**What changed:**
- Genre match dropped from a +0.15 bonus to +0.075 — half the reward for matching the user's preferred genre
- Energy proximity now contributes up to +0.40 per song, dominating the score
- Top-5 order stayed the same for most profiles — rankings were already energy-driven

**What stayed the same:** Profile 1 (Nine Vicious) and Chill Lofi kept the same exact order. The top song didn't change for any profile.

**Verdict — more different, not more accurate.** Doubling energy made the system care almost exclusively about how intense a song feels. A user who asks for hip-hop gets essentially the same results as one who asks for rock — genre barely distinguishes anything at 0.075. The original 0.20 / 0.15 balance was more intentional and produced more genre-sensitive results.

---

### Experiment B — Feature Removal (mood disabled)

**Change made:** Mood score hard-set to 0.0 for every song. The 0.25 weight was effectively dead weight.

**What changed:**
- Profile 2 (High-Energy Pop): `Gym Hero` jumped to #1, bumping `Sunrise City` down — Gym Hero's better energy proximity (+0.20) overtook Sunrise City once mood stopped rewarding the happy match
- All scores compressed — max score dropped from 0.97 to ~0.73 since 0.25 weight was gone
- Songs with wrong mood but perfect numeric scores climbed the rankings

**Verdict — more different, not more accurate.** Without mood, the system rewards *how a song sounds* over *how the user described what they want*. Mood is the highest-weight feature for a reason — it's the most direct signal of user intent. Removing it made results feel generic and less personal.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

