# simple_note.py

import random
import wx


class TabPanel(wx.Panel):

    def __init__(self, parent, name):
        """"""
        super().__init__(parent=parent)
        self.name = name

        colors = ["red", "blue", "gray", "yellow", "green"]
        self.SetBackgroundColour(random.choice(colors))

        btn = wx.Button(self, label="Press Me")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)


class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """


    def __init__(self):
        """Constructor"""
        super().__init__(None, wx.ID_ANY,
                         "Notebook Tutorial",
                         size=(600,400)
                         )
        panel = wx.Panel(self)

        self.notebook = wx.Notebook(panel)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change)
        tabOne = TabPanel(self.notebook, name='Tab 1')
        self.notebook.AddPage(tabOne, "Tab 1")

        tabTwo = TabPanel(self.notebook, name='Tab 2')
        self.notebook.AddPage(tabTwo, "Tab 2")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()

    def on_tab_change(self, event):
        # Works on Windows and Linux, but not Mac
        current_page = self.notebook.GetCurrentPage()
        print(current_page.name)
        event.Skip()


if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    app.MainLoop()