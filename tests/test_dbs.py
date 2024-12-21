# testing the database status
import sqlite3
database = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\quarterback.db"

# schema validation

def test_defense_present():

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'defense_stats'")
    assert cursor.fetchone() is not None
    conn.close()


def test_gl_present():

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'gamelogs'")
    assert cursor.fetchone() is not None
    conn.close()

def test_defense_col():
    pass

def test_gl_col():
    pass