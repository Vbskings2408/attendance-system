"""Display today's attendance, preserving leading zeroes in IDs."""
from datetime import date

import pandas as pd

from common import COLUMNS, LOG


def report():
    today = date.today().isoformat()
    rows = pd.read_csv(LOG, dtype=str, keep_default_na=False) if LOG.exists() else pd.DataFrame(columns=COLUMNS)
    if list(rows.columns) != COLUMNS:
        raise ValueError("Unexpected attendance.csv header.")
    present = rows.loc[rows["Date"] == today].drop_duplicates("ID")
    print(f"Attendance for {today}")
    if not present.empty:
        print(present[["Name", "ID", "Time"]].to_string(index=False))
    print(f"Total present: {len(present)}")


if __name__ == "__main__":
    try:
        report()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error))
