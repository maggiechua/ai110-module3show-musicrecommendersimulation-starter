import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recommender import Song, UserProfile, Recommender, score_song


def test_score_song_against_user_profile():
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {
        "id": 1,
        "title": "Test Pop Track",
        "artist": "Test Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }

    score, reasons = score_song(user_prefs, song)
    # Exact genre + exact mood + energy diff of 0.0 -> max points (2 + 2 + 4 = 8/8)
    assert score == 1.0
    assert isinstance(reasons, list)
    assert len(reasons) > 0
    assert all(isinstance(reason, str) for reason in reasons)
    print(f"Score: {score} \nScore reasons: {reasons}")

def test_score_song_partial_match_scores_lower_than_perfect_match():
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    mismatched_song = {
        "id": 2,
        "title": "Chill Lofi Loop",
        "artist": "Test Artist",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "tempo_bpm": 80,
        "valence": 0.6,
        "danceability": 0.5,
        "acousticness": 0.9,
    }

    score, reasons = score_song(user_prefs, mismatched_song)

    # No genre/mood match, energy diff of 0.4 -> only 1 similarity point (0 + 0 + 1 = 1/8)
    assert 0.0 <= score < 1.0
    assert len(reasons) > 0
    print(f"Score: {score} \nScore reasons: {reasons}")

test_score_song_against_user_profile()
test_score_song_partial_match_scores_lower_than_perfect_match()

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
