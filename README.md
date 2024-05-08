# Movie Recommender API Documentation
This document provides a comprehensive guide to the Movie Recommender API, including installation, usage, and API endpoints.

## API EndPoints
The API offers movie recommendations through a single endpoint located under version 1
### `/`
This endpoint is a health check which returns the author name, Github URL and host.
- Here is a sample response when running on localhost:
```
{
  "author": "Steven David Pillay",
  "githubUrl": "https://github.com/code-Gambler/movie-recommender-api",
  "hostname": "localhost"
}
```
### `/api/v1/recommend` (GET)
This endpoint accepts optional query parameters to recommend movies:
- `title`: Recommend movies similar to the provided title.
- `genre`(comma-separated): Recommend movies based on the provided genre(s) (case-insensitive).
- If both title and genre are missing, it returns a JSON object with an error message.
- Response format: JSON containing 10 recommended movies or an error message.
The Response mainly contains the Movie title, genres and a Link to the IMBD webpage of the movie

### Here are some sample requests and responses:
- Request: `/api/v1/recommend?genre=sci-fi,drama`
- Response:
  ```
  [
    {
      "genres": "Comedy|Drama|Sci-Fi",
      "imdbLink": "http://www.imdb.com/title/tt2040470/",
      "title": "Plato's Reality Machine (2013)"
    },
    {
      "genres": "Action|Drama|Mystery|Romance|Sci-Fi|Thriller",
      "imdbLink": "http://www.imdb.com/title/tt0288808/",
      "title": "Say Nothing (2001)"
    },
    ....,
    {
      "genres": "Action|Crime|Drama|Mystery|Sci-Fi|Thriller|IMAX",
      "imdbLink": "http://www.imdb.com/title/tt1375666/",
      "title": "Inception (2010)"
    }
  ]
  ```
- Request: `/api/v1/recommend?title=the%20avengers%202012`
- Response:
  ```
  [
    {
      "genres": "Action|Adventure|Fantasy|IMAX",
      "imdbLink": "http://www.imdb.com/title/tt1981115/",
      "score": 19.6101985468,
      "title": "Thor: The Dark World (2013)"
    },
    {
      "genres": "Action|Adventure|Sci-Fi",
      "imdbLink": "http://www.imdb.com/title/tt2395427/",
      "score": 19.4917702457,
      "title": "Avengers: Age of Ultron (2015)"
    },
    ...,
    {
      "genres": "Action|Adventure|Sci-Fi|Thriller|IMAX",
      "imdbLink": "http://www.imdb.com/title/tt1228705/",
      "score": 15.6519205859,
      "title": "Iron Man 2 (2010)"
    }
  ]
  ```



## Project Structure
The project is organized using a modular structure with Flask Blueprints for the separation of concerns. Here's a breakdown of the key files:

- `app.py`: Creates the Flask application instance and registers Blueprints.
- `blueprints/`: Contains various Blueprint directories for specific functionalities.
- `health_check/health_check.py`: Defines a Blueprint for a basic health check endpoint.
- `api/`: Contains API Blueprints further versioned.
- `api.py`: Registers the v1 Blueprint for API version 1.
- `v1/v1.py`: Defines the v1 Blueprint with API endpoints.
- `recommend-logic/`: (External Module) Contains the recommendation logic (implementation not provided here). Note: The recommend-logic module is assumed to be located outside the main project directory. You'll need to adjust the path in v1.py to reflect the actual location.

## Prerequisites
- Python 3.x (https://www.python.org/downloads/)
- Git version control system (https://git-scm.com/)
- Docker container engine (https://www.docker.com/)

## Installation
- Clone the Repository
```
git clone https://github.com/code-Gambler/movie-recommender-api.git
```
- Install Dependencies:
```
cd movie-recommender-api
pip install -r requirements.txt
```
## Running the Project Locally
### Running the Development Server
#### (Optional) Create a .env file
- Create a file named .env in the project root directory.
- For now, this file only specifies the port on which the API will run. (Default port is 5000)
#### Start the Server
```
python api/app.py
```
- This will start the Flask development server, typically accessible at `http://localhost:5000` by default.
### Using Docker
- Pull the Latest Image
```
docker pull stevenpillay/movie-recommender-api:latest
```
- Run the Docker Container
```
docker run -p 5000:5000 stevenpillay/movie-recommender-api:latest
```
- This command runs the container and maps the container port (5000) to the host port (5000).
- Adjust the host port (-p 5000:`your_desired_port`) if needed to avoid conflicts.

#### Without .env file
- The container will run on port 5000 by default if no .env file is present.
#### With .env file
- Mount the host directory containing your .env file to the container's working directory
```
docker run -p 5000:5000 --env-file .env stevenpillay/movie-recommender-api:latest
```
