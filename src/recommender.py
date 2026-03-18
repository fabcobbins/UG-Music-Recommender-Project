import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_moods: List[str]
    target_energy: float
    likes_acoustic: bool
    target_valence: float
    target_danceability: float

_SIGMA: float = 0.2
_WEIGHTS: Dict[str, float] = {
    "mood":         0.25,
    "energy":       0.20,
    "acousticness": 0.20,
    "genre":        0.15,
    "danceability": 0.12,
    "valence":      0.08,
}


def _gaussian(song_val: float, target: float) -> float:
    """Gaussian proximity — returns 1.0 for perfect match, drops toward 0 as distance grows."""
    return math.exp(-((song_val - target) ** 2) / (2 * _SIGMA ** 2))


def score_song(song: Song, user: UserProfile) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user profile.

    Parameters
    ----------
    song : Song
        The song to evaluate.
    user : UserProfile
        The user's taste preferences.

    Returns
    -------
    Tuple[float, List[str]]
        (total_score, reasons) where total_score is in [0, 1]
        and reasons is a list of strings explaining each judge's contribution.
    """
    reasons: List[str] = []

    # --- Mood (0.25) — binary: any match in favorite_moods list
    mood_match = 1.0 if song.mood in user.favorite_moods else 0.0
    mood_contribution = _WEIGHTS["mood"] * mood_match
    if mood_match:
        reasons.append(f"Mood matched ({song.mood}): +{mood_contribution:.2f}")
    else:
        reasons.append(f"Mood no match ({song.mood} not in {user.favorite_moods}): +0.00")

    # --- Energy (0.20) — Gaussian proximity to target_energy
    energy_score = _gaussian(song.energy, user.target_energy)
    energy_contribution = _WEIGHTS["energy"] * energy_score
    reasons.append(f"Energy proximity ({song.energy:.2f} vs {user.target_energy:.2f}): +{energy_contribution:.2f}")

    # --- Acousticness (0.20) — directional based on likes_acoustic bool
    acoustic_score = song.acousticness if user.likes_acoustic else 1.0 - song.acousticness
    acoustic_contribution = _WEIGHTS["acousticness"] * acoustic_score
    reasons.append(f"Acoustic alignment ({song.acousticness:.2f}): +{acoustic_contribution:.2f}")

    # --- Genre (0.15) — binary: exact match
    genre_match = 1.0 if song.genre == user.favorite_genre else 0.0
    genre_contribution = _WEIGHTS["genre"] * genre_match
    if genre_match:
        reasons.append(f"Genre matched ({song.genre}): +{genre_contribution:.2f}")
    else:
        reasons.append(f"Genre no match ({song.genre} != {user.favorite_genre}): +0.00")

    # --- Danceability (0.12) — Gaussian proximity to target_danceability
    dance_score = _gaussian(song.danceability, user.target_danceability)
    dance_contribution = _WEIGHTS["danceability"] * dance_score
    reasons.append(f"Danceability proximity ({song.danceability:.2f} vs {user.target_danceability:.2f}): +{dance_contribution:.2f}")

    # --- Valence (0.08) — Gaussian proximity to target_valence
    valence_score = _gaussian(song.valence, user.target_valence)
    valence_contribution = _WEIGHTS["valence"] * valence_score
    reasons.append(f"Valence proximity ({song.valence:.2f} vs {user.target_valence:.2f}): +{valence_contribution:.2f}")

    total = (
        mood_contribution
        + energy_contribution
        + acoustic_contribution
        + genre_contribution
        + dance_contribution
        + valence_contribution
    )

    return round(total, 4), reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs      : Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
