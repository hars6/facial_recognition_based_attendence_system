import cv2
import face_recognition
import os
import numpy as np
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter import ttk
import winsound
import platform



# ========== DATABASE SETUP ==========

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                encoding BLOB NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                in_time TEXT NOT NULL,
                out_time TEXT)''')

    conn.commit()
    conn.close()


# ========== FACE ENCODING SETUP ==========

def load_known_faces():
    known_encodings = []
    known_names = []

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT name, encoding FROM faces")
    rows = c.fetchall()

    for row in rows:
        name, encoding = row
        known_names.append(name)
        known_encodings.append(np.frombuffer(encoding, dtype=np.float64))

    conn.close()
    return known_encodings, known_names


# ========== FACE REGISTRATION ==========

def register_face(name):
    if not os.path.exists("faces"):
        os.makedirs("faces")

    cap = cv2.VideoCapture(0)
    print("[*] Capturing face. Look at the camera...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Register Face - Press 's' to Save, 'q' to Quit", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            img_path = os.path.join("faces", f"{name}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"[✓] Face saved as {img_path}")
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    image = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        messagebox.showerror("Error", "No face detected. Try again.")
        return
    encoding = encodings[0]

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)", (name, encoding.tobytes()))
    conn.commit()
    conn.close()




def recognize_faces():
    known_encodings, known_names = load_known_faces()
    if not known_encodings:
        print("[x] No registered faces found. Register first!")
        return

    recently_marked_out = {}
    message_to_show = None
    message_time = None

    cap = cv2.VideoCapture(0)
    window_name = 'Attendance Recognition'
    print("[*] Starting face recognition. Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        now = datetime.now()

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            name = "Unknown"

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

                date_str = now.strftime("%Y-%m-%d")
                current_time = now.strftime("%H:%M:%S")

                conn = sqlite3.connect('attendance.db')
                c = conn.cursor()

                # Cooldown check
                if name in recently_marked_out:
                    time_since_out = (now - recently_marked_out[name]).total_seconds()
                    if time_since_out < 10:
                        conn.close()
                        continue
                    else:
                        del recently_marked_out[name]

                # Check if an active session exists
                c.execute("SELECT id, in_time FROM sessions WHERE name=? AND date=? AND out_time IS NULL", (name, date_str))
                session = c.fetchone()

                if session:
                    session_id, in_time_str = session
                    in_datetime = datetime.strptime(date_str + " " + in_time_str, "%Y-%m-%d %H:%M:%S")
                    seconds_passed = (now - in_datetime).total_seconds()

                    if seconds_passed >= 30:
                        c.execute("UPDATE sessions SET out_time=? WHERE id=?", (current_time, session_id))
                        print(f"[✓] Marked OUT for {name} at {current_time}")
                        recently_marked_out[name] = now
                        message_to_show = f"{name} OUT at {current_time}"
                        message_time = datetime.now()
                        play_beep()
                else:
                    c.execute("INSERT INTO sessions (name, date, in_time) VALUES (?, ?, ?)", (name, date_str, current_time))
                    print(f"[✓] Marked IN for {name} at {current_time}")
                    message_to_show = f"{name} IN at {current_time}"
                    message_time = datetime.now()
                    play_beep()

                conn.commit()
                conn.close()

            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (0, 0, 0), 2)

        # Show message if available
        if message_to_show and (datetime.now() - message_time).total_seconds() < 3:
            cv2.rectangle(frame, (10, 10), (400, 80), (50, 205, 50), -1)  # green box
            cv2.putText(frame, message_to_show, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

        cv2.imshow(window_name, frame)

        # === Updated breaking condition ===
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()




def play_beep():
    if platform.system() == "Windows":
        winsound.Beep(1000, 200)  # frequency 1000Hz, duration 200ms




# ========== GUI SETUP (Tkinter) ==========

def authenticate_user():
    username = username_entry.get()
    password = password_entry.get()

    authorized_users = {
        "admin": "pass",
    }

    if username in authorized_users and authorized_users[username] == password:
        login_window.destroy()
        main_gui()
    else:
        messagebox.showerror("Authentication Failed", "Invalid username or password!")


def login_gui():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Login - Attendance System")

    window_width = 300
    window_height = 250
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(login_window, text="Username:").pack(pady=10)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=10)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=authenticate_user)
    login_button.pack(pady=20)

    login_window.mainloop()


def register_face_gui():
    name = name_entry.get()
    if name:
        status_label.config(text=f"Registering {name}'s face. Please wait...")
        register_face(name)
        status_label.config(text=f"{name}'s face registered successfully!")
        messagebox.showinfo("Success", f"Face for {name} registered successfully!")
    else:
        messagebox.showwarning("Input Error", "Please enter a name.")


def recognize_faces_gui():
    status_label.config(text="Recognizing faces... Please wait...")
    recognize_faces()
    status_label.config(text="Face recognition completed!")


def show_attendance():
    attendance_window = Toplevel(window)
    attendance_window.title("Attendance Records")

    tree = ttk.Treeview(attendance_window,
                        columns=("Name", "Date", "IN Time", "OUT Time", "Session Duration", "Total Hours Per Day"),
                        show="headings")
    tree.pack(pady=20, padx=20)

    tree.heading("Name", text="Name")
    tree.heading("Date", text="Date")
    tree.heading("IN Time", text="IN Time")
    tree.heading("OUT Time", text="OUT Time")
    tree.heading("Session Duration", text="Session Duration")
    tree.heading("Total Hours Per Day", text="Total Hours Per Day")

    tree.column("Name", width=100, anchor="center")
    tree.column("Date", width=100, anchor="center")
    tree.column("IN Time", width=80, anchor="center")
    tree.column("OUT Time", width=80, anchor="center")
    tree.column("Session Duration", width=120, anchor="center")
    tree.column("Total Hours Per Day", width=150, anchor="center")

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT name, date, in_time, out_time FROM sessions ORDER BY date ASC, in_time ASC")
    rows = c.fetchall()
    conn.close()

    cumulative_time = {}
    processed_rows = []

    for row in rows:
        name, date, in_time, out_time = row
        session_duration = "-"
        total_hours_day = "-"

        key = (name, date)
        if out_time:
            in_dt = datetime.strptime(f"{date} {in_time}", "%Y-%m-%d %H:%M:%S")
            out_dt = datetime.strptime(f"{date} {out_time}", "%Y-%m-%d %H:%M:%S")
            session_seconds = (out_dt - in_dt).total_seconds()

            hours = int(session_seconds // 3600)
            minutes = int((session_seconds % 3600) // 60)
            seconds = int(session_seconds % 60)
            session_duration = f"{hours}h {minutes}m {seconds}s"

            if key in cumulative_time:
                cumulative_time[key] += session_seconds
            else:
                cumulative_time[key] = session_seconds

            total_sec_day = cumulative_time[key]
            hours_d = int(total_sec_day // 3600)
            minutes_d = int((total_sec_day % 3600) // 60)
            seconds_d = int(total_sec_day % 60)
            total_hours_day = f"{hours_d}h {minutes_d}m {seconds_d}s"

        processed_rows.append((name, date, in_time, out_time if out_time else "-", session_duration, total_hours_day))

    processed_rows.reverse()

    for record in processed_rows:
        tree.insert("", "end", values=record)


def delete_user_gui():
    def delete_selected_user():
        selected_name = user_name_combobox.get().strip()
        if not selected_name:
            messagebox.showwarning("Input Error", "Please select a user name to delete.")
            return

        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()

        c.execute("SELECT * FROM faces WHERE name=?", (selected_name,))
        result = c.fetchone()

        if result:
            c.execute("DELETE FROM faces WHERE name=?", (selected_name,))
            conn.commit()
            conn.close()

            face_img_path = os.path.join("faces", f"{selected_name}.jpg")
            if os.path.exists(face_img_path):
                os.remove(face_img_path)

            messagebox.showinfo("Deleted", f"User '{selected_name}' deleted successfully!")
            refresh_user_list()
        else:
            conn.close()
            messagebox.showerror("User Not Found", f"No user named '{selected_name}' exists!")

    def refresh_user_list():
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute("SELECT name FROM faces")
        names = [row[0] for row in c.fetchall()]
        conn.close()

        user_name_combobox['values'] = names
        if names:
            user_name_combobox.current(0)
        else:
            user_name_combobox.set('')

    delete_window = Toplevel(window)
    delete_window.title("Delete User")

    tk.Label(delete_window, text="Select User to Delete:").pack(pady=10)

    user_name_combobox = ttk.Combobox(delete_window, width=30, state="readonly")
    user_name_combobox.pack(pady=5)

    tk.Button(delete_window, text="Delete User", command=delete_selected_user, bg="red", fg="white").pack(pady=20)

    refresh_user_list()


def main_gui():
    global window, name_entry, status_label

    init_db()

    window = tk.Tk()
    window.title("Facial Recognition Attendance System")

    window_width = 400
    window_height = 500
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    welcome_label = tk.Label(window, text="Welcome to Attendance System", font=("Arial", 16))
    welcome_label.pack(pady=10)

    tk.Label(window, text="Enter Name for Registration:").pack(pady=10)
    name_entry = tk.Entry(window, width=30)
    name_entry.pack(pady=5)

    tk.Button(window, text="Register Face", command=register_face_gui, bg="lightgreen", width=25).pack(pady=10)
    tk.Button(window, text="Recognize & Mark Attendance", command=recognize_faces_gui, bg="lightblue", width=25).pack(
        pady=10)
    tk.Button(window, text="Show Attendance Records", command=show_attendance, bg="lightyellow", width=25).pack(pady=10)
    tk.Button(window, text="Delete User", command=delete_user_gui, bg="red", fg="white", width=25).pack(pady=10)

    status_label = tk.Label(window, text="", font=("Arial", 12), fg="green")
    status_label.pack(pady=20)

    window.mainloop()


# ========== START APPLICATION ==========

if __name__ == '__main__':
    login_gui()
