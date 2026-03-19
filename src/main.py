"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def run_profile(songs, label: str, user_prefs: dict) -> None:
    """Print top-5 recommendations for a single user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 60)
    print(f"  {label}")
    print(f"  Profile: {user_prefs['genre']} | moods: {user_prefs['moods']}")
    print("=" * 60)

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"\n#{rank}  {song['title']}  --  {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.2f}")
        print("    Breakdown:")
        for reason in explanation.split(" | "):
            print(f"      • {reason}")

    print("\n" + "=" * 60)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Profile 1: Nine Vicious (original) — Atlanta trap/rage, high energy, no acoustic
    nine_vicious = {
        "genre":               "hip-hop",
        "moods":               ["intense", "uplifting"],
        "energy":              0.85,
        "likes_acoustic":      False,
        "target_valence":      0.68,
        "target_danceability": 0.82,
    }

    # --- Profile 2: High-Energy Pop — gym playlist, happy and euphoric, max danceability
    high_energy_pop = {
        "genre":               "pop",
        "moods":               ["happy", "euphoric"],
        "energy":              0.90,
        "likes_acoustic":      False,
        "target_valence":      0.85,
        "target_danceability": 0.88,
    }

    # --- Profile 3: Chill Lofi — late-night study session, low energy, acoustic preferred
    chill_lofi = {
        "genre":               "lofi",
        "moods":               ["chill", "focused"],
        "energy":              0.38,
        "likes_acoustic":      True,
        "target_valence":      0.58,
        "target_danceability": 0.55,
    }

    # --- Profile 4: Deep Intense Rock — workout, angry and intense, no acoustic
    deep_intense_rock = {
        "genre":               "rock",
        "moods":               ["intense", "angry"],
        "energy":              0.93,
        "likes_acoustic":      False,
        "target_valence":      0.40,
        "target_danceability": 0.65,
    }

    # --- Profile 5: EDGE CASE — Conflicted Listener (high energy but sad mood)
    # Adversarial: energy=0.9 wants a high-tempo feel but mood=sad pulls toward low-energy songs
    conflicted = {
        "genre":               "soul",
        "moods":               ["sad", "melancholic"],
        "energy":              0.90,
        "likes_acoustic":      True,
        "target_valence":      0.30,
        "target_danceability": 0.50,
    }

    # --- Profile 6: EDGE CASE — Genre Ghost (jazz fan who wants intense mood)
    # Adversarial: no jazz song in catalog has mood=intense, so genre score will never fire together with mood
    genre_ghost = {
        "genre":               "jazz",
        "moods":               ["intense", "euphoric"],
        "energy":              0.80,
        "likes_acoustic":      False,
        "target_valence":      0.70,
        "target_danceability": 0.75,
    }

    run_profile(songs, "PROFILE 1 -- Nine Vicious (Hip-Hop / Trap)", nine_vicious)
    run_profile(songs, "PROFILE 2 -- High-Energy Pop", high_energy_pop)
    run_profile(songs, "PROFILE 3 -- Chill Lofi", chill_lofi)
    run_profile(songs, "PROFILE 4 -- Deep Intense Rock", deep_intense_rock)
    run_profile(songs, "PROFILE 5 (EDGE CASE) -- Conflicted Listener", conflicted)
    run_profile(songs, "PROFILE 6 (EDGE CASE) -- Genre Ghost (Jazz + Intense)", genre_ghost)


if __name__ == "__main__":
    main()
