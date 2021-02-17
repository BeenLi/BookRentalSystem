import wx

"""
wx.APP: 运行GUI所必须的, 通过.MainLoop()
wx.Frame: 创建一个窗口,给用户交互;已经包含了最大化,最小化,和关闭控价.
我们需要subclass wx.Frame和其它 widget: 为了更好获得这些部件的全部功能

通常我们还需要个面板(panel):有了面板我们可以遍历Tab
"""
class MyFrame(wx.Frame):
    def __init__(self, title):
        super().__init__(parent=None, title=title)
        """当我们把panel加入我们的frame中时, 它是sole child;会自动扩展整个frame"""
        panel = wx.Panel(self)

        """ 1 绝对布局 """
        # pos:默认是parent左上角为(0,0) : absolute position
        # self.text_ctrl = wx.TextCtrl(panel, pos=(5, 5))
        # my_btn = wx.Button(panel, label='Press Mw', pos=(5, 55))

        """ 2 动态布局 """
        # dynamic layout: Sizers: BoxSizer, GridSizer, FlexGridSizer
        my_sizer = wx.BoxSizer(wx.VERTICAL)  # 部件被加入的方向
        self.text_ctrl = wx.TextCtrl(panel)
        # 加部件加入到布局器中: my_sizer.Add()
        # window (the widget)
        # proportion: 在sizer的方向上,如果sizer变化,它里面的部件变化相对于其它部件的比例;0是不变化
        # flag: 标志, 用|传递多个标志; wx.ALL表示在四周加border(外边界)
        # border
        # userData
        my_sizer.Add(self.text_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        my_btn = wx.Button(panel, label='Press Me')
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        
        """给控件绑定事件"""
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)

        """ 加sizers应用到父组件上"""
        panel.SetSizer(my_sizer)

        """ 展示widgets """
        self.Show()

    """ button的回调函数 """
    # event 可以换成其它;它只是代表该方法被调用时, event是一个某种事件对象
    # <class 'wx._core.CommandEvent'>
    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything")
        else:
            print(f'You typed: "{value}"')


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame("星月书店v1.0")
    app.MainLoop()

