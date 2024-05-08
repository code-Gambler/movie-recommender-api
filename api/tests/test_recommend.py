import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import app

def test_health_check():
    response = app.create_app().test_client().get('/api/v1/recommend?title=interstellar%202014')
    assert response.status_code == 200
    assert response.data == b'[{"genres":"Adventure|Drama","imdbLink":"http://www.imdb.com/title/tt1663202/","score":7.4521859204,"title":"The Revenant (2015)"},{"genres":"Action|Sci-Fi|IMAX","imdbLink":"http://www.imdb.com/title/tt1454468/","score":7.3843153457,"title":"Gravity (2013)"},{"genres":"Adventure|Drama|Sci-Fi","imdbLink":"http://www.imdb.com/title/tt3659388/","score":7.1828211405,"title":"The Martian (2015)"},{"genres":"Action|Sci-Fi|IMAX","imdbLink":"http://www.imdb.com/title/tt1631867/","score":7.1515312111,"title":"Edge of Tomorrow (2014)"},{"genres":"Sci-Fi","imdbLink":"http://www.imdb.com/title/tt2543164/","score":7.0998370674,"title":"Arrival (2016)"},{"genres":"Drama|Sci-Fi|Thriller","imdbLink":"http://www.imdb.com/title/tt0470752/","score":6.9756378285,"title":"Ex Machina (2015)"},{"genres":"Drama|Thriller|War","imdbLink":"http://www.imdb.com/title/tt2084970/","score":6.4625847617,"title":"The Imitation Game (2014)"},{"genres":"Drama|Thriller","imdbLink":"http://www.imdb.com/title/tt2267998/","score":6.3880750782,"title":"Gone Girl (2014)"},{"genres":"Sci-Fi|Thriller","imdbLink":"http://www.imdb.com/title/tt1219289/","score":6.3203225396,"title":"Limitless (2011)"}]\n'