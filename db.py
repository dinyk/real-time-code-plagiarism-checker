"""SQLite helpers for storing reference code snippets."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, List

from algorithms.rabin_karp import ReferenceCode


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "database" / "references.sqlite3"


SAMPLE_REFERENCES = [
    ReferenceCode(
        id=None,
        filename="python_binary_search.py",
        language="Python",
        code="""def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
""",
    ),
    ReferenceCode(
        id=None,
        filename="cpp_factorial.cpp",
        language="C++",
        code="""#include <iostream>
using namespace std;

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
""",
    ),
    ReferenceCode(
        id=None,
        filename="java_palindrome.java",
        language="Java",
        code="""public static boolean isPalindrome(String text) {
    int left = 0;
    int right = text.length() - 1;
    while (left < right) {
        if (text.charAt(left) != text.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
""",
    ),
]


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(seed: bool = True) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reference_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                language TEXT NOT NULL,
                code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM reference_codes").fetchone()[0]
        if seed and count == 0:
            add_reference_codes(SAMPLE_REFERENCES, connection=connection)


def add_reference_code(filename: str, language: str, code: str) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO reference_codes (filename, language, code) VALUES (?, ?, ?)",
            (filename, language, code),
        )
        return int(cursor.lastrowid)


def add_reference_codes(references: Iterable[ReferenceCode], connection: sqlite3.Connection | None = None) -> None:
    owns_connection = connection is None
    connection = connection or get_connection()
    try:
        connection.executemany(
            "INSERT INTO reference_codes (filename, language, code) VALUES (?, ?, ?)",
            [(ref.filename, ref.language, ref.code) for ref in references],
        )
        if owns_connection:
            connection.commit()
    finally:
        if owns_connection:
            connection.close()


def list_reference_codes() -> List[ReferenceCode]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, filename, language, code FROM reference_codes ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return [ReferenceCode(id=row["id"], filename=row["filename"], language=row["language"], code=row["code"]) for row in rows]


def delete_reference_code(reference_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM reference_codes WHERE id = ?", (reference_id,))
        return cursor.rowcount > 0
