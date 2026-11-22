"""Paths are relative to the project, even when launched from another folder."""
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FACES = ROOT / "known_faces"
CACHE = ROOT / "encodings.pkl"
LOG = ROOT / "attendance.csv"
COLUMNS = ["Name", "ID", "Date", "Time"]


@contextmanager
def webcam():
    import cv2

    camera = cv2.VideoCapture(0)
    try:
        if not camera.isOpened():
            raise RuntimeError("No webcam found. Check camera permissions and close other camera apps.")
        yield camera
    finally:
        camera.release()
        cv2.destroyAllWindows()


def read_frame(camera):
    ok, frame = camera.read()
    if not ok or frame is None:
        raise RuntimeError("Could not read the webcam frame.")
    return frame
