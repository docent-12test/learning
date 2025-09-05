"""
FILE_INFORMATION=Fluvius;Arvid Claassen;Some python code
"""
import os
import sqlite3
import stat
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, Union

from filesystem import file_hash
from sqlite import create_table, datetime_to_sqlite


TABLE_DEF = """
    path TEXT PRIMARY KEY,
    mtime TEXT NOT NULL,
    fsize INTEGER NOT NULL,
    perms TEXT NOT NULL,
    info TEXT NOT NULL
"""


def normalize_path(p: str) -> str:
    return os.path.abspath(os.path.normpath(p))

@dataclass
class Fact:
    mtime: str
    fsize: int
    perms: str
    info: str

def get_file_facts(path: str) -> Fact:
    """
    Bepaal (sha256, mtime_sqlite, perms_octal) voor het bestand.
    - sha256: hex-string van de inhoud
    - mtime_sqlite: datum/tijd in sqlite-formaat
    - perms_octal: permissies als octale string, bv. '0644' (Windows geeft mogelijk beperkte info)
    """
    st = os.stat(path)
    mtime = datetime.fromtimestamp(st.st_mtime)
    fsize = str(st.st_size)
    mtime_sqlite = datetime_to_sqlite(mtime)
    perms_octal = f"{stat.S_IMODE(st.st_mode):04o}"
    return Fact(mtime=mtime_sqlite, fsize=fsize, perms=perms_octal, info="")







class FileScanner:

    def __init__(self, root: str, db_path: str, table: str = "files") -> None:
        self.root = normalize_path(root)
        self.db_path = db_path
        self.conn = None
        self.table_new = table+"_NEW"
        self.table_old = table+"_OLD"
        self.ensure_tables()

    def ensure_tables(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        ok, err = create_table(self.conn, self.table_old, TABLE_DEF, drop=True, create_if_exists=True)
        print(f"Table {self.table_old} created: {ok}, error: {err}")
        ok, err = create_table(self.conn, self.table_new, TABLE_DEF, drop=False, create_if_exists=True)
        print(f"Table {self.table_new} created: {ok}, error: {err}")
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO {self.table_old} SELECT * FROM {self.table_new}")
        cur.execute(f"DELETE FROM {self.table_new}")
        if not ok:
            raise RuntimeError(f"Kon de tabel niet aanmaken of openen: {err}")

    def scan(self):
        """
        Doorloop root, filter tekstbestanden met een 'FILE_information'-regel, vergelijk met SQLite.
        Print een rapport en geeft het aantal afwijkingen terug.
        """
        processed = 0
        try:

            for dirpath, _, filenames in os.walk(self.root):
                for name in filenames:
                    path = normalize_path(os.path.join(dirpath, name))
                    processed += 1
                    current = get_file_facts(path)
                    if processed % 1000 == 0:
                        print(f"Processed {processed} files...")
                    self.insert_record(path, current)

        finally:
            self.conn.close()
        print(f"Processed {processed} files.")

    def insert_record(self, path: str, fact: Fact) -> None:
        cur = self.conn.cursor()
        cur.execute(
            f"""
            INSERT INTO {self.table_new} (path, mtime, fsize, perms, info)
            VALUES (?, ?, ?, ?, ?)
            """,
            (path, fact.mtime, fact.fsize, fact.perms, fact.info),
        )
        self.conn.commit()


if __name__ == "__main__":
    FileScanner("c:\\windows", "d:\\f1", "files").scan()

