import sqlite3
import asyncio
from bilibiliClient import bilibiliClient

class taskcreator():
    def __init__(self, lock, commentq):
        self.lock = lock
        self.commentq = commentq
        cx = sqlite3.connect('bilbili.db', check_same_thread = False)
        #cu = cx.cursor()
        rooms = cx.execute('select * from rooms')
        self.urls = []
        for room in rooms:
            self.urls.append(room[1])
        cx.close()

    async def creating(self):
        for url in self.urls:
            danmuji = bilibiliClient(url, self.lock, self.commentq)
            asyncio.ensure_future(danmuji.connectServer())
            asyncio.ensure_future(danmuji.HeartbeatLoop())
            await asyncio.sleep(0.2)
