import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import app

def test_health_check():
    response = app.create_app().test_client().get('/api/v1/recommend?genre=sci-fi,drama')
    assert response.status_code == 200
    assert response.data == b'[{"genres":"Comedy|Drama|Sci-Fi","imdbLink":"http://www.imdb.com/title/tt2040470/","title":"Plato\'s Reality Machine (2013)"},{"genres":"Action|Drama|Mystery|Romance|Sci-Fi|Thriller","imdbLink":"http://www.imdb.com/title/tt0288808/","title":"Say Nothing (2001)"},{"genres":"Drama|Horror|Sci-Fi","imdbLink":"http://www.imdb.com/title/tt0071855/","title":"Moonchild (1974)"},{"genres":"Drama|Horror|Sci-Fi|Thriller","imdbLink":"http://www.imdb.com/title/tt0781392/","title":"Black Night (2006)"},{"genres":"Drama|Romance|Sci-Fi","imdbLink":"http://www.imdb.com/title/tt1894616/","title":"Awaken (2013)"},{"genres":"Drama|Sci-Fi","imdbLink":"http://www.imdb.com/title/tt3444016/","title":"The Awareness (2014)"},{"genres":"Documentary|Drama|Sci-Fi","imdbLink":"http://www.imdb.com/title/tt1590010/","title":"Voyage to Metropolis (2010)"},{"genres":"Drama|Mystery|Sci-Fi","imdbLink":"http://www.imdb.com/title/tt7243006/","title":"Meteors (2017)"},{"genres":"Adventure|Drama|Sci-Fi|Thriller","imdbLink":"http://www.imdb.com/title/tt0069601/","title":"Failure of Engineer Garin (1973)"},{"genres":"Action|Crime|Drama|Mystery|Sci-Fi|Thriller|IMAX","imdbLink":"http://www.imdb.com/title/tt1375666/","title":"Inception (2010)"}]\n'