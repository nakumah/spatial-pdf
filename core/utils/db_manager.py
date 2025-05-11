import os
from typing import Callable, Optional, Any
import sqlite3

from core.config.settings import DATABASE_FILE
from core.utils.file_readers import readCorpus


class DatabaseManager:

    def __init__(self):
        self.__opts = {
            "db_file": DATABASE_FILE
        }

    def prime(self):
        """
        configures the database
        :return:
        """
        # if db already exists, do not override
        if os.path.exists(self.__opts['db_file']):
            return

        # create the db
        con = sqlite3.connect(self.__opts['db_file'])
        cur = con.cursor()

        # prepare the db
        cur.executescript(readCorpus("structure_db","sql"))
        cur.executescript(readCorpus("prime_db","sql"))

        # close the connection
        con.commit()
        con.close()

    def execute(self, task: Callable[[sqlite3.Connection, Optional[object]], Any], **kwargs) -> tuple[bool, Any, Exception | None]:
        """
        executes a task on the database
        :param task: the function to be called
        :param kwargs: the parameters for the provided function
        :return:
        """

        file: str | None = self.__opts.get('db_file', None)
        if file is None:
            return False, None, ValueError("Can't find database file")

        con = sqlite3.connect(file)

        try:
            res = task(con, **kwargs)
            con.commit()
            con.close()
            return True, res, None
        except Exception as e:
            con.rollback()
            con.close()
            return False, None, e
