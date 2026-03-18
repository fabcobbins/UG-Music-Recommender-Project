"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # User profile modeled after Nine Vicious — Atlanta trap/rage, YSL, high energy, melodic auto-tune flow
    user_prefs = {
        "genre":               "hip-hop",
        "moods":               ["intense", "uplifting"],
        "energy":              0.85,
        "likes_acoustic":      False,
        "target_valence":      0.68,
        "target_danceability": 0.82,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 60)
    print("  TOP RECOMMENDATIONS")
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


if __name__ == "__main__":
    main()
