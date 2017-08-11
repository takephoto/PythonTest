# -*- coding:utf-8 -*-
# android iOS window
import sqlite3

if __name__ == '__main__':

    userID = 53499286

    iOS_db_path = '/Users/admin/Desktop/db/LKDB.db'
    android_db_path = '/Users/admin/Desktop/db/LKDB.db'
    window_db_path = '/Users/admin/Desktop/db/LKDB.db'

    dbPaths = [iOS_db_path, android_db_path, window_db_path]
    dbNames = ['newRecordThing', 'newRecordThing', 'newRecordThing']
    osNames = ['iOS', 'android', 'window']
    # 三端比较总个数
    # 已

    w_db_path = '/Users/admin/Desktop/db/notedata.db'
    s = sqlite3.connect(w_db_path)
    c = s.cursor()
    c.execute('show tables')
    s.commit()

    every_count = []
    for i in range(0, len(dbPaths)):
        db = sqlite3.connect(dbPaths[i])
        cu = db.cursor()
        cu.execute(
            "select count(*) from %s where userId = %d and recordType != 8 and recordType != 9 and recordType != 10" % (
            dbNames[i], userID))
        db.commit()
        r = cu.fetchone()
        count = r[0]
        every_count.append(count)
        print "%s 同步记事总数: %d" % (osNames[i], count)
        cu.close()
        db.close()

    # 那个端的记事最多
    maxIndex = 0
    maxValue = every_count[0]
    for i in range(0, len(every_count)):
        if i > maxValue:
            maxIndex = i

    sql = ''
    db = sqlite3.connect(dbPaths[maxIndex])
    cu = db.cursor()
    cu.row_factory = sqlite3.Row

    if osNames[maxIndex] == 'iOS':
        sql = 'select * from %s where userId = %d and recordType != 8 and recordType != 9 and recordType != 10' % (
        dbNames[maxIndex], userID)
    else:
        sql = 'select * from %s where userId = %d' % (dbNames[maxIndex], userID)
    cu.execute(sql)
    db.commit()
    for p in cu.fetchall():
        recordId = p['recordId']
        print recordId
        for index in range(0, len(dbPaths)):
            if index == maxIndex:
                break
            sqldb = sqlite3.connect(dbPaths[maxIndex])
            sqlcu = sqldb.cursor()
            sqlcu.execute('select * from %s where userId =%d and recordId = %d', (dbNames[index], userID, recordId))
            sqldb.commit()
            row = sqlcu.fetchone()
            sqlcu.close()
            sqldb.close()
            if not row:
                print '%s 不存在 recordId = %d 记事' % (osNames[index], recordId)
    cu.close()
    db.close()