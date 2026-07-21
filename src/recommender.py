import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_UMBRELLAS: Dict[str, List[str]] = {
    "pop": ["pop", "indie pop", "k-pop", "synthwave", "reggaeton", "afrobeats"],
    "acoustic": ["lofi", "ambient", "jazz", "classical", "folk", "blues", "country"],
    "intense": ["rock", "metal", "hip-hop", "experimental"],
}

MOOD_UMBRELLAS: Dict[str, List[str]] = {
    "happy": ["happy", "joyful"],
    "mellow": ["chill", "dreamy", "nostalgic", "peaceful"],
    "moody": ["moody", "brooding"],
    "intense": ["intense", "energetic"],
}

def _invert_umbrellas(umbrella_map: Dict[str, List[str]]) -> Dict[str, str]:
    return {label: umbrella for umbrella, labels in umbrella_map.items() for label in labels}

_GENRE_LABEL_TO_UMBRELLA = _invert_umbrellas(GENRE_UMBRELLAS)
_MOOD_LABEL_TO_UMBRELLA = _invert_umbrellas(MOOD_UMBRELLAS)

def _normalize_label(label: Optional[str]) -> str:
    return (label or "").strip().lower()

def _category_match_points(
    user_label: Optional[str],
    song_label: Optional[str],
    label_to_umbrella: Dict[str, str],
    points: int,
    field_name: str,
) -> Tuple[int, str]:
    user_norm = _normalize_label(user_label)
    song_norm = _normalize_label(song_label)

    if not user_norm:
        return 0, f"No {field_name} preference provided; skipped ({field_name} +0)"

    if user_norm == song_norm:
        return points, f"Exact {field_name} match: '{song_label}' == '{user_label}' ({field_name} +{points})"

    user_umbrella = label_to_umbrella.get(user_norm)
    song_umbrella = label_to_umbrella.get(song_norm)
    if user_umbrella is not None and user_umbrella == song_umbrella:
        return points, (
            f"Umbrella {field_name} match: '{song_label}' and '{user_label}' "
            f"both in '{user_umbrella}' ({field_name} +{points})"
        )

    return 0, f"No {field_name} match: '{song_label}' vs '{user_label}' ({field_name} +0)"

def _energy_similarity_points(target_energy: float, song_energy: float) -> Tuple[int, str]:
    diff = abs(song_energy - target_energy)
    if diff < 0.2:
        pts = 4
    elif diff < 0.4:
        pts = 3
    elif diff < 0.6:
        pts = 2
    elif diff < 0.8:
        pts = 1
    else:
        pts = 0
    return pts, (
        f"Energy similarity: |{song_energy:.2f} - {target_energy:.2f}| = "
        f"{diff:.2f} diff (energy +{pts})"
    )

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
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

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
    print(f"Loading songs from {csv_path}...")
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

MAX_POSSIBLE_SCORE = 8.0

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons: List[str] = []
    raw_score = 0

    genre_points, genre_reason = _category_match_points(
        user_prefs.get("genre"), song.get("genre", ""), _GENRE_LABEL_TO_UMBRELLA, 2, "genre"
    )
    raw_score += genre_points
    reasons.append(genre_reason)

    mood_points, mood_reason = _category_match_points(
        user_prefs.get("mood"), song.get("mood", ""), _MOOD_LABEL_TO_UMBRELLA, 2, "mood"
    )
    raw_score += mood_points
    reasons.append(mood_reason)

    user_energy = user_prefs.get("energy")
    song_energy = song.get("energy")
    if user_energy is None or song_energy is None:
        reasons.append("Energy preference or song energy missing; skipped (energy +0)")
    else:
        energy_points, energy_reason = _energy_similarity_points(user_energy, song_energy)
        raw_score += energy_points
        reasons.append(energy_reason)

    score = raw_score / MAX_POSSIBLE_SCORE
    reasons.append(f"Total: {raw_score:.0f}/{MAX_POSSIBLE_SCORE:.0f} raw points -> normalized score {score:.2f}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
