"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""
import os
from recommender import load_songs, recommend_songs


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    width = 60
    prefs_line = f"genre={user_prefs.get('genre')}, mood={user_prefs.get('mood')}, energy={user_prefs.get('energy')}"

    print("=" * width)
    print(f"Top {len(recommendations)} Recommendations ({prefs_line})".center(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} - Score: {score:.2f}")
        print(f"   {song['artist']} | genre: {song['genre']} | mood: {song['mood']}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print("\n" + "=" * width)


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "..", "data", "songs.csv")
    songs = load_songs(csv_path)
    print(f"Loaded {len(songs)} songs.")
    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
