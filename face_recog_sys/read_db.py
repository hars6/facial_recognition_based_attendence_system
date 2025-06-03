
import sqlite3

def display_database():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    # Display faces table
    print("\n--- [FACES TABLE] ---\n")
    c.execute("SELECT * FROM faces")
    faces = c.fetchall()
    for face in faces:
        print(face)

    # Display sessions table
    print("\n--- [SESSIONS TABLE] ---\n")
    c.execute("SELECT * FROM sessions")
    sessions = c.fetchall()
    for session in sessions:
        print(session)

    conn.close()

if __name__ == "__main__":
    display_database()













# import sqlite3
#
# # DB file ka naam yahan likh
# db_file = 'attendance.db'
#
# # SQLite connection banayenge
# conn = sqlite3.connect(db_file)
# cursor = conn.cursor()
#
# # Saari tables ka naam fetch karna
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
#
# print("Tables in the database:")
# for table in tables:
#     print(f"\n--- Data from table: {table[0]} ---")
#     cursor.execute(f"SELECT * FROM {table[0]}")
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)
#
# # Connection close karna
# conn.close()
