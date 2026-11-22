"""Recognize faces and record the first sighting of each student per day."""
import csv
import pickle
from datetime import datetime

import cv2
import face_recognition as fr
import numpy as np

from common import CACHE, COLUMNS, LOG, read_frame, webcam


def load_seen():
    if not LOG.exists():
        with LOG.open("x", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(COLUMNS)
    with LOG.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != COLUMNS:
            raise ValueError("Unexpected attendance.csv header.")
        return {(row["ID"], row["Date"]) for row in reader}


def mark(name, student_id, seen):
    now = datetime.now()
    date = now.date().isoformat()
    key = (student_id, date)
    if key in seen:
        return
    with LOG.open("a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([name, student_id, date, now.strftime("%H:%M:%S")])
    seen.add(key)
    print(f"Present: {name} ({student_id})")


def recognize(frame, records, vectors, seen):
    small = cv2.resize(frame, None, fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    boxes = fr.face_locations(rgb)
    results = []
    for box, vector in zip(boxes, fr.face_encodings(rgb, boxes)):
        distances = fr.face_distance(vectors, vector)
        best = int(np.argmin(distances))
        label = "Unknown"
        if distances[best] <= 0.50:
            label, student_id, _ = records[best]
            mark(label, student_id, seen)
        results.append((box, label))
    return results


def run():
    if not CACHE.exists():
        raise ValueError("Run encode_faces.py first.")
    # Only load the local pickle created by encode_faces.py.
    with CACHE.open("rb") as file:
        records = pickle.load(file)
    if not records:
        raise ValueError("Empty face cache. Register and encode first.")
    vectors = np.array([record[2] for record in records])
    seen = load_seen()
    process = True
    with webcam() as camera:
        while True:
            frame = read_frame(camera)
            if process:
                results = recognize(frame, records, vectors, seen)
            process = not process
            # Reuse the previous boxes on skipped frames. Scale coordinates back up.
            for box, label in results:
                top, right, bottom, left = [value * 4 for value in box]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 220, 0), 2)
                cv2.putText(frame, label, (left, max(20, top - 6)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 220, 0), 2)
            cv2.imshow("Attendance | q to quit", frame)
            if cv2.waitKey(1) & 255 == ord("q"):
                break


if __name__ == "__main__":
    try:
        run()
    except (OSError, RuntimeError, ValueError, EOFError, pickle.UnpicklingError) as error:
        raise SystemExit(str(error))
