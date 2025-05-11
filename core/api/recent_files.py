import os.path
import sqlite3

from core.utils import DATABASE_MANAGER
from models.recent_file import FileModel


def API_fetchRecentFiles() -> tuple[bool, list[FileModel] | None, Exception | None]:
    """
    fetches all date accessed in descending order. Newest first
    :return:
    """
    def task(con: sqlite3.Connection, ):
        cur = con.cursor()
        cur.execute("SELECT * FROM RECENT_FILES")

        entries = cur.fetchall()

        models = []
        invalid: list[str] = []
        for row in entries:
            if not os.path.exists(row[0]):
                invalid.append(row[0])
                continue
            model = FileModel({
                "path": row[0],
                "date_accessed": float(row[1]),
            })
            models.append(model)
        sorted_models = sorted(models, key=lambda m: m.opts()["date_accessed"], reverse=True)

        # drop all invalid paths from the db
        for path in invalid:
            cur.execute("DELETE FROM RECENT_FILES WHERE path=?", (path,))

        return sorted_models

    return DATABASE_MANAGER.execute(task)


def API_clearRecentFiles() -> tuple[bool, None, Exception | None]:
    """
    removes all recent files from the database
    :return:
    """

    def task(con: sqlite3.Connection, ):

        cur = con.cursor()
        cur.execute("DELETE FROM RECENT_FILES")
        return None

    return DATABASE_MANAGER.execute(task)

def API_removeTargetRecentFile(path: str) -> tuple[bool, None, Exception | None]:
    """
    removes the target recent file
    :param path:
    :return:
    """
    def task(con: sqlite3.Connection, _path: str):
        cur = con.cursor()
        cur.execute("DELETE FROM RECENT_FILES WHERE path is ?", (_path))

    return DATABASE_MANAGER.execute(task, _path=path)


def API_addRecentFile(model: FileModel) -> tuple[bool, None, Exception | None]:
    """
    adds the recent file to the database
    :param model:
    :return:
    """
    def task(con: sqlite3.Connection, _path: str, _date_accessed: str):
        cur = con.cursor()
        cur.execute("INSERT INTO RECENT_FILES (path, date_accessed) VALUES (?, ?)", (_path, _date_accessed))

    return DATABASE_MANAGER.execute(task, _path=model.path(), _date_accessed=model.dateAccessed(formatted=False))


def API_updateRecentFile(model: FileModel) -> tuple[bool, None, Exception | None]:
    """"""
    def task(con: sqlite3.Connection, _path: str, _date_accessed: str):
        cur = con.cursor()
        cur.execute("UPDATE RECENT_FILES SET date_accessed=? WHERE path is ? ", (_date_accessed, _path))
        return None

    return DATABASE_MANAGER.execute(task, _path=model.path(), _date_accessed=str(model.dateAccessed(formatted=False)))
