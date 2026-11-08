import urllib.request
import json

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/recommend',
    data=json.dumps({
        'session_id': 'browser_test',
        'target_mood': {'valence': 0.70, 'arousal': -0.40, 'confidence': 1.0},
        'strategy': 'catharsis',
        'filters': {'excluded_genres': [], 'preferred_genres': [], 'excluded_warnings': [], 'streaming_providers': [], 'exclude_seen': True},
        'limit': 5
    }).encode(),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())
    print("Status:", r.status)
    for rec in data['recommendations']:
        print(f"{rec['title']} ({rec['release_year']}) -> {rec['poster_url']}")
