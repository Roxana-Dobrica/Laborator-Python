import psycopg2
import os
import shutil
import pygame
import logging
import keyboard
from datetime import datetime
from zipfile import ZipFile

song_storage_path = 'C:\\Users\\Roxana\\Desktop\\SongStorage'
log_file_path = os.path.join(song_storage_path, 'song_storage_log.log')

logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_database():
    """
    Connects to the database using the psycopg2 library.

    Parameters
    ----------
        None

    Returns
    -------
        psycopg2.extensions.connection or None: The active database connection, or None if the connection fails.

    Raises
    ------
        psycopg2.Error: If an error occurs during the database transaction.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="SongStorageDB",
            user="postgres",
            password="password",
            port=5432
        )
        logging.info("Connected to the database.")
        return conn
    except psycopg2.Error as e:
        logging.error("Unable to connect to the database: %s", e)
        return None


def file_exists(file_path):
    """
    Checks if a file exists.

    Parameters
    ----------
        file_path (str): The file path to check.

    Returns
    -------
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def is_valid_file(file_path):
    """
    Checks if a file has a valid file type.

    Parameters
    ----------
        file_path (str): The file path to check.

    Returns
    -------
        bool: True if the file has a valid file type, False otherwise.
    """
    valid_extensions = {'.mp3', '.wav', '.aac', '.wma', '.flac'}
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in valid_extensions


def is_valid_date(date_string):
    """
    Checks if a date string has a valid YYYY-MM-DD format.

    Parameters
    ----------
        date_string (str): The date string to check.

    Returns
    -------
        bool: True if the date string has a valid format, False otherwise.
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_all_tags(conn):
    """
    Retrieves all tags from the 'tags' table.

    Parameters:
    ----------
        conn (psycopg2.extensions.connection): The active database connection.

    Returns:
    -------
        list or None: A list of tags, or None if the operation fails.
    """
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM tags")
        result = cursor.fetchall()

        tags_list = [{"id": tag[0], "name": tag[1]} for tag in result]
        return tags_list
    except psycopg2.Error as e:
        logging.error("An error occurred while retrieving tags: %s", e)
        print(f"An error occurred while retrieving tags: {e}")
        return None


def get_all_songtags(conn):
    """
    Retrieves all entries from the 'songtags' table.

    Parameters:
    ----------
        conn (psycopg2.extensions.connection): The active database connection.

    Returns:
    -------
        list or None: A list of songtags, or None if the operation fails.
    """
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT song_id, tag_id FROM songtags")
        result = cursor.fetchall()

        songtags_list = [{"song_id": songtag[0], "tag_id": songtag[1]} for songtag in result]
        return songtags_list
    except psycopg2.Error as e:
        logging.error("An error occurred while retrieving songtags: %s", e)
        print(f"An error occurred while retrieving songtags: {e}")
        return None


def add_song_to_database(conn, file_path, artist, title, release_date, tags):
    """
        Adds a new song to the database.

        This function takes the necessary information about a song and inserts this information into the
        'songs', 'tags', and 'songtags' tables in the database. It performs checks to ensure the file
        exists and has a valid file type. \n
        Parameters
        ----------
        conn (psycopg2.extensions.connection): The active database connection.
        file_path (str): The file path of the song.
        artist (str): The artist of the song.
        title (str): The title of the song.
        release_date (str): The release date of the song.
        tags (list): A list of tags associated with the song. \n

        Returns
        -------
        int or None: The ID of the added song in the 'songs' table, or None if the addition fails.\n

        Raises
        ------
        psycopg2.Error: If an error occurs during the database transaction.
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file type is not supported.
        """
    try:
        if not file_exists(file_path):
            logging.warning(f"File does not exist: {file_path}")
            print(f"File does not exist: {file_path}")
            return None

        if not is_valid_file(file_path):
            logging.warning(f"Invalid file type: {file_path}")
            print(f"Invalid file type: {file_path}")
            return None

        if not is_valid_date(release_date):
            logging.warning(f"Invalid date format: {release_date}. Please use YYYY-MM-DD.")
            print(f"Invalid date format: {release_date}. Please use YYYY-MM-DD.")
            return None

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO songs(file_path, artist, title, release_date)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (file_path, artist, title, release_date))

        song_id = cursor.fetchone()[0]

        for tag in tags:
            cursor.execute("""
                INSERT INTO tags(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (tag,))

            cursor.execute("""
                INSERT INTO songtags(song_id, tag_id)
                VALUES (%s, (SELECT id FROM tags WHERE name = %s));
            """, (song_id, tag))

        conn.commit()
        logging.info(f"Song added successfully with ID: {song_id}")
        print(f"Song added successfully: {song_id} - {artist} - {title} - {release_date} - {tags}")
        return song_id
    except psycopg2.Error as e:
        logging.error("Unable to add song: %s", e)
        print(f"Failed to add song to database. {e}")
        return None


def add_song_to_storage(file_path):
    """
    Adds a new song to the storage folder.

    This function takes the file path of a song and copies it to the storage folder. It performs
    checks to ensure the file exists and does not already exist in the storage folder.

    Parameters
    ----------
        file_path (str): The file path of the song.

    Returns
    -------
        str or None: The file path of the song in the storage folder, or None if the addition fails.

    Raises
    ------
        FileNotFoundError: If the specified file_path does not exist.
        FileExistsError: If a file with the same name already exists in the storage folder.
        shutil.Error: If an error occurs during the file copy.
        Exception: If an unexpected error occurs.
    """

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        file_name = os.path.basename(file_path)
        destination = os.path.join(song_storage_path, file_name)

        if os.path.exists(destination):
            raise FileExistsError(f"A file with the same name already exists in the storage folder: {destination}")

        try:
            shutil.copy2(file_path, destination)
        except shutil.Error as e:
            logging.error(f"Error copying file: {e}")
            return None
        logging.info(f"Song added to storage: {destination}")
        print(f"Song added successfully to storage: {destination}")
        return destination
    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        print(f"Failed to add song to storage. {e}")
        return None
    except FileExistsError as e:
        logging.error(f"Error: {e}")
        print(f"Failed to add song to storage. {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"Failed to add song to storage. {e}")
        return None


def add_song(file_path, artist, title, release_date, tags):
    """
    Adds a new song to the database and storage folder.

    This function takes the necessary information about a song and inserts this information into the
    'songs', 'tags', and 'songtags' tables in the database. It also copies the song to the storage folder.
    It performs checks to ensure the file exists and has a valid file type.

    Parameters
    ----------
        file_path (str): The file path of the song.
        artist (str): The artist of the song.
        title (str): The title of the song.
        release_date (str): The release date of the song.
        tags (list): A list of tags associated with the song.

    Returns
    -------
        int or None: The ID of the added song in the 'songs' table, or None if the addition fails.

    Raises
    ------
        psycopg2.Error: If an error occurs during the database transaction.
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file type is not supported.
    """
    database_connection = connect_to_database()
    if database_connection:
        song_id = add_song_to_database(database_connection, file_path, artist, title, release_date, tags)
        if song_id:
            add_song_to_storage(file_path)
            database_connection.close()
            return song_id
        else:
            database_connection.close()
            return None
    else:
        return None


def delete_song_from_database(conn, song_id):

    """
    Deletes a song from the database.

    This function removes a song and its associated tags from the 'songs' table and 'tags' table
    in the database. It performs checks to ensure the song exists in the database. \n

    Parameters:
    ----------
        conn (psycopg2.extensions.connection): The active database connection.
        song_id (int): The ID of the song to be deleted.
    Returns:
    -------
        bool: True if the deletion is successful, False otherwise.
    Raises:
    ------
        psycopg2.Error: If an error occurs during the database transaction.
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM songs WHERE id = %s;
        """, (song_id,))
        existing_id = cursor.fetchone()

        if existing_id:
            cursor.execute("""
                DELETE FROM songtags 
                WHERE song_id = %s;
            """, (song_id,))

            cursor.execute("""
                DELETE FROM songs
                WHERE id = %s;
            """, (song_id,))

            conn.commit()
            logging.info(f"Song deleted successfully with ID: {song_id}")
            print(f"Song deleted successfully with ID: {song_id}")
            return True
        else:
            logging.warning(f"Song with ID {song_id} does not exist in the database.")
            print(f"Song with ID {song_id} does not exist in the database.")
            return False
    except psycopg2.Error as e:
        logging.error("Unable to delete song: %s", e)
        print(f"Failed to delete song from database. {e}")
        return False


def delete_song_from_storage(file_name):
    """
    Deletes a song from the storage folder.

    This function removes a song from the storage folder. It performs checks to ensure the song exists
    in the storage folder.

    Parameters
    ----------
        file_name (str): The file name of the song to be deleted.

    Returns
    -------
        bool: True if the deletion is successful, False otherwise.

    Raises
    ------
        FileNotFoundError: If the specified file_name does not exist in the storage folder.
        Exception: If an unexpected error occurs.
    """
    try:
        storage_path = os.path.join(song_storage_path, file_name)

        if not os.path.exists(storage_path):
            raise FileNotFoundError(f"The file '{storage_path}' does not exist.")

        os.remove(storage_path)
        logging.info(f"Song deleted from storage: {storage_path}")
        print(f"Song deleted successfully from storage: {storage_path}")
        return True
    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        print(f"The file does not exist.")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"Failed to delete song from storage. {e}")
        return False


def get_song_path_from_database(conn, song_id):
    """
    Retrieves the file path of a song from the database.

    Parameters
    ----------
        conn (psycopg2.extensions.connection): The active database connection.
        song_id (int): The ID of the song to be retrieved.

    Returns
    -------
        str or None: The file path of the song, or None if the song does not exist in the database.

    Raises
    ------
        psycopg2.Error: If an error occurs during the database transaction.
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT file_path FROM songs WHERE id = %s;
        """, (song_id,))
        result = cursor.fetchone()

        if result:
            song_path = result[0]
            logging.info(f"Song path retrieved successfully: {song_path}")
            print(f"Song path retrieved successfully: {song_path}")
            return song_path
        else:
            logging.warning(f"Song with ID {song_id} does not exist in the database.")
            print(f"Song with ID {song_id} does not exist in the database.")
            return None
    except psycopg2.Error as e:
        logging.error("Unable to retrieve song path: %s", e)
        print(f"Failed to retrieve song path from database. {e}")
        return None


def delete_song(song_id):
    """
    Deletes a song from the database and storage folder.

    This function removes a song and its associated tags from the 'songs' table and 'tags' table
    in the database. It also removes the song from the storage folder. It performs checks to ensure
    the song exists in the database and storage folder.

    Parameters:
    ----------
        song_id (int): The ID of the song to be deleted.

    Returns:
    -------
        bool: True if the deletion is successful, False otherwise.

    Raises:
    ------
        psycopg2.Error: If an error occurs during the database transaction.
        FileNotFoundError: If the specified file_name does not exist in the storage folder.
        Exception: If an unexpected error occurs.
    """
    database_connection = connect_to_database()

    if database_connection:
        try:
            song_path = get_song_path_from_database(database_connection, song_id)
            if delete_song_from_database(database_connection, song_id):
                if song_path:
                    file_name = os.path.basename(song_path)
                    delete_song_from_storage(file_name)
                    return True
                else:
                    return False
            else:
                return False

        finally:
            database_connection.close()
    else:
        return False


def modify_data(conn, song_id, artist=None, title=None, release_date=None, tags=None):
    """
    Modifies the metadata of a song in the database.

    This function modifies the metadata of a song in the 'songs' table in the database. It performs
    checks to ensure the song exists in the database. \n
    Parameters:
    ----------
        conn (psycopg2.extensions.connection): The active database connection.
        song_id (int): The ID of the song to be modified.
        artist (str): The new artist of the song.
        title (str): The new title of the song.
        release_date (str): The new release date of the song.
        tags (list): A list of new tags associated with the song.
    Returns:
    -------
        bool: True if the modification is successful, False otherwise.
    Raises:
    ------
        psycopg2.Error: If an error occurs during the database transaction.
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM songs WHERE id = %s;
        """, (song_id,))
        existing_id = cursor.fetchone()

        if existing_id:
            if artist:
                cursor.execute("""
                    UPDATE songs
                    SET artist = %s
                    WHERE id = %s;
                """, (artist, song_id))

            if title:
                cursor.execute("""
                    UPDATE songs
                    SET title = %s
                    WHERE id = %s;
                """, (title, song_id))

            if release_date:
                if not is_valid_date(release_date):
                    logging.warning(f"Invalid date format: {release_date}. Please use YYYY-MM-DD.")
                    print(f"Invalid date format: {release_date}. Please use YYYY-MM-DD.")
                    return False
                cursor.execute("""
                    UPDATE songs
                    SET release_date = %s
                    WHERE id = %s;
                """, (release_date, song_id))

            if tags:
                cursor.execute("""
                    DELETE FROM songtags 
                    WHERE song_id = %s;
                """, (song_id,))

                for tag in tags:
                    cursor.execute("""
                        INSERT INTO tags(name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING;
                    """, (tag,))

                    cursor.execute("""
                        INSERT INTO songtags(song_id, tag_id)
                        VALUES (%s, (SELECT id FROM tags WHERE name = %s));
                    """, (song_id, tag))

            conn.commit()
            logging.info(f"Song updated successfully with ID: {song_id}")
            print(f"Song updated successfully: {song_id} - {artist} - {title} - {release_date} - {tags}")
            return True
        else:
            logging.warning(f"Song with ID {song_id} does not exist in the database.")
            print(f"Song with ID {song_id} does not exist in the database.")
            return False
    except psycopg2.Error as e:
        logging.error("Unable to update song: %s", e)
        print(f"Failed to update song in database. {e}")
        return False


def search_songs(conn, criteria):
    """
    Searches for songs based on the specified criteria.

    This function searches for songs in the 'songs' table in the database based on the specified criteria. \n
    Parameters:
    ----------
        conn (psycopg2.extensions.connection): The active database connection.
        criteria (dict): A dictionary containing the search criteria.
    Returns:
    -------
        list or None: A list of songs matching the search criteria, or None if the search fails.
    Raises:
    ------
        psycopg2.Error: If an error occurs during the database transaction.
    """
    try:
        cursor = conn.cursor()

        query = """
            SELECT s.id, s.file_path, s.artist, s.title, s.release_date, COALESCE(array_agg(t.name), ARRAY[]::text[])
            FROM songs s
            LEFT JOIN songtags st ON s.id = st.song_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE true
        """

        for key, value in criteria.items():
            if key == 'tags':
                tags_condition = ' OR '.join([f"t.name LIKE '%{tag}%'" for tag in value])
                if tags_condition:
                    query += f" AND ({tags_condition})"
            elif key == 'release_date':
                if is_valid_date(value):
                    query += f" AND {key} = '{value}'::date"
            elif key == 'file_extension':
                if value:
                    query += f" AND s.file_path ILIKE '%{value}'"
            else:
                if value:
                    query += f" AND {key} LIKE '%{value}%'"

        query += " GROUP BY s.id, s.file_path, s.artist, s.title, s.release_date"

        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            logging.info("Search results:")
            print("Search results:")
            for song in result:
                logging.info(
                    f"ID: {song[0]}, File Path: {song[1]}, Artist: {song[2]}, Title: {song[3]}, Release Date: {song[4]}, Tags: {song[5]}")
                print(
                    f"ID: {song[0]}, File Path: {song[1]}, Artist: {song[2]}, Title: {song[3]}, Release Date: {song[4]}, Tags: {song[5]}")
        else:
            logging.warning("No matching songs found.")
            print("No matching songs found.")

        return result
    except psycopg2.Error as e:
        logging.error("An error occurred during search: %s", e)
        print(f"An error occurred during search: {e}")
        return None


def create_save_list(conn, output_archive, criteria):
    """
    Creates a save list of songs matching the search criteria.

    This function searches for songs in the 'songs' table in the database based on the specified criteria.
    It then creates a save list of the songs in the storage folder. \n
    Parameters:
    ----------
        conn (psycopg2.extensions.connection): The active database connection.
        output_archive (str): The path of the output archive.
        criteria (dict): A dictionary containing the search criteria.
    Returns:
    -------
        bool: True if the save list is created successfully, False otherwise.
    Raises:
    ------
        psycopg2.Error: If an error occurs during the database transaction.
    """
    try:
        if not (output_archive.lower().endswith('.zip') or output_archive.lower().endswith('.rar')) :
            output_archive += '.zip'

        songs_to_archive = search_songs(conn, criteria)

        if not songs_to_archive:
            logging.warning("No matching songs found.")
            print("No matching songs found.")
            return False
        else:
            destination_path = os.path.join(song_storage_path, os.path.basename(output_archive))
            with ZipFile(destination_path, 'w') as archive:
                for song in songs_to_archive:
                    song_path = song[1]
                    if os.path.exists(song_path):
                        archive.write(song_path, os.path.basename(song_path))

        logging.info(f"Save list created successfully: {output_archive}")
        print(f"Save list created successfully: {output_archive}")
        return True
    except Exception as e:
        logging.error(f"An error occurred while creating the save list: {e}")
        print(f"An error occurred while creating the save list: {e}")
        return False


def play_song(file_path):
    """
    Plays a song.

    This function plays a song using the Pygame library. It performs checks to ensure the file exists
    and has a valid file type. \n
    Parameters:
    ----------
        file_path (str): The file path of the song.
    Returns:
    -------
        bool: True if the song is played successfully, False otherwise.
    Raises:
    ------
        FileNotFoundError: If the specified file_path does not exist.
        pygame.error: If an error occurs during the song playback.
        Exception: If an unexpected error occurs.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        pygame.init()
        played_song = pygame.mixer.Sound(file_path)
        played_song.play()

        logging.info(f"Song started: {file_path}")
        print(f"Song started: {file_path}")

        while pygame.mixer.get_busy() and not keyboard.is_pressed('enter'):
            pygame.time.Clock().tick(10)

        pygame.mixer.stop()
        pygame.quit()

        logging.info(f"Song stopped: {file_path}")
        print(f"Song stopped: {file_path}")

    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        print(f"The file does not exist.")
        return False
    except pygame.error as e:
        logging.error(f"Pygame error: {e}")
        print(f"Pygame error: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        return False


def play_song_by_id(conn, song_id):
    """
    Plays a song based on its ID.

    This function retrieves the file path of a song using the specified ID from the database
    and plays the song using the Pygame library.

    Parameters
    ----------
        conn (psycopg2.extensions.connection): The active database connection.
        song_id (int): The ID of the song to be played.

    Returns
    -------
        bool: True if the song is played successfully, False otherwise.

    Raises
    ------
        FileNotFoundError: If the specified file_path does not exist.
        pygame.error: If an error occurs during the song playback.
        Exception: If an unexpected error occurs.
    """
    try:
        cursor = conn.cursor()

        # Retrieve file path based on song_id
        cursor.execute(f"SELECT file_path FROM songs WHERE id = {song_id}")
        result = cursor.fetchone()

        if not result:
            logging.warning(f"No song found with ID {song_id}.")
            print(f"No song found with ID {song_id}.")
            return False

        file_path = result[0]

        if not os.path.exists(file_path) or not is_valid_file(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist or is not a valid audio file.")

        pygame.init()
        played_song = pygame.mixer.Sound(file_path)
        played_song.play()

        logging.info(f"Song started: {file_path}")
        print(f"Song started: {file_path}")

        while pygame.mixer.get_busy() and not keyboard.is_pressed('enter'):
            pygame.time.Clock().tick(10)

        pygame.mixer.stop()
        pygame.quit()

        logging.info(f"Song stopped: {file_path}")
        print(f"Song stopped: {file_path}")
        return True

    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        print(f"The file does not exist or is not a valid audio file.")
        return False
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
        print(f"Database error: {e}")
        return False
    except pygame.error as e:
        logging.error(f"Pygame error: {e}")
        print(f"Pygame error: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        return False


def show_all_songs():
    """
    Displays all songs in the database.

    This function displays all songs in the 'songs' table in the database and associated tags. \n
    Parameters:
    ----------
        conn (psycopg2.extensions.connection): The active database connection.
    Returns:
    -------
        bool: True if the songs are displayed successfully, False otherwise.
    Raises:
    ------
        psycopg2.Error: If an error occurs during the database transaction.
    """
    conn = connect_to_database()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.file_path, s.artist, s.title, s.release_date, COALESCE(array_agg(t.name), ARRAY[]::text[]) AS tags
            FROM songs s
            LEFT JOIN songtags st ON s.id = st.song_id
            LEFT JOIN tags t ON st.tag_id = t.id
            GROUP BY s.id
        """)
        result = cursor.fetchall()
        if result:
            print("All songs:")
            for song in result:
                print(
                    f"ID: {song[0]}, File Path: {song[1]}, Artist: {song[2]}, Title: {song[3]}, Release Date: {song[4]}, Tags: {song[5]}")
            logging.info("All songs displayed successfully.")
        else:
            print("No songs found.")
            logging.warning("No songs found.")
    except psycopg2.Error as e:
        print(f"An error occurred during search: {e}")
        logging.error("An error occurred during search: %s", e)
        return None
    finally:
        conn.close()


if __name__ == '__main__':
    conn = connect_to_database()

    print("Welcome to Song Storage App!")

    while True:
        print("----------------------------------------------")
        print("Please choose one of the following options:")
        print("1. Add a song to the database")
        print("2. Delete a song from the database")
        print("3. Modify metadata")
        print("4. Search songs")
        print("5. Create save list")
        print("6. Play song by path")
        print("7. Play song by ID")
        print("8. Show all songs")
        print("9. Show all tags")
        print("10. Show all songtags")
        print("0. Exit")
        print("----------------------------------------------")

        choice = input("Enter the number of your choice (or 0 to exit): ")

        if choice == '1':
            file_path = input("Enter the file path: ")
            artist = input("Enter the artist: ")
            title = input("Enter the title: ")
            release_date = input("Enter the release date (YYYY-MM-DD): ")
            tags = input("Enter the tags (comma-separated): ").split(',')
            add_song(file_path, artist, title, release_date, tags)

        elif choice == '2':
            song_id = input("Enter the song ID: ")
            delete_song(song_id)

        elif choice == '3':
            song_id = input("Enter the song ID: ")
            artist = input("Enter the artist (or press Enter to skip): ")
            title = input("Enter the title (or press Enter to skip): ")
            release_date = input("Enter the release date (YYYY-MM-DD) (or press Enter to skip): ")
            tags = input("Enter the tags (comma-separated) (or press Enter to skip): ").split(',')
            modify_data(conn, song_id, artist, title, release_date, tags)

        elif choice == '4':
            criteria = {}
            artist = input("Enter the artist (or press Enter to skip): ")
            if artist:
                criteria['artist'] = artist
            title = input("Enter the title (or press Enter to skip): ")
            if title:
                criteria['title'] = title
            release_date = input("Enter the release date (YYYY-MM-DD) (or press Enter to skip): ")
            if release_date:
                criteria['release_date'] = release_date
            tags = input("Enter the tags (comma-separated) (or press Enter to skip): ").split(',')
            if tags:
                criteria['tags'] = tags
            file_extension = input("Enter the file extension (or press Enter to skip): ")
            if file_extension:
                criteria['file_extension'] = file_extension
            search_songs(conn, criteria)

        elif choice == '5':
            output_archive = input("Enter the output archive path: ")
            criteria = {}
            artist = input("Enter the artist (or press Enter to skip): ")
            if artist:
                criteria['artist'] = artist
            title = input("Enter the title (or press Enter to skip): ")
            if title:
                criteria['title'] = title
            release_date = input("Enter the release date (YYYY-MM-DD) (or press Enter to skip): ")
            if release_date:
                criteria['release_date'] = release_date
            tags = input("Enter the tags (comma-separated) (or press Enter to skip): ").split(',')
            if tags:
                criteria['tags'] = tags
            create_save_list(conn, output_archive, criteria)

        elif choice == '6':
            file_path = input("Enter the file path: ")
            play_song(file_path)

        elif choice == '7':
            song_id = input("Enter the song ID: ")
            play_song_by_id(conn, song_id)

        elif choice == '8':
            show_all_songs()

        elif choice == '9':
            print("All tags:")
            for tag in get_all_tags(conn):
                print(tag)

        elif choice == '10':
            print("All songtags:")
            for songtag in get_all_songtags(conn):
                print(songtag)

        elif choice == '0':
            print("Exiting Song Storage App. Bye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")













