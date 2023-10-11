import sqlite3

from conf import db_path


def check_last_sent_status():
    conn = sqlite3.connect(db_path())
    c = conn.cursor()
    c.execute(f'SELECT COUNT(ids) as total,'
              f'COUNT(last_send) as not_send, '
              f'COUNT(ids) - COUNT(last_send) as send '
              f'FROM messages;')
    lats_sent = c.fetchone()
    conn.commit()
    conn.close()
    return lats_sent


def mess_reset():
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute('UPDATE messages SET last_send = NULL;')
        conn.commit()
        conn.close()
        return f'History sending messages is reset, new iteration started.'
    except sqlite3.OperationalError as err:
        return f"Not reset! Error: {err}"


def search_mess(mess_text):
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute(f'SELECT ids, text_message FROM messages WHERE text_message like "%{mess_text}%"')
        messages = c.fetchall()
        conn.commit()
        conn.close()
        if not messages:
            return ["Not found"]
        return messages
    except sqlite3.OperationalError as err:
        return [f"Error: {err}"]


def get_message_id(mess_id):
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute(f'SELECT ids, text_message FROM messages WHERE ids="{mess_id}"')
        mess = c.fetchone()
        conn.commit()
        conn.close()
        if not mess:
            return None
        return mess
    except sqlite3.OperationalError as err:
        return f"Error: {err}"


def add_message(text_message):
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        c.execute(f"INSERT INTO messages (text_message) VALUES ('{text_message}')")
        conn.commit()
        c.execute('SELECT ids FROM messages ORDER BY ids DESC LIMIT 1')
        lats_sent = c.fetchone()
        conn.commit()
        conn.close()
        return f"Saved! last ID= {lats_sent[0]}"
    except sqlite3.OperationalError as err:
        return f"Not Save! Error: {err}"


def remove_message(id_mess):
    try:
        conn = sqlite3.connect(db_path())
        c = conn.cursor()
        count = c.execute(f'DELETE FROM messages WHERE ids = "{id_mess}"').rowcount
        conn.commit()
        conn.close()
        if count != 0:
            return True
        else:
            return False
    except sqlite3.OperationalError as err:
        return f"Error: {err}"