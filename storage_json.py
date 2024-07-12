import json
from typing import Dict, Any
from istorage import IStorage

class StorageJson(IStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.movies = self.load_movies()

    def load_movies(self) -> Dict[str, Dict[str, Any]]:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_movies(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.movies, file, indent=4)

    def list_movies(self) -> Dict[str, Dict[str, Any]]:
        return self.movies

    def add_movie(self, title: str, year: int, rating: float):
        self.movies[title] = {'year': year, 'rating': rating}
        self.save_movies()

    def delete_movie(self, title: str):
        if title in self.movies:
            del self.movies[title]
            self.save_movies()

    def update_movie(self, title: str, rating: float):
        if title in self.movies:
            self.movies[title]['rating'] = rating
            self.save_movies()