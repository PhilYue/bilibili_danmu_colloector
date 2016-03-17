import asyncio
import sqlite3
import threading
import time
import copy

class CommentsRecorder(threading.Thread):
    def __init__(self, lock, commentq, numq):
        threading.Thread.__init__(self)
        self.lock = lock
        self.commentq = commentq
        self.numq = numq

        self.cx = sqlite3.connect('bilbili.db', check_same_thread = False)
        self.cu = self.cx.cursor()

    def run(self):

        while True:
            time.sleep(10)
            print ()
            print ('begin to write db')

            if self.lock.acquire():
                nums = copy.deepcopy(self.numq)
                print (len(nums))
                self.numq.clear()
                self.lock.release()
                for num in nums:
                    table = 'ss' + str(num[0])
                    self.cu.execute("insert into %s (number, time) values (?, ? )" % table, (num[1], num[2]))
                self.cx.commit()
                print ('record number of people')

            if self.lock.acquire():
                comments = copy.deepcopy(self.commentq)
                print (len(comments))
                self.commentq.clear()
                self.lock.release()
                for comment in comments:
                    table = 'tt' + str(comment[0])

                    self.cu.execute("insert into %s (name, comment, time) values (?, ?, ?)" % table, (comment[1], comment[2], comment[3]))
                self.cx.commit()
                print ('record comments')
            print ()
