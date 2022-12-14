from time import sleep
from threading import Thread

from sqlalchemy.orm import sessionmaker

from db import transaction

import os
import sys

def process1():
    with transaction() as tran:
        tran.execute('UPDATE users SET balance = balance + 10 WHERE id = 3;')
        sleep(1)
        tran.execute('UPDATE users SET balance = balance + 10 WHERE id = 1 RETURNING pg_sleep(1);')

def process2():
    with transaction() as tran:
        tran.execute('UPDATE users SET balance = balance + 10 WHERE id = 1;')
        sleep(1)
        tran.execute('UPDATE users SET balance = balance + 10 WHERE id = 3 RETURNING pg_sleep(1);')

if __name__ == '__main__':
    print("Starting lock transactions")
    p1 = Thread(target=process1)
    p2 = Thread(target=process2)
    p1.start()
    p2.start()
    sleep(4)
    print("Exit")
    os.execv(sys.executable, [sys.executable, __file__] + sys.argv)