import psycopg2
import os
import shutil


def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="SongStorageDB",
            user="postgres",
            password="password",
            port=5432
        )
        print("Connected to the database.")
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database: {e}")
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
            print(f"File does not exist: {file_path}")
            return None

        if not is_valid_file(file_path):
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
        print(f"Song added successfully with ID: {song_id}")
        return song_id
    except psycopg2.Error as e:
        print(f"Unable to add song: {e}")
        return None


def add_song_to_storage(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        storage_path = 'C:\\Users\\Roxana\\Desktop\\SongStorage'
        file_name = os.path.basename(file_path)
        destination = os.path.join(storage_path, file_name)

        shutil.copy2(file_path, destination)
        return destination
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
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
            print(f"Song deleted successfully with ID: {song_id}")
            return True
        else:
            print(f"Song with ID {song_id} does not exist in the database.")
            return False
    except psycopg2.Error as e:
        print(f"Unable to delete song: {e}")
        return False


def delete_song_from_storage(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        os.remove(file_path)
        return True
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


database_connection = connect_to_database()
if database_connection:
    # add_song_to_database(
    #     database_connection,
    #     'C:\\Users\\Roxana\\Desktop\\sample-3s.mp3',
    #     'Artist Name',
    #     'Song Title',
    #     '2023-01-01',
    #     ['Tag1', 'Tag2']
    # )

    delete_song_from_database(database_connection, 2)


    database_connection.close()

    #add_song_to_storage('C:\\Users\\Roxana\\Desktop\\sample-3s.mp3')
    delete_song_from_storage('C:\\Users\\Roxana\\Desktop\\SongStorage\\sample-3s.mp3')










