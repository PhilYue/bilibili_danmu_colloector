import asyncio
import sqlite3
import threading
import time
import copy

class CommentsRecorder(threading.Thread):
    def __init__(self, lock, commentq):
        threading.Thread.__init__(self)
        self.lock = lock
        self.commentq = commentq
        self.cx = sqlite3.connect('bilbili.db', check_same_thread = False)
        self.cu = self.cx.cursor()

    def run(self):

        while True:
            time.sleep(10)
            if len(self.commentq) == 0:
                continue
            if self.lock.acquire():
                comments = copy.deepcopy(self.commentq)
                print (len(comments))
                self.commentq.clear()
                self.lock.release()
                print (comments[0])
                for comment in comments:
                    table = 'tt' + str(comment[0])

                    self.cu.execute("insert into %s (name, comment, time) values (?, ?, ?)" % table, (comment[1], comment[2], comment[3]))
                self.cx.commit()
                print ('插入成功')
