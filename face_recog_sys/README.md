# Facial Recognition Attendance System

The **Facial Recognition Attendance System** is a Python-based application that allows you to mark attendance using facial recognition technology. This system uses your webcam to identify registered faces, marking users as "IN" and "OUT" based on their attendance times. It stores the records in an SQLite database, allowing easy viewing and management of attendance data through a simple Tkinter-based GUI.

---

## 🚀 Features

* **Face Registration**: Register a user’s face by capturing it via the webcam.
* **Face Recognition**: Recognizes faces and marks attendance automatically.
* **Attendance Tracking**: Tracks "IN" and "OUT" times, and calculates session durations.
* **Database Management**: Uses SQLite to store face encodings and session records.
* **View Attendance**: A GUI option to view all attendance records and total hours worked per user.
* **Delete User**: Remove a registered user from the system.
* **Login System**: Simple admin login to access the main functionalities.
* **Real-Time Notifications**: Displays real-time notifications about marked "IN" and "OUT" times.

---

## 📦 Setup

### 1. Install Dependencies

First, make sure you have Python 3.x installed on your machine.

Then, install the required dependencies using the following command in your terminal:

```bash
pip install click==8.1.8 colorama==0.4.6 dlib==19.24.0 face-recognition==1.3.0 face-recognition-models==0.3.0 numpy==1.26.4 opencv-python==4.5.3.56 pillow==11.2.1 pip==25.1.1 setuptools==80.9.0 wheel==0.46.1
```

This will install all necessary libraries that the project requires to run properly.

> **Note**: Make sure the versions of these libraries are exactly as specified. The project may not work properly with different versions.

### 2. Create a Virtual Environment (Optional but Recommended)

To avoid conflicts with other Python projects, it’s a good idea to create a virtual environment. Simply use Pycharm IDE.

Once activated, you can install the dependencies as mentioned earlier.

---

## 🛠 Usage

### 1. Run the Application

After installing the dependencies, you can start the application by running the `main.py` script:


This will open the login window for authentication.

### 2. Admin Login

When the login window appears, use the following credentials to log in as an admin:

* **Username**: `admin`
* **Password**: `pass`

> ⚠️ You can change the login credentials in the `main.py` file if needed.

### 3. Register a User’s Face

* Go to the **Register Face** section in the app.
* Enter the name of the user you want to register.
* The system will use your webcam to capture the user’s face.
* Press `s` to save the face and `q` to quit if needed.

### 4. Recognize Faces and Mark Attendance

* Go to the **Recognize & Mark Attendance** section in the app.
* The system will use face recognition to mark users as "IN" or "OUT".
* It will automatically track the attendance for each user.

### 5. View Attendance Records

* Go to the **Show Attendance Records** section to view all users’ attendance data, including:

  * Name
  * Date
  * IN Time
  * OUT Time
  * Session Duration
  * Total Hours Per Day

### 6. Delete a User

* Go to the **Delete User** section.
* Select the user you wish to delete.
* The user’s face image and associated database records will be deleted.

---

## 🔧 Development Notes

* **Database**: The project uses an SQLite database (`attendance.db`) to store face encodings and session records.
* **Face Detection**: The system uses the `face-recognition` library for detecting and encoding faces.
* **GUI**: The user interface is built using the `Tkinter` library, allowing for easy interaction with the application.
* **Beep Notification**: When attendance is marked, the system will play a beep sound (Windows-specific via `winsound`).

---

## 💻 Requirements

Before running the application, make sure your system meets the following requirements:

* Python 3.x
* A webcam connected to your system
* The following Python libraries installed:

  * **click==8.1.8**
  * **colorama==0.4.6**
  * **dlib==19.24.0**
  * **face-recognition==1.3.0**
  * **face-recognition-models==0.3.0**
  * **numpy==1.26.4**
  * **opencv-python==4.5.3.56**
  * **pillow==11.2.1**
  * **pip==25.1.1**
  * **setuptools==80.9.0**
  * **wheel==0.46.1**
* **Windows-specific**: `winsound` for beep notifications (you can modify this section for other platforms if needed).

---

## 🔍 Inspect Database (Optional)

If you want to view the contents of the database, you can use the `read_db.py` script to print the entries from the `faces` and `sessions` tables.

This will display the face data and session logs from the SQLite database in the terminal.
