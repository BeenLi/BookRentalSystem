from tkinter import *
from main import Mysql_db
import db_info


if __name__ == '__main__':
    row, column = 0, 0
    with Mysql_db(**db_info.db_connect) as db:
        sql = "SELECT * from book_item"
        book_item = db.search(sql)
        row = len(book_item)
        column = len(book_item[0])
        print(row, column)
    for i in range(row):
        for j in range(column):
            e = Entry(relief=GROOVE)
            e.grid(row=i, column=j, sticky=NSEW)    # NSEW='nsew'
            e.insert(END, '%s' % (book_item[i][j]))

    mainloop()