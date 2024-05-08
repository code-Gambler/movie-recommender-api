import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import app

def test_health_check():
    response = app.create_app().test_client().get('/')
    json_dict = json.loads(response.data)
    assert response.status_code == 200
    assert json_dict["author"] == "Steven David Pillay"
    assert json_dict["githubUrl"] == "https://github.com/code-Gambler/movie-recommender-api"