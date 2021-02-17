import tkinter as tk
from tkinter import ttk
from main import Mysql_db
import db_info

if __name__ == '__main__':
    root = tk.Tk()
    # 表格的头部
    tree = ttk.Treeview(root, column=("ISBN", "书名", "价格", "库存"), show='headings')
    tree.tag_configure('ttk', background="yellow")
    tree.column("ISBN", anchor=tk.CENTER)
    tree.heading("ISBN", text="ISBN")
    tree.column("书名", anchor=tk.CENTER)
    tree.heading("书名", text="书名")
    tree.column("价格", anchor=tk.CENTER)
    tree.heading("价格", text="价格")
    tree.column("库存", anchor=tk.CENTER)
    tree.heading("库存", text="库存")

    # 向表格添加数据
    # tree.insert("", "end", values=("9787533936020", "月亮与六便士", "39.80", "2"), tags='ttk')
    with Mysql_db(**db_info.db_connect) as db:
        sql = "SELECT * from book_item"
        book_item = db.search(sql)
        row = len(book_item)
        column = len(book_item[0])
    for index in range(row):
        print(book_item[index])
        tree.insert("", "end", values=book_item[index])
    tree.pack()
    button = tk.Button(text="检索", command="Show_data")
    button.pack(pady=10)

    root.mainloop()