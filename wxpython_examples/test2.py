import wx
import MySQLdb

class MyFrame(wx.Frame):
    """frame and widgets to handle input and output of shopping list"""
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        # add panel, labels, text and sizer widgets
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('Light Gray')
        label1 = wx.StaticText(panel, -1, "Enter Product:")
        self.Product = wx.TextCtrl(panel, -1, "")
        self.list = wx.Button(panel, -1, ' Execute Query ')
        self.list.Bind(wx.EVT_BUTTON, self.makeList)
        self.result = wx.TextCtrl(panel, -1, size=(290, 100), 
            style=wx.TE_MULTILINE)
        
        # use gridbagsizer for layout of widgets
        sizer = wx.GridBagSizer(vgap=5, hgap=10)
        sizer.Add(label1, pos=(0, 0))
        sizer.Add(self.Product, pos=(0, 1))  # row 0, column
        sizer.Add(self.list, pos=(2, 1), span=(1, 2))
        # span=(1, 2) --> allow to span over 2 columns 
        sizer.Add(self.result, pos=(4, 0), span=(1, 2))
        
        # use boxsizer to add border around sizer
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        panel.SetSizerAndFit(border)
        self.Fit()
        
    def makeList(self, event):
        """print shopping list"""
        # query database
        db=MySQLdb.connect("localhost", "root", "kanga112", "grocery")
        cursor = db.cursor()
        Product = self.Product.GetValue()
        # get the values from the input widgets
        sql = """SELECT * FROM prices where Product = '%s'""" %(Product)
        cursor.execute(sql)
        # show the result
        resultStr1 = "%s" %Product
        self.result.SetValue(sql)
        
app = wx.App()
frame = MyFrame(None, -1, "Shopping List")
frame.Show()
app.MainLoop()