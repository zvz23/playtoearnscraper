import sqlite3

DB_NAME = 'playtoearn.db'
TABLE_NAME = 'games'

def get_keys(game_info: dict):
    keys = []
    values = []
    
    for key, value in game_info.items():
        if value is not None:
            keys.append(key)
            values.append(value)
    return (keys, values)
    

def save_url(url: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO {TABLE_NAME}(URL) VALUES(?)", [url])

def update_info(id: int, game_info: dict):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        keys, values = get_keys(game_info)
        values.append(id)
        UPDATE_QUERY = f"UPDATE {TABLE_NAME} SET {', '.join([f'{key}=?' for key in keys])} WHERE ID=?"
        cursor.execute(UPDATE_QUERY, values)
        conn.commit()

def get_urls_without_info():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(f"SELECT ID, URL FROM {TABLE_NAME} WHERE NAME IS NULL")
        return cursor.fetchall()

def get_urls_with_info():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(f"SELECT ID, URL FROM {TABLE_NAME} WHERE NAME IS NOT NULL")
        return cursor.fetchall()

def get_urls_without_info_count():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(ID) FROM {TABLE_NAME} WHERE NAME IS NULL")
        return cursor.fetchone()[0]
    
def get_urls_with_info_count():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(ID) FROM {TABLE_NAME} WHERE NAME IS NOT NULL")
        return cursor.fetchone()[0]
