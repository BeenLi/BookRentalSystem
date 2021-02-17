# -*- coding: utf-8 -*-
#!/usr/bin/env python
import wx
import wx.lib.sized_controls as sc

class AFrame(sc.SizedFrame):
    def __init__(self, *args, **kwds):
        super(AFrame, self).__init__(*args, **kwds)

        pane = self.GetContentsPane()

        self.tc1 = wx.TextCtrl(pane, style=wx.TE_PROCESS_ENTER)
        self.tc2 = wx.TextCtrl(pane)

        self.tc1.Bind(wx.EVT_TEXT_ENTER, self.onTc1Enter)

    def onTc1Enter(self, Evt):
        self.tc2.ChangeValue(self.tc1.GetValue())



if __name__ == "__main__":
    import wx.lib.mixins.inspection as WIT

    app = WIT.InspectableApp()
    f = AFrame(None)
    f.Show()
    app.MainLoop()