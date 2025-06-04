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
