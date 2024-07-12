"""
Movie Database Application Entry Point
"""

from movie_app import EnhancedMovieApp
from storage_csv import StorageCsv


# If JSON storage is preferred, uncomment the following line:
# from storage_json import StorageJson


def main():
    """
    Main function to run the Movie Database Application.
    """
    # Create an instance of the storage class
    # for easier switch between CSV and JSON storage
    storage = StorageCsv('movies.csv')
    # in case of JSON storage, comment out the line above and uncomment below:
    # storage = StorageJson('movies.json')

    # Create an instance of MovieApp with the chosen storage
    app = EnhancedMovieApp(storage)

    # Run the application
    app.run()


if __name__ == "__main__":
    main()
