"""
Curated Seed Catalog for MoodReel.
Expanded domain covering Korean cinema & K-dramas, Japanese cinema & J-dramas,
Chinese cinema & C-dramas, and Hollywood / World live-action masterpieces.
Carefully mapped into Russell's Circumplex Affective Space (Valence x Arousal).
"""

from sqlalchemy.orm import Session
from app.db.models import MovieTitle, Genre, ContentWarning, Availability

SEED_MOVIES = [
    # =========================================================================
    # --- SECTION A: KOREAN CINEMA & K-DRAMAS ---
    # =========================================================================
    {
        "id": "m_kd_01",
        "title": "Crash Landing on You",
        "release_year": 2019,
        "runtime_minutes": 130,
        "synopsis": "A South Korean chaebol heiress accidentally paraglides into the DMZ and North Korea, meeting an honorable army officer who hides and protects her.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZmRkNzAzODItZmI5OS00NzU0LWIwZjEtYjhiMTkyMzIwZDVjXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "valence_score": 0.82,
        "arousal_score": 0.35,
        "ending_tone": "romantic and heartwarming",
        "popularity_score": 9.3,
        "genres": ["Drama", "Romance", "Comedy"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["netflix"]
    },
    {
        "id": "m_kd_02",
        "title": "Squid Game",
        "release_year": 2021,
        "runtime_minutes": 55,
        "synopsis": "Hundreds of cash-strapped contestants accept an invitation to compete in children's games for a tempting prize, but the stakes are deadly.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDcxYjg1OTctYmUxZi00ZjhjLWIwNTMtNmI2M2Y4OTU1YWU2XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.78,
        "arousal_score": 0.92,
        "ending_tone": "chilling and cynical",
        "popularity_score": 9.6,
        "genres": ["Drama", "Mystery", "Thriller", "Action"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "PRESENT"}
        ],
        "platforms": ["netflix"]
    },
    {
        "id": "m_kd_03",
        "title": "Train to Busan",
        "release_year": 2016,
        "runtime_minutes": 118,
        "synopsis": "While a zombie virus breaks out in South Korea, passengers struggle to survive on the train from Seoul to Busan.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODA3OTM4NWQtMjU1OS00NzA2LTlhZDAtYjU2YjM5MWUxNTdiXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.60,
        "arousal_score": 0.94,
        "ending_tone": "intense and emotional",
        "popularity_score": 8.9,
        "genres": ["Action", "Horror", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "grief_loss", "status": "PRESENT"}
        ],
        "platforms": ["prime", "free"]
    },
    {
        "id": "m_kd_04",
        "title": "Memories of Murder",
        "release_year": 2003,
        "runtime_minutes": 132,
        "synopsis": "In 1986, two detectives with wildly contrasting methods attempt to solve Korea's first serial murder cases in a rural province.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYmRjOWE5NmMtYTdkYS00ODFlLWJiMTMtYzE2NDZlZjlkZDQ0XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.75,
        "arousal_score": 0.70,
        "ending_tone": "unsettling and haunting",
        "popularity_score": 9.1,
        "genres": ["Crime", "Drama", "Mystery", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "sexual_violence", "status": "PRESENT"}
        ],
        "platforms": ["hulu", "prime"]
    },
    {
        "id": "m_kd_05",
        "title": "The Glory",
        "release_year": 2022,
        "runtime_minutes": 60,
        "synopsis": "Years after surviving horrific abuse in high school, a woman puts an elaborate revenge scheme in motion to make the perpetrators pay.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODM0ZTc5YTAtZmMxNi00YzJkLWEzODItZDczZTRlNTc1NGE3XkEyXkFqcGc@._V1_QL75_UY562_CR6,0,380,562_.jpg",
        "valence_score": -0.70,
        "arousal_score": 0.80,
        "ending_tone": "cathartic vengeance",
        "popularity_score": 9.0,
        "genres": ["Drama", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "psychological_abuse", "status": "PRESENT"}
        ],
        "platforms": ["netflix"]
    },
    {
        "id": "m_kd_06",
        "title": "Reply 1988",
        "release_year": 2015,
        "runtime_minutes": 90,
        "synopsis": "A heartwarming exploration of nostalgia, friendship, and family bonds between five neighborhood friends growing up in 1988 Seoul.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDBiNDE1NzUtYmU0OS00YmUxLTljODUtOTczNDE3ZGQ0MmYzXkEyXkFqcGc@._V1_QL75_UY562_CR9,0,380,562_.jpg",
        "valence_score": 0.88,
        "arousal_score": -0.30,
        "ending_tone": "warm and nostalgic",
        "popularity_score": 9.4,
        "genres": ["Comedy", "Drama", "Romance", "Family"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["netflix", "free"]
    },
    {
        "id": "m_kd_07",
        "title": "Decision to Leave",
        "release_year": 2022,
        "runtime_minutes": 138,
        "synopsis": "A meticulous homicide detective investigating a man's fall from a mountain peak develops a captivating obsession with the prime suspect—the man's enigmatic widow.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2NhZjcxYjItNDhlOC00Y2U2LWE4NDktMDJhNTQ1NzNjMmNmXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.45,
        "arousal_score": 0.40,
        "ending_tone": "mesmerizing neo-noir",
        "popularity_score": 8.7,
        "genres": ["Mystery", "Romance", "Thriller", "Crime"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["mubi", "prime"]
    },
    {
        "id": "m_kd_08",
        "title": "Vincenzo",
        "release_year": 2021,
        "runtime_minutes": 80,
        "synopsis": "An Italian-Korean mafia consigliere returns to Seoul to recover hidden gold beneath an old plaza, becoming an unlikely vigilante fighting an unscrupulous conglomerate.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDk5ZTY1ZWMtYzY0MC00MmRkLTlmYjYtZTA4ZDYxNWNjZDVkXkEyXkFqcGc@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "valence_score": 0.65,
        "arousal_score": 0.75,
        "ending_tone": "exhilarating anti-hero triumph",
        "popularity_score": 9.0,
        "genres": ["Comedy", "Crime", "Drama", "Action"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["netflix"]
    },

    # =========================================================================
    # --- SECTION B: JAPANESE CINEMA & J-DRAMAS ---
    # =========================================================================
    {
        "id": "m_jd_01",
        "title": "Drive My Car",
        "release_year": 2021,
        "runtime_minutes": 179,
        "synopsis": "An aging theater director mourning his wife's sudden passing is assigned a quiet young female chauffeur in Hiroshima, sparking a delicate bond of shared grief.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOGE5ZWRhYjYtNzVkMS00ZGU3LTg2MTMtODYyMmJlMDMyZjU0XkEyXkFqcGc@._V1_QL75_UY562_CR9,0,380,562_.jpg",
        "valence_score": -0.35,
        "arousal_score": -0.70,
        "ending_tone": "profound and healing",
        "popularity_score": 8.8,
        "genres": ["Drama", "Mystery"],
        "content_warnings": [
            {"warning_code": "grief_loss", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_jd_02",
        "title": "Shoplifters",
        "release_year": 2018,
        "runtime_minutes": 121,
        "synopsis": "A family of impoverished small-time grifters takes in a neglected child they find freezing on a balcony, until an unforeseen incident exposes their hidden bonds.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjY2NGZlZDUtMDUwMi00YTUxLTljNzEtZTE3YjAyNTQyNzU5XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.25,
        "arousal_score": -0.40,
        "ending_tone": "tender and bittersweet",
        "popularity_score": 8.9,
        "genres": ["Crime", "Drama"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["hulu", "prime"]
    },
    {
        "id": "m_jd_03",
        "title": "Alice in Borderland",
        "release_year": 2020,
        "runtime_minutes": 50,
        "synopsis": "An aimless gamer and his two friends find themselves in an eerily abandoned Tokyo, forced to survive cruel, high-stakes psychological and physical death games.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYmMzODA4M2MtMjBmNC00YjFhLTg4NzgtODgyNzE4NWQxMThmXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.65,
        "arousal_score": 0.90,
        "ending_tone": "gripping and electrifying",
        "popularity_score": 9.1,
        "genres": ["Action", "Drama", "Mystery", "Sci-Fi", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "panic_attacks", "status": "PRESENT"}
        ],
        "platforms": ["netflix"]
    },
    {
        "id": "m_jd_04",
        "title": "First Love: Hatsukoi",
        "release_year": 2022,
        "runtime_minutes": 55,
        "synopsis": "Inspired by Hikaru Utada's iconic songs, two sweethearts from the late 1990s cross paths two decades later after tragic turns of fate.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzlkNjU0NzUtMmNkNi00OTBiLWEyN2YtNjkxNzc0ODhkYjExXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": 0.65,
        "arousal_score": -0.30,
        "ending_tone": "romantic and poignant",
        "popularity_score": 8.7,
        "genres": ["Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["netflix"]
    },
    {
        "id": "m_jd_05",
        "title": "Departures",
        "release_year": 2008,
        "runtime_minutes": 130,
        "synopsis": "A dedicated classical cellist loses his orchestra job and accidentally takes work as an encoffiner preparing bodies for burial, discovering profound beauty in life and death.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDNjMzVhZWEtNTA3Zi00NjY0LThiMTUtYzk2MjI5NTQyMjNjXkEyXkFqcGc@._V1_QL75_UY562_CR10,0,380,562_.jpg",
        "valence_score": 0.70,
        "arousal_score": -0.55,
        "ending_tone": "peaceful and restorative",
        "popularity_score": 8.9,
        "genres": ["Drama", "Music"],
        "content_warnings": [
            {"warning_code": "grief_loss", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["prime", "free"]
    },

    # =========================================================================
    # --- SECTION C: CHINESE CINEMA & C-DRAMAS ---
    # =========================================================================
    {
        "id": "m_cd_01",
        "title": "In the Mood for Love",
        "release_year": 2000,
        "runtime_minutes": 98,
        "synopsis": "In 1962 British Hong Kong, two neighbors whose spouses are having an affair develop a tender, restrained bond of unspoken longing and mutual restraint.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2Q4NjllMDgtOTk2Zi00YzM1LWJmOTMtNmRiZDgyZGJmMjQzXkEyXkFqcGc@._V1_QL75_UX380_CR0,3,380,562_.jpg",
        "valence_score": -0.35,
        "arousal_score": -0.60,
        "ending_tone": "gorgeously melancholy and poetic",
        "popularity_score": 9.3,
        "genres": ["Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["max", "apple_tv"]
    },
    {
        "id": "m_cd_02",
        "title": "Crouching Tiger, Hidden Dragon",
        "release_year": 2000,
        "runtime_minutes": 120,
        "synopsis": "A master swordsman gives his fabled ancient green destiny sword to his lover for safekeeping, setting off an epic wuxia conflict of martial arts and romance.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzRmMTU2OWEtZjI0Ni00MGRhLThjOTItZTJiNmM4MDk0ZWU2XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": 0.60,
        "arousal_score": 0.75,
        "ending_tone": "mythic and transcendent",
        "popularity_score": 9.0,
        "genres": ["Action", "Adventure", "Drama", "Fantasy"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["prime", "apple_tv"]
    },
    {
        "id": "m_cd_03",
        "title": "Reset",
        "release_year": 2022,
        "runtime_minutes": 45,
        "synopsis": "A university student and a video game architect find themselves trapped in an inescapable time-loop on a city bus that explodes every single hour.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTY0ZmExMjAtZmIxMC00M2RhLTg0MzgtYTNkMWFlYjA2MjZhXkEyXkFqcGc@._V1_QL75_UY562_CR8,0,380,562_.jpg",
        "valence_score": -0.40,
        "arousal_score": 0.85,
        "ending_tone": "suspenseful and mind-bending",
        "popularity_score": 8.8,
        "genres": ["Drama", "Mystery", "Sci-Fi", "Thriller"],
        "content_warnings": [
            {"warning_code": "panic_attacks", "status": "PRESENT"},
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["viki", "netflix"]
    },
    {
        "id": "m_cd_04",
        "title": "Hidden Love",
        "release_year": 2023,
        "runtime_minutes": 45,
        "synopsis": "A warm, gentle romance following Sang Zhi as she reunites with Duan Jiaxu, her older brother's university friend, turning sweet teenage admiration into true love.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA0NjVhNGEtODBlNC00MzBkLThkMjUtMjYwZmEyNjA4MmIwXkEyXkFqcGc@._V1_QL75_UX380_CR0,55,380,562_.jpg",
        "valence_score": 0.85,
        "arousal_score": -0.25,
        "ending_tone": "comforting and sweet",
        "popularity_score": 8.9,
        "genres": ["Comedy", "Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["netflix", "viki"]
    },
    {
        "id": "m_cd_05",
        "title": "Better Days",
        "release_year": 2019,
        "runtime_minutes": 135,
        "synopsis": "Under the unbearable pressure of national gaokao exams and school bullying, an academic girl forms a protective pact with a street-smart drifter.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDAwNDEyODMtNGQ0NC00Y2M5LWE0OTctZjIwMWU3ZDlmMzMyXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.65,
        "arousal_score": 0.65,
        "ending_tone": "gripping and emotionally raw",
        "popularity_score": 8.6,
        "genres": ["Crime", "Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "psychological_abuse", "status": "PRESENT"}
        ],
        "platforms": ["prime", "free"]
    },

    # =========================================================================
    # --- SECTION D: HOLLYWOOD & WORLD LIVE-ACTION MASTERPIECES ---
    # =========================================================================
    {
        "id": "m_hw_01",
        "title": "Inception",
        "release_year": 2010,
        "runtime_minutes": 148,
        "synopsis": "A skilled thief who steals corporate secrets through dream-sharing technology is offered a chance to erase his criminal past if he can plant an idea into a CEO's subconscious.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": 0.15,
        "arousal_score": 0.85,
        "ending_tone": "mind-bending and exhilarating",
        "popularity_score": 9.5,
        "genres": ["Action", "Adventure", "Sci-Fi", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_hw_02",
        "title": "Interstellar",
        "release_year": 2014,
        "runtime_minutes": 169,
        "synopsis": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked to pilot a spacecraft through a newly discovered wormhole to find humanity a new home.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": 0.35,
        "arousal_score": 0.55,
        "ending_tone": "awe-inspiring and tear-jerking",
        "popularity_score": 9.6,
        "genres": ["Adventure", "Drama", "Sci-Fi"],
        "content_warnings": [
            {"warning_code": "grief_loss", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["paramount", "prime"]
    },
    {
        "id": "m_hw_03",
        "title": "The Dark Knight",
        "release_year": 2008,
        "runtime_minutes": 152,
        "synopsis": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.60,
        "arousal_score": 0.88,
        "ending_tone": "gritty and legendary",
        "popularity_score": 9.7,
        "genres": ["Action", "Crime", "Drama", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_hw_04",
        "title": "The Shawshank Redemption",
        "release_year": 1994,
        "runtime_minutes": 142,
        "synopsis": "Over the course of several decades, two imprisoned men find solace and eventual redemption through acts of common decency.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "valence_score": 0.75,
        "arousal_score": 0.10,
        "ending_tone": "deeply triumphant and hopeful",
        "popularity_score": 9.8,
        "genres": ["Drama"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "PRESENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_hw_05",
        "title": "The Matrix",
        "release_year": 1999,
        "runtime_minutes": 136,
        "synopsis": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth—the life he knows is the elaborate deception of an evil cyber-intelligence.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "valence_score": 0.40,
        "arousal_score": 0.82,
        "ending_tone": "iconic cyberpunk awakening",
        "popularity_score": 9.4,
        "genres": ["Action", "Sci-Fi"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_hw_06",
        "title": "Good Will Hunting",
        "release_year": 1997,
        "runtime_minutes": 126,
        "synopsis": "Will Hunting, a janitor at M.I.T. with a genius-level intellect, struggles with emotional trauma until he begins therapy with a compassionate psychologist.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzJkNmZiMDEtNjg2Yi00ZDljLWJjZGQtZGFiMTExZjMyMTljXkEyXkFqcGdeQXVyMjQ0NzE0MQ@@._V1_SX300.jpg",
        "valence_score": 0.70,
        "arousal_score": -0.15,
        "ending_tone": "deeply emotional and healing",
        "popularity_score": 9.2,
        "genres": ["Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_hw_07",
        "title": "Pulp Fiction",
        "release_year": 1994,
        "runtime_minutes": 154,
        "synopsis": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTViYTE3ZGQtNDBlMC00ZTAyLTkyODMtZGRiZDg0MjA2YThkXkEyXkFqcGc@._V1_QL75_UY562_CR3,0,380,562_.jpg",
        "valence_score": 0.20,
        "arousal_score": 0.88,
        "ending_tone": "stylized and audacious",
        "popularity_score": 9.3,
        "genres": ["Crime", "Drama"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "substance_abuse", "status": "PRESENT"}
        ],
        "platforms": ["max", "paramount"]
    },
    {
        "id": "m_hw_08",
        "title": "Arrival",
        "release_year": 2016,
        "runtime_minutes": 116,
        "synopsis": "A linguist is recruited by the military to assist in translating alien communications after twelve mysterious spacecraft touch down across Earth.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_QL75_UX380_CR0,16,380,562_.jpg",
        "valence_score": 0.25,
        "arousal_score": 0.15,
        "ending_tone": "philosophical and emotionally poignant",
        "popularity_score": 8.9,
        "genres": ["Drama", "Mystery", "Sci-Fi"],
        "content_warnings": [
            {"warning_code": "grief_loss", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["paramount", "prime"]
    },
    {
        "id": "m_hw_09",
        "title": "Dune",
        "release_year": 2021,
        "runtime_minutes": 155,
        "synopsis": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset on the dangerous desert planet Arrakis.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNWIyNmU5MGYtZDZmNi00ZjAwLWJlYjgtZTc0ZGIxMDE4ZGYwXkEyXkFqcGc@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "valence_score": 0.10,
        "arousal_score": 0.65,
        "ending_tone": "epic and immersive",
        "popularity_score": 9.2,
        "genres": ["Action", "Adventure", "Drama", "Sci-Fi"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_hw_10",
        "title": "About Time",
        "release_year": 2013,
        "runtime_minutes": 123,
        "synopsis": "At the age of 21, Tim discovers he can travel in time and change what happens in his own life, teaching him to treasure every single ordinary day.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTA1ODUzMDA3NzFeQTJeQWpwZ15BbWU3MDgxMTYxNTk@._V1_QL75_UX380_CR0,20,380,562_.jpg",
        "valence_score": 0.85,
        "arousal_score": -0.20,
        "ending_tone": "tender, tearful, and life-affirming",
        "popularity_score": 9.1,
        "genres": ["Comedy", "Drama", "Fantasy", "Romance"],
        "content_warnings": [
            {"warning_code": "grief_loss", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["prime", "apple_tv"]
    },
    {
        "id": "m_hw_11",
        "title": "Get Out",
        "release_year": 2017,
        "runtime_minutes": 104,
        "synopsis": "A young African-American visits his white girlfriend's parents for the weekend, uncovering a disturbing truth behind their polite facade.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjUxMDQwNjcyNl5BMl5BanBnXkFtZTgwNzcwMzc0MTI@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.65,
        "arousal_score": 0.85,
        "ending_tone": "disturbing and electrifying",
        "popularity_score": 9.0,
        "genres": ["Horror", "Mystery", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "panic_attacks", "status": "PRESENT"}
        ],
        "platforms": ["prime", "free"]
    },
    {
        "id": "m_hw_12",
        "title": "Everything Everywhere All at Once",
        "release_year": 2022,
        "runtime_minutes": 139,
        "synopsis": "A middle-aged Chinese immigrant is swept up into an insane adventure in which she alone can save existence by exploring other universes and connecting with the lives she could have led.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOWNmMzAzZmQtNDQ1NC00Nzk5LTkyMmUtNGI2N2NkOWM4MzEyXkEyXkFqcGc@._V1_QL75_UY562_CR4,0,380,562_.jpg",
        "valence_score": 0.70,
        "arousal_score": 0.88,
        "ending_tone": "exhilarating, absurd, and profoundly moving",
        "popularity_score": 9.5,
        "genres": ["Action", "Adventure", "Comedy", "Sci-Fi", "Drama"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["paramount", "prime"]
    },
    {
        "id": "m_hw_13",
        "title": "Se7en",
        "release_year": 1995,
        "runtime_minutes": 127,
        "synopsis": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives in a perpetually rain-soaked city.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTU5MTFlYmItMGI4Ni00OTJkLTlmZTUtNzcyNzcxM2Y4MWI0XkEyXkFqcGdeQXVyNzg5OTk2OA@@._V1_SX300.jpg",
        "valence_score": -0.85,
        "arousal_score": 0.85,
        "ending_tone": "unforgiving psychological dread",
        "popularity_score": 9.2,
        "genres": ["Crime", "Drama", "Mystery", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_hw_14",
        "title": "Pride & Prejudice",
        "release_year": 2005,
        "runtime_minutes": 129,
        "synopsis": "Sparks fly when spirited Elizabeth Bennet meets single, rich, and proudly reserved Mr. Darcy, learning to look past social vanity.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTA1NDQ3NTcyOTNeQTJeQWpwZ15BbWU3MDA0MzA4MzE@._V1_QL75_UX380_CR0,1,380,562_.jpg",
        "valence_score": 0.80,
        "arousal_score": -0.30,
        "ending_tone": "enchanting and romantic",
        "popularity_score": 8.9,
        "genres": ["Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["netflix", "prime"]
    },

    # =========================================================================
    # --- SECTION E: ORIGINAL SEED CLASSICS ---
    # =========================================================================
    {
        "id": "m_q1_01",
        "title": "Amélie",
        "release_year": 2001,
        "runtime_minutes": 122,
        "synopsis": "An imaginative Parisian waitress decides to help those around her find happiness, while seeking love of her own.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTNmYzY0MWQtZGZmNy00Y2Y4LWFmMDQtMTZjYTdiYzEwZGQ2XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "valence_score": 0.82,
        "arousal_score": 0.45,
        "ending_tone": "uplifting",
        "popularity_score": 8.6,
        "genres": ["Comedy", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"},
            {"warning_code": "substance_abuse", "status": "ABSENT"}
        ],
        "platforms": ["prime", "apple_tv"]
    },
    {
        "id": "m_q1_02",
        "title": "Spider-Man: Into the Spider-Verse",
        "release_year": 2018,
        "runtime_minutes": 117,
        "synopsis": "Teenager Miles Morales becomes the new Spider-Man and joins other alternate-dimension heroes to stop a threat to all reality.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgzOF5BMl5BanBnXkFtZTgwNTkwNTQ3NjM@._V1_QL75_UX380_CR0,1,380,562_.jpg",
        "valence_score": 0.78,
        "arousal_score": 0.85,
        "ending_tone": "triumphant",
        "popularity_score": 9.2,
        "genres": ["Animation", "Action", "Adventure"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "grief_loss", "status": "PRESENT"}
        ],
        "platforms": ["netflix", "prime"]
    },
    {
        "id": "m_q1_03",
        "title": "Little Miss Sunshine",
        "release_year": 2006,
        "runtime_minutes": 101,
        "synopsis": "A family determined to get their young daughter into the finals of a beauty pageant takes a cross-country trip in their VW bus.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTgzNTgzODU0NV5BMl5BanBnXkFtZTcwMjEyMjMzMQ@@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "valence_score": 0.72,
        "arousal_score": 0.50,
        "ending_tone": "uplifting",
        "popularity_score": 8.1,
        "genres": ["Comedy", "Drama"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "PRESENT"},
            {"warning_code": "substance_abuse", "status": "PRESENT"}
        ],
        "platforms": ["hulu", "prime"]
    },
    {
        "id": "m_q1_04",
        "title": "Paddington 2",
        "release_year": 2017,
        "runtime_minutes": 103,
        "synopsis": "Paddington picks up a series of odd jobs to buy a unique pop-up book for his aunt's 100th birthday, only for the book to be stolen.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTk1YzlhMTUtZmU5MC00NmRmLTlkZjItYzQ0NTY4Y2NiNzc4XkEyXkFqcGc@._V1_QL75_UY562_CR0,0,380,562_.jpg",
        "valence_score": 0.92,
        "arousal_score": 0.40,
        "ending_tone": "pure joy",
        "popularity_score": 8.8,
        "genres": ["Adventure", "Comedy", "Family"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"},
            {"warning_code": "substance_abuse", "status": "ABSENT"}
        ],
        "platforms": ["netflix", "max"]
    },
    {
        "id": "m_q1_05",
        "title": "Ferris Bueller's Day Off",
        "release_year": 1986,
        "runtime_minutes": 103,
        "synopsis": "A high school wise guy is determined to have a day off from school, despite what the principal thinks of that.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZWYwMjUxNjMtMzE0MC00NDM3LWIxMmQtYmEyNWVjNjdlZGZjXkEyXkFqcGc@._V1_QL75_UX380_CR0,13,380,562_.jpg",
        "valence_score": 0.85,
        "arousal_score": 0.65,
        "ending_tone": "exuberant",
        "popularity_score": 8.4,
        "genres": ["Comedy"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["prime", "paramount"]
    },
    {
        "id": "m_q1_06",
        "title": "La La Land",
        "release_year": 2016,
        "runtime_minutes": 128,
        "synopsis": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDllYjliOTUtMDJjZC00ODIzLWJmNGMtOWI2NzQxMjA2NzdlXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "valence_score": 0.68,
        "arousal_score": 0.60,
        "ending_tone": "bittersweet",
        "popularity_score": 8.7,
        "genres": ["Comedy", "Drama", "Music", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["netflix", "apple_tv"]
    },
    {
        "id": "m_q1_07",
        "title": "The Grand Budapest Hotel",
        "release_year": 2014,
        "runtime_minutes": 99,
        "synopsis": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": 0.74,
        "arousal_score": 0.55,
        "ending_tone": "whimsical",
        "popularity_score": 8.9,
        "genres": ["Adventure", "Comedy", "Crime"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["hulu", "prime"]
    },
    {
        "id": "m_q2_01",
        "title": "My Neighbor Totoro",
        "release_year": 1988,
        "runtime_minutes": 86,
        "synopsis": "When two girls move to the country to be near their ailing mother, they have adventures with the friendly spirits who live nearby.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYWM3MDE3YjEtMzIzZC00ODE5LTgxNTItNmUyMTBkM2M2NmNiXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": 0.88,
        "arousal_score": -0.65,
        "ending_tone": "peaceful",
        "popularity_score": 9.1,
        "genres": ["Animation", "Family", "Fantasy"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["max", "netflix"]
    },
    {
        "id": "m_q2_02",
        "title": "Paterson",
        "release_year": 2016,
        "runtime_minutes": 118,
        "synopsis": "A quiet observation of the triumphs and defeats of daily life, along with the poetry evident in its smallest details.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTUzODA4Nzk0OF5BMl5BanBnXkFtZTgwNzE1MDIwMDI@._V1_QL75_UX380_CR0,2,380,562_.jpg",
        "valence_score": 0.65,
        "arousal_score": -0.80,
        "ending_tone": "serene",
        "popularity_score": 7.8,
        "genres": ["Comedy", "Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["prime", "free"]
    },
    {
        "id": "m_q2_03",
        "title": "Before Sunrise",
        "release_year": 1995,
        "runtime_minutes": 101,
        "synopsis": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna before parting ways.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDZhZmI1ZTUtYWI3NC00NTMwLTk3NWMtNDc0OGNjM2I0ZjlmXkEyXkFqcGc@._V1_QL75_UX380_CR0,1,380,562_.jpg",
        "valence_score": 0.75,
        "arousal_score": -0.40,
        "ending_tone": "tender",
        "popularity_score": 8.7,
        "genres": ["Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["apple_tv", "prime"]
    },
    {
        "id": "m_q2_04",
        "title": "Chef",
        "release_year": 2014,
        "runtime_minutes": 114,
        "synopsis": "A head chef quits his restaurant job and buys a food truck in an effort to reclaim his creative promise and piece together his estranged family.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODkyNTI4YjUtNjEyNC00NWQ5LTk4M2YtM2Q3NjBiYmJmMGUyXkEyXkFqcGc@._V1_QL75_UY562_CR0,0,380,562_.jpg",
        "valence_score": 0.80,
        "arousal_score": -0.20,
        "ending_tone": "warm and comforting",
        "popularity_score": 8.0,
        "genres": ["Adventure", "Comedy", "Drama"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_q2_05",
        "title": "Kiki's Delivery Service",
        "release_year": 1989,
        "runtime_minutes": 103,
        "synopsis": "A young witch on her mandatory year of independent life finds fitting into a new community difficult while supporting herself running an air courier service.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTFhYWI1NGUtZWFhZS00MTdkLWIzZTItMDBhNWNiZDNlMjYyXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "valence_score": 0.85,
        "arousal_score": -0.30,
        "ending_tone": "gentle and reassuring",
        "popularity_score": 8.6,
        "genres": ["Animation", "Adventure", "Family"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["max", "netflix"]
    },
    {
        "id": "m_q2_06",
        "title": "Midnight in Paris",
        "release_year": 2011,
        "runtime_minutes": 94,
        "synopsis": "While on a trip to Paris with his fiancée's family, a nostalgic screenwriter finds himself mysteriously going back to the 1920s every night at midnight.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTM4NjY1MDQwMl5BMl5BanBnXkFtZTcwNTI3Njg3NA@@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "valence_score": 0.70,
        "arousal_score": -0.45,
        "ending_tone": "reflective",
        "popularity_score": 7.9,
        "genres": ["Comedy", "Fantasy", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["prime", "apple_tv"]
    },
    {
        "id": "m_q3_01",
        "title": "Manchester by the Sea",
        "release_year": 2016,
        "runtime_minutes": 137,
        "synopsis": "A depressed uncle is asked to take care of his teenage nephew after the boy's father dies, forcing him to face an unspeakable tragedy from his past.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTYxMjk0NDg4Ml5BMl5BanBnXkFtZTgwODcyNjA5OTE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.85,
        "arousal_score": -0.50,
        "ending_tone": "deeply somber",
        "popularity_score": 8.3,
        "genres": ["Drama"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "PRESENT"},
            {"warning_code": "grief_loss", "status": "PRESENT"},
            {"warning_code": "substance_abuse", "status": "PRESENT"}
        ],
        "platforms": ["prime"]
    },
    {
        "id": "m_q3_02",
        "title": "Her",
        "release_year": 2013,
        "runtime_minutes": 126,
        "synopsis": "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNjIxYTI3NTYtMDJmMC00Yzk0LWFkOGUtODlkMDdkZTFiNTE4XkEyXkFqcGc@._V1_SX300.jpg",
        "valence_score": -0.45,
        "arousal_score": -0.55,
        "ending_tone": "poignant and bittersweet",
        "popularity_score": 8.5,
        "genres": ["Drama", "Romance", "Sci-Fi"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "grief_loss", "status": "PRESENT"}
        ],
        "platforms": ["max", "prime"]
    },
    {
        "id": "m_q3_03",
        "title": "Past Lives",
        "release_year": 2023,
        "runtime_minutes": 105,
        "synopsis": "Nora and Hae Sung, two deeply connected childhood friends, are wrested apart after Nora's family emigrates from South Korea. Two decades later, they reunite.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjQyMTNhNjUtN2VmYy00NWRhLTkwOTctMGVmNTBmNDIxYjZhXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.40,
        "arousal_score": -0.60,
        "ending_tone": "achingly tender",
        "popularity_score": 8.6,
        "genres": ["Drama", "Romance"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["paramount", "prime"]
    },
    {
        "id": "m_q3_04",
        "title": "Eternal Sunshine of the Spotless Mind",
        "release_year": 2004,
        "runtime_minutes": 108,
        "synopsis": "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTY4NzcwODg3Nl5BMl5BanBnXkFtZTcwNTEwOTMyMw@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.55,
        "arousal_score": -0.20,
        "ending_tone": "wistful and melancholic",
        "popularity_score": 8.9,
        "genres": ["Drama", "Romance", "Sci-Fi"],
        "content_warnings": [
            {"warning_code": "substance_abuse", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["prime", "apple_tv"]
    },
    {
        "id": "m_q3_05",
        "title": "Lost in Translation",
        "release_year": 2003,
        "runtime_minutes": 102,
        "synopsis": "A faded movie star and a neglected young woman form an unlikely bond after crossing paths in Tokyo.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTUxMzk0NDg1MV5BMl5BanBnXkFtZTgwNDg0NjkxMDI@._V1_QL75_UX380_CR0,12,380,562_.jpg",
        "valence_score": -0.50,
        "arousal_score": -0.70,
        "ending_tone": "lonely yet evocative",
        "popularity_score": 8.2,
        "genres": ["Comedy", "Drama"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "ABSENT"},
            {"warning_code": "violence", "status": "ABSENT"}
        ],
        "platforms": ["netflix", "prime"]
    },
    {
        "id": "m_q4_01",
        "title": "Whiplash",
        "release_year": 2014,
        "runtime_minutes": 106,
        "synopsis": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDFjOWFkYzktYzhhMC00NmYyLTkwY2EtYjViMDhmNzg0OGFkXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.60,
        "arousal_score": 0.88,
        "ending_tone": "electrifying and exhausting",
        "popularity_score": 9.0,
        "genres": ["Drama", "Music"],
        "content_warnings": [
            {"warning_code": "psychological_abuse", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "PRESENT"},
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["netflix", "prime"]
    },
    {
        "id": "m_q4_02",
        "title": "Parasite",
        "release_year": 2019,
        "runtime_minutes": 132,
        "synopsis": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.70,
        "arousal_score": 0.75,
        "ending_tone": "chilling and tragic",
        "popularity_score": 9.4,
        "genres": ["Drama", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["max", "hulu"]
    },
    {
        "id": "m_q4_03",
        "title": "Uncut Gems",
        "release_year": 2019,
        "runtime_minutes": 135,
        "synopsis": "With his debts mounting and angry collectors closing in, a fast-talking New York City jeweler risks everything in hope of staying afloat and alive.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNmI0YjA5NjItYzExYi00NzkxLTkxNDctNGJjYTZhM2M0NDQ0XkEyXkFqcGc@._V1_QL75_UX380_CR0,15,380,562_.jpg",
        "valence_score": -0.80,
        "arousal_score": 0.95,
        "ending_tone": "unrelenting anxiety",
        "popularity_score": 8.2,
        "genres": ["Crime", "Drama", "Thriller"],
        "content_warnings": [
            {"warning_code": "panic_attacks", "status": "PRESENT"},
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "substance_abuse", "status": "PRESENT"}
        ],
        "platforms": ["netflix", "prime"]
    },
    {
        "id": "m_q4_04",
        "title": "Black Swan",
        "release_year": 2010,
        "runtime_minutes": 108,
        "synopsis": "A committed dancer wins the lead role in a production of Tchaikovsky's 'Swan Lake' only to find herself struggling to maintain her sanity.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzY2NzI4OTE5MF5BMl5BanBnXkFtZTcwMjMyNDY4Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "valence_score": -0.75,
        "arousal_score": 0.85,
        "ending_tone": "hallucinatory descent",
        "popularity_score": 8.5,
        "genres": ["Drama", "Thriller"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "PRESENT"},
            {"warning_code": "eating_disorders", "status": "PRESENT"},
            {"warning_code": "sexual_violence", "status": "PRESENT"}
        ],
        "platforms": ["hulu", "prime"]
    },
    {
        "id": "m_q4_05",
        "title": "Nightcrawler",
        "release_year": 2014,
        "runtime_minutes": 117,
        "synopsis": "When Louis Bloom, a con man desperate for work, muscles into the world of L.A. crime journalism, he blurs the line between observer and participant.",
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjMwMmI5MWQtOTU4OS00OTAyLTg0OTYtNmQ5YzExZTQ3ZWJhXkEyXkFqcGc@._V1_QL75_UY562_CR5,0,380,562_.jpg",
        "valence_score": -0.70,
        "arousal_score": 0.70,
        "ending_tone": "cynical and unsettling",
        "popularity_score": 8.4,
        "genres": ["Crime", "Drama", "Thriller"],
        "content_warnings": [
            {"warning_code": "violence", "status": "PRESENT"},
            {"warning_code": "self_harm", "status": "ABSENT"}
        ],
        "platforms": ["netflix", "free"]
    },
    {
        "id": "m_unknown_01",
        "title": "The Mysterious Enigma",
        "release_year": 2022,
        "runtime_minutes": 95,
        "synopsis": "An indie suspense film with unverified crowdsourced trigger metadata.",
        "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=500&auto=format&fit=crop&q=80",
        "valence_score": 0.10,
        "arousal_score": 0.20,
        "ending_tone": "ambiguous",
        "popularity_score": 7.0,
        "genres": ["Mystery", "Thriller"],
        "content_warnings": [
            {"warning_code": "self_harm", "status": "UNKNOWN"},
            {"warning_code": "violence", "status": "PRESENT"}
        ],
        "platforms": ["free"]
    }
]

def seed_database(db: Session):
    """
    Seeds database with genres and movie titles.
    Inserts any titles that do not already exist by ID.
    """
    existing_ids = {row[0] for row in db.query(MovieTitle.id).all()}
    genre_cache = {g.name: g for g in db.query(Genre).all()}

    for item in SEED_MOVIES:
        if item["id"] in existing_ids:
            continue

        movie = MovieTitle(
            id=item["id"],
            title=item["title"],
            release_year=item["release_year"],
            runtime_minutes=item["runtime_minutes"],
            synopsis=item["synopsis"],
            poster_url=item["poster_url"],
            valence_score=item["valence_score"],
            arousal_score=item["arousal_score"],
            valence_arousal_source="editorial_curated",
            valence_arousal_confidence=0.95,
            ending_tone=item["ending_tone"],
            popularity_score=item["popularity_score"]
        )
        db.add(movie)

        # Attach genres
        for g_name in item["genres"]:
            if g_name not in genre_cache:
                genre_obj = db.query(Genre).filter(Genre.name == g_name).first()
                if not genre_obj:
                    genre_obj = Genre(name=g_name)
                    db.add(genre_obj)
                    db.flush()
                genre_cache[g_name] = genre_obj
            movie.genres.append(genre_cache[g_name])

        # Attach content warnings
        for cw in item.get("content_warnings", []):
            warning_entry = ContentWarning(
                title_id=item["id"],
                warning_code=cw["warning_code"],
                status=cw["status"],
                confidence=0.90 if cw["status"] != "UNKNOWN" else 0.40,
                source="editorial_curated"
            )
            movie.content_warnings.append(warning_entry)

        # Attach availability
        for platform in item.get("platforms", []):
            avail_entry = Availability(
                title_id=item["id"],
                platform=platform,
                region="GLOBAL"
            )
            movie.availabilities.append(avail_entry)

        db.add(movie)

    db.commit()
