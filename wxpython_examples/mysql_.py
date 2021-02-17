import wx
import MySQLdb

db=MySQLdb.connect("localhost", "root", "WANli550296815", "grocery")
cursor = db.cursor()

class MyFrame(wx.Frame):

    def __init__(self, parent, id, title):

        wx.Frame.__init__(self, parent, id, title)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('light gray')
        iconFile = "Grocery.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
        label1 = wx.StaticText(panel, -1, "Product:")
        label2 = wx.StaticText(panel, -1, "Price:")
        label3 = wx.StaticText(panel, -1, "Store:")
        label4 = wx.StaticText(panel, -1, "Brand:")
        label5 = wx.StaticText(panel, -1, "Description:")
        self.Product = wx.TextCtrl(panel, -1, "")
        self.Price = wx.TextCtrl(panel, -1, "")
        self.Store = wx.TextCtrl(panel, -1, "")
        self.Brand = wx.TextCtrl(panel, -1, "")
        self.Description = wx.TextCtrl(panel, -1, "")
        self.calc_btn = wx.Button(panel, -1, 'Save')
        self.calc_btn.Bind(wx.EVT_BUTTON, self.onEnter)
        self.close = wx.Button(panel, -1, "Exit")
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        
        # use gridbagsizer for layout of widgets
        sizer = wx.GridBagSizer(vgap=5, hgap=5)
        sizer.Add(label1, pos=(0, 0))
        sizer.Add(self.Product, pos=(0, 2))  # row 0, column 2
        sizer.Add(label2, pos=(1, 0))
        sizer.Add(self.Price, pos=(1, 2))
        sizer.Add(label3, pos=(2, 0))
        sizer.Add(self.Store, pos=(2, 2))
        sizer.Add(label4, pos=(3, 0))
        sizer.Add(self.Brand, pos=(3, 2))
        sizer.Add(label5, pos=(4, 0))
        sizer.Add(self.Description, pos=(4, 2))
        sizer.Add(self.calc_btn, pos=(6, 1))
        sizer.Add(self.close, pos=(6, 2))
        
        # use boxsizer to add border around sizer
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        panel.SetSizerAndFit(border)
        self.Fit()
        
    def onEnter(self, event):
        # get the values from the input widgets
        Product = str(self.Product.GetValue())
        Price = float(self.Price.GetValue())
        Store = str(self.Store.GetValue())
        Brand = str(self.Brand.GetValue())
        Description = str(self.Description.GetValue())
        db=MySQLdb.connect("localhost", "root", "kanga112", "grocery")
        cursor = db.cursor()
        cursor.execute("INSERT INTO prices (Product, Price, Store, Brand, Description) VALUES (%s, %s, %s, %s, %s)", (Product, Price, Store, Brand, Description))
        cursor.execute("commit")

        self.Product.Clear()
        self.Price.Clear()
        self.Store.Clear()
        self.Brand.Clear()
        self.Description.Clear()
        cursor.close()

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

app = wx.App()
frame = MyFrame(None, -1, "Grocery Database")
frame.Show()
app.MainLoop()