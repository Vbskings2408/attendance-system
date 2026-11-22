# Face Recognition Attendance System

A local webcam project for a first-semester CSE demonstration. Register five photos per student, turn them into reference vectors, recognize registered students on camera, and print a daily report. Each student ID gets one row per local calendar day.

## Install

Use 64-bit Python 3.10 or newer. Python 3.10 is a practical starting point for this older face_recognition package. Use a desktop terminal with camera access.

**Windows:** Install Visual Studio Build Tools with **Desktop development with C++**, the MSVC x64 compiler and a Windows SDK. Install CMake and select the installer option to add CMake to PATH. Open a new **x64 Native Tools Command Prompt** and run:

```bat
cmake --version
cl
py -3.10 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install dlib
python -m pip install -r requirements.txt
```

If CMake cannot find the compiler, check that both commands above resolve in the same prompt as pip. If native Windows installation still fails, use the Linux setup on a machine with a working webcam. Upstream describes Windows support as unofficial.

**Linux (Debian, Ubuntu or Kali):**

```bash
sudo apt install build-essential cmake python3-dev python3-venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

References: [dlib build guide](https://dlib.net/compile.html) and [face_recognition installation notes](https://github.com/ageitgey/face_recognition#installation).

## Run in order

1. Run `python register.py`. Enter a name and unique ID. Look at the camera and press Space five times, changing your angle slightly each time. Exactly one face must be visible. Press q in the camera window to cancel. Repeat for other students.
2. Run `python encode_faces.py`. It reads known_faces/student_ID/1.jpg through 5.jpg and student.json, then writes encodings.pkl. Repeat after changing registrations.
3. Run `python attendance.py`. Keep one attendance process running at a time. The first recognized sighting writes Name,ID,Date,Time to attendance.csv. Unknown faces get a label only. Press q in the camera window to quit.
4. Run `python report.py` to print today's names, IDs, first attendance times, and total.

common.py contains the shared paths and camera cleanup. Detection uses quarter-size frames every other frame. The nearest reference encoding must have a distance of 0.50 or less to count as a match.

## Example output

```text
Cached 5 face encodings.
Present: Asha (001)

Attendance for 2026-11-22
Name  ID     Time
Asha 001 09:15:02
Total present: 1
```

Screenshot placeholder: Insert a webcam preview from a consenting volunteer here.

## Privacy and limitations

Get permission before registering anyone. Images, biometric vectors, and attendance records stay on this computer. Keep them out of GitHub. Only open pickle files you generated locally. To withdraw a registration, delete the student's folder and rerun the encoder before restarting attendance. Existing CSV records are separate. Lighting can cause missed or mistaken matches, and a photograph can fool this demo. Review the CSV before using it for a class record.

## Future improvements

Add liveness detection, an Excel export, or a Streamlit dashboard for daily totals.
