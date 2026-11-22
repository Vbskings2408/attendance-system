"""Extract reference vectors with a pretrained model."""
import json
import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile

import face_recognition as fr

from common import CACHE, FACES


def encode():
    records = []
    for folder in sorted(FACES.glob("student_*")):
        student = json.loads((folder / "student.json").read_text(encoding="utf-8"))
        for photo in sorted(folder.glob("*.jpg")):
            image = fr.load_image_file(str(photo))
            vectors = fr.face_encodings(image)
            if len(vectors) == 1:
                records.append((student["Name"], student["ID"], vectors[0]))
            else:
                print(f"Skipped {photo.name} in {folder.name}: expected exactly one face.")
    # Write even an empty list so removed students disappear from the cache.
    with NamedTemporaryFile(dir=CACHE.parent, delete=False) as stream:
        temporary = Path(stream.name)
        pickle.dump(records, stream)
    temporary.replace(CACHE)
    if not records:
        raise ValueError("No usable photos in known_faces. Register a student first.")
    print(f"Cached {len(records)} face encodings.")


if __name__ == "__main__":
    try:
        encode()
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(str(error))
