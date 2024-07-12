from abc import ABC, abstractmethod
from typing import Dict, Any

class IStorage(ABC):
    @abstractmethod
    def list_movies(self) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary of dictionaries that contains the movies information."""
        pass

    @abstractmethod
    def add_movie(self, title: str, year: int, rating: float, poster: str = "", imdb_id: str = ""):
        """Adds a movie to the database."""
        pass

    @abstractmethod
    def delete_movie(self, title: str):
        """Deletes a movie from the database."""
        pass

    @abstractmethod
    def update_movie(self, title: str, rating: float):
        """Updates a movie's rating in the database."""
        pass