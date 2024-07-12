"""
CSV Storage Module
"""

import csv
from typing import Dict, Any
from istorage import IStorage

class StorageCsv(IStorage):
    """
    Implements the IStorage interface using CSV file storage.
    """

    def __init__(self, file_path: str):
        """
        Initialize the StorageCsv object.
        """
        self.file_path = file_path

    def list_movies(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns a dictionary of dictionaries containing the movies information.
        """
        movies = {}
        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movies[row['title']] = {
                        'year': int(row['year']),
                        'rating': float(row['rating']),
                        'poster': row.get('poster', ''),
                        'imdb_id': row.get('imdb_id', '')
                    }
        except FileNotFoundError:
            pass
        return movies

    def add_movie(self, title: str, year: int, rating: float, poster: str = "", imdb_id: str = ""):
        """
        Adds a movie to the database.
        """
        movies = self.list_movies()
        movies[title] = {
            'year': year,
            'rating': rating,
            'poster': poster,
            'imdb_id': imdb_id
        }
        self._save_movies(movies)

    def delete_movie(self, title: str):
        """
        Deletes a movie from the database.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            return True
        return False

    def update_movie(self, title: str, rating: float):
        """
        Updates a movie's rating in the database.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
            return True
        return False

    def _save_movies(self, movies: Dict[str, Dict[str, Any]]):
        """
        Helper method to save the movies dictionary to the CSV file.
        """
        with open(self.file_path, 'w', newline='') as file:
            fieldnames = ['title', 'year', 'rating', 'poster', 'imdb_id']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, info in movies.items():
                writer.writerow({
                    'title': title,
                    'year': info['year'],
                    'rating': info['rating'],
                    'poster': info.get('poster', ''),
                    'imdb_id': info.get('imdb_id', '')
                })