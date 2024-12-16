import sqlite3

# Fungsi untuk membuat database dan tabel jika belum ada
def setup_database():
    conn = sqlite3.connect("bibliography.db")
    cursor = conn.cursor()
    conn.commit()
    conn.close()

def create_table(table_name):
    conn = sqlite3.connect("bibliography.db")
    cursor = conn.cursor()

    # Membuat tabel jika belum ada
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            authors TEXT,
            date TEXT,
            link TEXT,
            source TEXT,
            format TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(table_name, filtered_items, format_choice):
    conn = sqlite3.connect("bibliography.db")
    cursor = conn.cursor()

    # Pastikan tabel ada
    create_table(table_name)

    # Hapus semua data sebelumnya di tabel tersebut
    cursor.execute(f"DELETE FROM {table_name}")

    # Simpan data baru
    for item in filtered_items:
        cursor.execute(f"""
            INSERT INTO {table_name} (title, authors, date, link, source, format)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item.get("title"),
            ", ".join(item.get("authors", [])),  # Gabungkan daftar authors jadi string
            item.get("date"),
            item.get("link"),
            item.get("source"),
            format_choice
        ))

    conn.commit()
    conn.close()
    print(f"Data pustaka berhasil disimpan ke tabel '{table_name}'.")

def load_from_database(table_name):
    conn = sqlite3.connect("bibliography.db")
    cursor = conn.cursor()

    # Ambil semua data pustaka dari tabel yang diminta
    cursor.execute(f"SELECT title, authors, date, link, source, format FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()

    # Konversi hasil ke dalam bentuk dictionary
    if rows:
        format_choice = rows[0][5] if rows else "IEEE"  # Ambil format dari entri pertama
        filtered_items = [
            {
                "title": row[0],
                "authors": row[1].split(", "),  # Pisahkan kembali string authors jadi list
                "date": row[2],
                "link": row[3],
                "source": row[4],
            }
            for row in rows
        ]
        return filtered_items, format_choice
    return [], "IEEE"



def load_tables_from_database():
    conn = sqlite3.connect("bibliography.db")
    cursor = conn.cursor()

    # Query to get all table names from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    # Filter out the "sqlite_sequence" table
    return [table[0] for table in tables if table[0] != "sqlite_sequence"]


def remove_table(name):
    conn = sqlite3.connect("bibliography.db")
    cursor = conn.cursor()
    
    try:
        # Drop the table from the database
        cursor.execute(f"DROP TABLE IF EXISTS {name}")
        conn.commit()
        print(f"Table {name} removed successfully.")
    except sqlite3.Error as e:
        print(f"Error removing table {name}: {e}")
    finally:
        conn.close()
        