"""
Movie Application Module
"""

import random
import requests
from colorama import Fore, Style
from istorage import IStorage

API_KEY = 'd5ee8f11'  # Your OMDB API key


def get_string_input(prompt: str) -> str:
    """Handle empty inputs from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_int_input(prompt: str) -> int:
    """Handle invalid integer inputs from the user."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_float_input(prompt: str) -> float:
    """Handle invalid float input from the user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def fetch_movie_details(title):
    """Fetch movie details from the OMDb API."""
    url = f'http://www.omdbapi.com/?apikey={API_KEY}&t={title}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            return data
        else:
            print(f"Error: {data.get('Error')}")
            return None
    elif response.status_code == 401:
        print("Unauthorized: Check your API key.")
        return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None


class MovieApp:
    """Main application class for managing the movie database."""

    def __init__(self, storage: IStorage):
        self.storage = storage

    def run(self):
        """Run the main application loop."""
        while True:
            self.display_menu()
            try:
                choice = get_int_input(Fore.CYAN + "Enter choice (0-9): ")
                if choice < 0 or choice > 9:
                    raise ValueError("Invalid menu option")

                if choice == 0:
                    print("Bye!")
                    break
                elif choice == 1:
                    self.list_movies()
                elif choice == 2:
                    self.add_movie()
                elif choice == 3:
                    self.delete_movie()
                elif choice == 4:
                    self.update_movie()
                elif choice == 5:
                    self.display_stats()
                elif choice == 6:
                    self.random_movie()
                elif choice == 7:
                    self.search_movie()
                elif choice == 8:
                    self.movies_sorted_by_rating()
                elif choice == 9:
                    self.generate_website()
            except ValueError as e:
                print(Fore.RED + f"Invalid input: {str(e)}")
            except Exception as e:
                print(Fore.RED + f"An unexpected error occurred: {str(e)}")

            input(Fore.YELLOW + "Press enter to continue: ")
            print()

    def display_menu(self):
        """Display the main menu options."""
        print(Style.BRIGHT + Fore.GREEN + "********** My Movies Database **********\n")
        print("Menu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate website\n")

    def list_movies(self):
        """List all movies in the database."""
        movies = self.storage.list_movies()
        print(f"{len(movies)} movies in total")
        for title, info in movies.items():
            print(f"{title} ({info['year']}): Rating {info['rating']}")

    def add_movie(self):
        """Add a new movie to the database."""
        title = get_string_input("Enter movie title: ")
        year = get_int_input("Enter movie year: ")
        rating = get_float_input("Enter movie rating: ")
        self.storage.add_movie(title, year, rating)
        print(f"Movie {title} added successfully.")

    def delete_movie(self):
        """Delete a movie from the database."""
        title = get_string_input("Enter the name of the movie to delete: ")
        if self.storage.delete_movie(title):
            print("Movie deleted successfully!")
        else:
            print("Movie not found in the database.")

    def update_movie(self):
        """
        Update a movie's rating in the database or return to the main menu.
        The movie title search is case-insensitive.
        """
        while True:
            title = get_string_input("Enter movie name (or 'q' to quit): ")
            if title.lower() == 'q':
                print("Returning to main menu.")
                return

            movies = self.storage.list_movies()
            # Create a case-insensitive dictionary for searching
            movies_lower = {k.lower(): (k, v) for k, v in movies.items()}

            if title.lower() in movies_lower:
                original_title, movie_info = movies_lower[title.lower()]
                while True:
                    rating_input = input(f"Enter new rating for '{original_title}' (or 'q' to quit): ")
                    if rating_input.lower() == 'q':
                        print("Returning to main menu.")
                        return

                    try:
                        rating = float(rating_input)
                        if 0 <= rating <= 10:
                            if self.storage.update_movie(original_title, rating):
                                print(f"Movie '{original_title}' successfully updated with new rating: {rating}")
                            return
                        else:
                            print("Rating must be between 0 and 10.")
                    except ValueError:
                        print("Invalid input. Please enter a number or 'q' to quit.")
            else:
                print(f"Movie '{title}' not found in the database.")
                continue

    def display_stats(self):
        """Display statistics about the movies in the database."""
        movies = self.storage.list_movies()

        if not movies:
            print("No movies found.")
            return

        ratings = [float(info['rating']) for info in movies.values()]

        if ratings:
            avg = sum(ratings) / len(ratings)
            med = sorted(ratings)[len(ratings) // 2]
            best_movie = max(movies.items(), key=lambda x: x[1]['rating'])
            worst_movie = min(movies.items(), key=lambda x: x[1]['rating'])

            print(f"Average rating: {avg:.2f}")
            print(f"Median rating: {med:.2f}")
            print(f"Best movie: {best_movie[0]}, Rating: {best_movie[1]['rating']}")
            print(f"Worst movie: {worst_movie[0]}, Rating: {worst_movie[1]['rating']}")
        else:
            print("No valid ratings found in the database.")

    def random_movie(self):
        """Display a random movie from the database."""
        movies = self.storage.list_movies()
        if movies:
            title = random.choice(list(movies.keys()))
            info = movies[title]
            print(f"Your movie for tonight: {title}, it's rated {info['rating']}")
        else:
            print("No movies in the database.")

    def search_movie(self):
        """Search for a movie by title."""
        search_term = get_string_input(Fore.CYAN + "Enter part of movie name: ")
        movies = self.storage.list_movies()
        found = False
        for title, info in movies.items():
            if search_term.lower() in title.lower():
                print(Fore.GREEN + f"Found: {title} ({info['year']}) with rating {info['rating']}")
                found = True
        if not found:
            print(Fore.RED + f"No movies found with '{search_term}'")

    def movies_sorted_by_rating(self):
        """List movies sorted by rating."""
        movies = self.storage.list_movies()
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        for title, info in sorted_movies:
            print(f"{title} ({info['year']}): {info['rating']}")

    def generate_website(self):
        """Generate a static HTML website for the movie collection."""
        movies = self.storage.list_movies()
        try:
            with open('index_template.html', 'r') as file:
                template = file.read()

            movie_grid_items = []
            for title, info in movies.items():
                movie_item = f'''
                    <div class="movie-item">
                        <h2>{title} ({info['year']})</h2>
                        <p>Rating: {info['rating']}</p>
                    </div>
                    '''
                movie_grid_items.append(movie_item)

            movie_grid_html = '\n'.join(movie_grid_items)
            website_content = template.replace('__TEMPLATE_TITLE__', 'My Movie App')
            website_content = website_content.replace('__TEMPLATE_MOVIE_GRID__', movie_grid_html)

            with open('index.html', 'w') as file:
                file.write(website_content)

            print("Website was generated successfully.")
        except FileNotFoundError:
            print("Error: index_template.html file not found.")
        except Exception as e:
            print(f"An unexpected error occurred while generating the website: {str(e)}")


class EnhancedMovieApp(MovieApp):
    """Enhanced version of MovieApp that includes poster and link functionality."""

    def add_movie(self):
        """Add a new movie to the database, including poster and IMDB ID."""
        title = get_string_input("Enter new movie name: ")
        movies = self.storage.list_movies()

        if title in movies:
            print(f"Movie {title} already exists!")
            return

        try:
            details = fetch_movie_details(title)
            if details:
                year = int(details.get('Year', 0))
                rating = float(details.get('imdbRating', 0))
                poster = details.get('Poster', '')
                imdb_id = details.get('imdbID', '')
                self.storage.add_movie(title, year, rating, poster, imdb_id)
                print(f"Movie {title} successfully added")
            else:
                print("Failed to fetch movie details. Please check the title and try again.")
        except Exception as e:
            print(f"An error occurred while adding the movie: {str(e)}")

    def generate_website(self):
        """Generate a static HTML website for the movie collection, including posters and links."""
        movies = self.storage.list_movies()
        try:
            with open('index_template.html', 'r') as file:
                template = file.read()

            movie_grid_items = []
            for title, info in movies.items():
                poster = info.get('poster', '/api/placeholder/400/320')
                imdb_link = f"https://www.imdb.com/title/{info.get('imdb_id', '')}" if info.get('imdb_id') else '#'
                movie_item = f'''
                    <div class="movie-item">
                        <div class="poster-container">
                            <a href="{imdb_link}" target="_blank">
                                <img src="{poster}" alt="{title} Poster">
                            </a>
                        </div>
                        <h2>{title} ({info['year']})</h2>
                        <p>Rating: {info['rating']}</p>
                    </div>
                    '''
                movie_grid_items.append(movie_item)

            movie_grid_html = '\n'.join(movie_grid_items)
            website_content = template.replace('__TEMPLATE_TITLE__', 'My Movie App')
            website_content = website_content.replace('__TEMPLATE_MOVIE_GRID__', movie_grid_html)

            with open('index.html', 'w') as file:
                file.write(website_content)

            print("Website was generated successfully.")
        except FileNotFoundError:
            print("Error: index_template.html file not found.")
        except Exception as e:
            print(f"An unexpected error occurred while generating the website: {str(e)}")
