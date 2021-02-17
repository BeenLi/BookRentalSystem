import wx
import datetime
import wx.adv
#----------------------------------------------------------------------

class TestPanel(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        dpc1 = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged, dpc1)
        sizer.Add(dpc1, 0, wx.ALL, 50)
        # In some cases the widget used above will be a native date
        # picker, so show the generic one too.
        dpc2 = wx.adv.GenericDatePickerCtrl(self, size=(120,-1),
                                       style = wx.TAB_TRAVERSAL
                                       | wx.adv.DP_DROPDOWN
                                       | wx.adv.DP_SHOWCENTURY
                                       | wx.adv.DP_ALLOWNONE )
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged, dpc2)
        sizer.Add(dpc2, 0, wx.LEFT, 50)
        now = wx.DateTime.Now()
        print (wx.DateTime.FormatISODate(now))     # str 2021-02-16
        print (wx.DateTime.Format(now))            # str 2021/2/16 18:25:12
        dpc2.SetValue(wx.DateTime.Now())

    def OnDateChanged(self, evt):
        sel_date = evt.GetDate()
        print (sel_date.Format("%d-%m-%Y"))        # 转化为字符串

#----------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App()
    frame = TestPanel()
    frame.Show()
    app.MainLoop()