"""Register one student. SPACE captures a photo and q cancels."""
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import cv2
import face_recognition as fr

from common import FACES, read_frame, webcam


def register(name, student_id):
    if not name or not re.fullmatch(r"[A-Za-z0-9_-]+", student_id):
        raise ValueError("Enter a name and an ID containing letters, digits, underscores or hyphens.")
    FACES.mkdir(exist_ok=True)
    destination = FACES / ("student_" + student_id)
    if destination.exists():
        raise ValueError("That ID is already registered.")
    # Publish the folder only after all five pictures are ready.
    with TemporaryDirectory(dir=FACES, prefix=".capture-") as temp, webcam() as camera:
        folder = Path(temp) / "photos"
        folder.mkdir()
        count = 0
        while count < 5:
            frame = read_frame(camera)
            preview = frame.copy()
            cv2.putText(preview, f"{count}/5 | SPACE: capture | q: cancel", (12, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Register", preview)
            key = cv2.waitKey(1) & 255
            if key == ord("q"):
                print("Registration cancelled.")
                return
            if key == ord(" "):
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if len(fr.face_locations(rgb)) != 1:
                    print("Capture skipped. Show exactly one face and try again.")
                    continue
                if not cv2.imwrite(str(folder / f"{count + 1}.jpg"), frame):
                    raise OSError("Could not save the photo.")
                count += 1
        (folder / "student.json").write_text(json.dumps({"Name": name, "ID": student_id}), encoding="utf-8")
        folder.rename(destination)
    print("Saved five photos. Run encode_faces.py next.")


if __name__ == "__main__":
    try:
        register(input("Student name: ").strip(), input("Student ID: ").strip())
    except (OSError, RuntimeError, ValueError) as error:
        raise SystemExit(str(error))
