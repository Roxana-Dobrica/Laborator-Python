import psycopg2
import os
import shutil
import pygame
import logging
import keyboard
from zipfile import ZipFile

song_storage_path = 'C:\\Users\\Roxana\\Desktop\\SongStorage'
log_file_path = os.path.join(song_storage_path, 'song_storage_log.log')

logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_database():
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
    return os.path.exists(file_path)


def is_valid_file(file_path):
    valid_extensions = {'.mp3', '.wav', '.aac', '.wma', '.flac'}
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in valid_extensions


def add_song_to_database(conn, file_path, artist, title, release_date, tags):
    try:
        if not file_exists(file_path):
            logging.warning(f"File does not exist: {file_path}")
            print(f"File does not exist: {file_path}")
            return None

        if not is_valid_file(file_path):
            logging.warning(f"Invalid file type: {file_path}")
            print(f"Invalid file type: {file_path}")
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
                query += f" AND ({tags_condition})"
            else:
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
    try:
        if not (output_archive.lower().endswith('.zip') or output_archive.lower().endswith('.rar')) :
            output_archive += '.zip'

        songs_to_archive = search_songs(conn, criteria)

        if not songs_to_archive:
            logging.warning("No matching songs found.")
            print("No matching songs found.")
            return False
        else:
            with ZipFile(output_archive, 'w') as archive:
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


def show_all_songs():
    conn = connect_to_database()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM songs")
        result = cursor.fetchall()
        if result:
            print("All songs:")
            for song in result:
                print(
                    f"ID: {song[0]}, File Path: {song[1]}, Artist: {song[2]}, Title: {song[3]}, Release Date: {song[4]}")
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
        print("6. Play song")
        print("7. Show all songs")
        print("0. Exit")
        print("----------------------------------------------")

        choice = input("Enter the number of your choice (or 0 to exit): ")

        if choice == '1':
            file_path = input("Enter the file path: ")
            artist = input("Enter the artist: ")
            title = input("Enter the title: ")
            release_date = input("Enter the release date: ")
            tags = input("Enter the tags (comma-separated): ").split(',')
            add_song(file_path, artist, title, release_date, tags)

        elif choice == '2':
            song_id = input("Enter the song ID: ")
            delete_song(song_id)

        elif choice == '3':
            song_id = input("Enter the song ID: ")
            artist = input("Enter the artist (or press Enter to skip): ")
            title = input("Enter the title (or press Enter to skip): ")
            release_date = input("Enter the release date (or press Enter to skip): ")
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
            release_date = input("Enter the release date (or press Enter to skip): ")
            if release_date:
                criteria['release_date'] = release_date
            tags = input("Enter the tags (comma-separated) (or press Enter to skip): ").split(',')
            if tags:
                criteria['tags'] = tags
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
            release_date = input("Enter the release date (or press Enter to skip): ")
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
            show_all_songs()

        elif choice == '8':
            print("Exiting Song Storage App. Bye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")













