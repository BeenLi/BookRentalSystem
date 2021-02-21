# 这段程序可将图标paul.ico转换成icon.py文件里的base64数据
import base64
open_icon = open("reading-book.ico","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = %s" % b64str
f = open("icon.py", encoding='utf8', mode="w+")
f.write(write_data)
f.close()