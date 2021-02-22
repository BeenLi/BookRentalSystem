import wx
import datetime
import wx.adv
import wx.grid as gridlib
import wx.lib.embeddedimage
from icon import img
from db_interface import *
from db_info import *
import copy


class MyFrame(wx.Frame):
    def __init__(self, title, icon, table_info):
        super().__init__(parent=None, title=title)
        """ 当我们把panel加入我们的frame中时, 它是sole child;会自动扩展整个frame """
        self.table_info = table_info
        p = wx.Panel(self)

        " 设置大小 "
        self.SetSize(1100, 600)

        " 设置图标 "
        self.SetIcon(wx.lib.embeddedimage.PyEmbeddedImage(icon).GetIcon())

        " 设置状态栏 "
        self.CreateStatusBar()

        " 设置菜单栏 "
        self.create_menu()

        " 设置3个表notebook "
        self.nb = wx.Notebook(p)
        # data = [表1data, 表2data, 表3data]
        tab1 = main_panel(self.nb, table_info[0][0], table_info[0][1],
                          table_index=0, show_flag=table_info[0][2])

        tab2 = customer_panel(self.nb, table_info[1][0], table_info[1][1],
                              table_index=1, show_flag = table_info[1][2], book_info=tab1.mygrid)

        tab3 = order_panel(self.nb, table_info[2][0], table_info[2][1],
                           table_index=2, show_flag = table_info[2][2], book_info=tab1.mygrid, customer_info=tab2.mygrid)


        self.nb.AddPage(tab1, "书单信息")
        self.nb.AddPage(tab2, "顾客信息")
        self.nb.AddPage(tab3, "订单信息")

        self.grid = [tab1.mygrid, tab2.mygrid, tab3.mygrid]
        " 设置notebook 到一个 sizer"
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND|wx.ALL, 5)
        p.SetSizer(sizer)
        p.Layout()
        " 展示Frame "
        self.Center()
        self.Layout()
        self.Show()

        " 每隔一分钟 自动保存到数据库 "
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.auto_commit)

        self.timer.Start(1000*60*1)

        " 每隔5小时 自动备份数据到 Excel "
        self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.auto_backup)
        self.timer.Start(1000*60*60*5)

    def auto_commit(self, event):
        try:
            write_to_db([grid.data for grid in self.grid], table_index=[0,1,2])
        except Exception as e:
            wx.MessageBox(f"{e}\n提交到数据库失败, 请核对是否有非法数据", "警告", wx.OK)

    def auto_backup(self, event):
        try:
            data = [[self.table_info[i][0]] + grid.data for i, grid in enumerate(self.grid)]
            write_excel(f"D:\\星月书店数据备份文件夹\\{(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'))}.xlsx",
                        sheet_index=[0,1,2], data=data)
            wx.MessageBox("恭喜你~ 成功备份数据", "恭喜", wx.OK)
        except Exception as e:
            wx.MessageBox(f"{e}\n备份数据到Excel失败, 请核对是否有非法数据", "警告", wx.OK)

    def OneKeySave(self, event):
        try:
            write_to_db([grid.data for grid in self.grid], table_index=[0,1,2])
            wx.MessageBox("恭喜你~已经成功提交到数据库", "恭喜", wx.OK)
        except Exception as e:
            wx.MessageBox(f"{e}\n提交到数据库失败, 请核对是否有非法数据", "警告", wx.OK)

    def create_menu(self):
        menu_bar = wx.MenuBar()

        """ 1. 管理菜单 """
        manage_menu = wx.Menu()
        ImportExcel = manage_menu.Append(
            wx.ID_ANY, "导入",
            "从Excel中导入数据"
        )
        ExportExcel = manage_menu.Append(
            wx.ID_ANY, "导出",  # title
            "将数据导出到Excel"  # help_string
        )
        OneKeySave = manage_menu.Append(
            wx.ID_ANY, "保存",
            "将数据一键保存到数据库中"
        )
        OneKeyBackup = manage_menu.Append(
            wx.ID_ANY, "备份",
            "将数据备份到[D:\\星月书店备份文件夹]目录下"
        )

        menu_bar.Append(manage_menu, "管理")
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.importfromexcel,
            source=ImportExcel
        )
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.exporttoexcel,
            source=ExportExcel
        )
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.OneKeySave,
            source=OneKeySave
        )
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.auto_backup,
            source=OneKeyBackup
        )

        """ 2. 帮助菜单"""
        help_menu = wx.Menu()
        intro_info = help_menu.Append(
            wx.ID_ANY, '使用说明',
            '平常怎么使用该系统'
        )
        about_info = help_menu.Append(
            wx.ID_ANY, '关于',
            '软件信息'
        )

        menu_bar.Append(help_menu, '帮助')
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.press_intro_info,
            source=intro_info
        )
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.press_about_info,
            source=about_info
        )

        self.SetMenuBar(menu_bar)

    """菜单栏响应逻辑"""

    def press_intro_info(self, event):
        spec = ["使用说明", "1. 备份: 将所有数据保存到excel文件中(用当前时间命名文件名)", "2. 提交: 将所有数据上传到数据库中(用户不可见)",
                "3. 导入导出: 可以将其中一个表或多个表导入到软件中,或者从软件导出到特定Excel文件中",
                "4. 自动上传周期: 1分钟;自动备份周期:5小时"]
        dlg = IntroDialog(*spec, parent=None, title="使用说明")
        dlg.ShowModal()
        dlg.Destroy()
        # print("点击<使用说明>")

    def press_about_info(self, event):
        # print("点击<关于>")
        dlg = AboutDialog(parent=None, title="软件信息")
        dlg.ShowModal()
        dlg.Destroy()

    def importfromexcel(self, event):
        chose = Chose_tables(parent=None, title="选择导入的表", mygrid=self.grid)
        chose.ShowModal()
        chose.Destroy()

    def exporttoexcel(self, event):
        chose = Chose_tables(parent=None, title="选择导出的表", mygrid=self.grid)
        chose.ShowModal()
        chose.Destroy()


""" 主界面 """

" 创建grid类 "


class myGrid(wx.grid.Grid):
    def __init__(self, parent, table_label, data, table_index, show_flag, book_info, customer_info):
        """
        创建表格控件
        :param parent:
        :param table_label: 列的title
        :param data: 填充表格的数据
        """
        wx.grid.Grid.__init__(self, parent, id=wx.ID_ANY)
        self.data = data
        self.data_copy = copy.deepcopy(self.data)           # 为了返回的时候用
        self.table_index = table_index
        self.table_label = table_label
        self.book_info = book_info
        self.customer_info = customer_info
        self.show_index = []

        # 设置要show的数据
        self.show_flag = show_flag
        self.show_title = get_show_data_helper(self.table_label, self.show_flag)

        self.RowNum = len(self.data)
        self.ColNum = len(self.show_title)

        # Grid
        self.CreateGrid(self.RowNum, self.ColNum)
        self.dict = {}  # show_title--index 对应起来(把所有的title对应起来)
        for i in range(len(self.table_label)):
            self.dict[self.table_label[i]] = i
        self.EnableEditing(True)
        self.EnableDragCell(False)
        self.EnableGridLines(True)
        # self.SetColSize(0, 150)  # 格子大小自适应内容

        # 设置列名称
        for i, m in enumerate(self.show_title):
            self.SetColLabelValue(i, m)
        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        self.EnableDragRowSize(True)
        self.SetRowLabelSize(80)
        self.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # 事件
        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.editor_shown)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.cell_changed)

        # 显示表格
        self.DisplayGrid()

    def get_next_uid(self):  # 获得下一个uid
        if self.data == []:  # 还有没用户(即没有办卡记录时)
            return 1
        else:
            return int(self.data[-1][0]) + 1

    def cell_changed(self, event):
        (row, column) = (event.GetRow(), event.GetCol())
        value = self.GetCellValue(row, column)
        if self.table_index > 0:   # 表2或者表3(因为顾客编号没有显示出来)
            column += 1
        column_title = self.table_label[column]
        message = wx.MessageDialog(self, f"你确定要将[{str(column_title)}]修改成[{str(value)}]吗?", '警告', wx.OK | wx.CANCEL | wx.ICON_WARNING)
        result = message.ShowModal()
        if result == wx.ID_CANCEL:
            self.DisplayGrid(self.data[self.show_index[row]])
        else:
            self.data_copy = copy.deepcopy(self.data)         # 每次data的修改都要备份到self.data_copy
            if self.show_index:
                self.data[self.show_index[row]][column] = value
                row_data = self.data[self.show_index[row]]
            else:
                self.data[row][column] = value
                row_data = self.data[row]
            " 完成同步书名的操作(保证数据一致性) "
            main_frame = app.GetTopWindow()

            if self.table_index == 0 and column_title == "书名":
                edit_isbn = row_data[0]
                edit_bname = row_data[column]
                tab3_grid = main_frame.grid[2]
                tab3_data = tab3_grid.data
                tab3_grid.data_copy = copy.deepcopy(tab3_data)
                for row in tab3_data:
                    if row[2] == edit_isbn:
                        row[3] = edit_bname
                tab3_grid.DisplayGrid()
            elif self.table_index == 2 and column_title == "租书书名":
                edit_isbn = row_data[2]                          # row_data 为  grid_data 没有去除uid
                edit_bname = row_data[column]
                tab1_grid = main_frame.grid[0]
                tab1_data = tab1_grid.data
                tab1_grid.data_copy = copy.deepcopy(tab1_data)  # 备份
                for row in tab1_data:
                    if row[0] == edit_isbn:
                        row[1] = edit_bname
                tab1_grid.DisplayGrid()
            event.Skip()
        message.Destroy()

    def editor_shown(self, event):
        pass
        # (row, column) = (event.GetRow(), event.GetCol())
        # value = self.GetCellValue(row, column)
        # message = wx.MessageDialog(self, f"你确定要修改[{str(value)}]吗?", '警告', wx.OK | wx.CANCEL | wx.ICON_WARNING)
        # result = message.ShowModal()
        # if result == wx.ID_CANCEL:
        #     pass
        # else:
        #     event.Skip()
        # message.Destroy()

    def DisplayGrid(self, data=None):
        if data == None:
            data = self.data
        data = get_show_data(data, self.show_flag)
        rownum = len(data)
        sub_num = rownum - self.GetNumberRows()
        try:
            if sub_num > 0:
                self.AppendRows(numRows=sub_num)
            elif sub_num < 0:
                self.DeleteRows(pos=0, numRows=abs(sub_num))
            colnum = len(data[0])
        except:
            return
        for i in range(rownum):
            for j in range(colnum):
                self.SetCellValue(i, j, str(data[i][j]))
        self.AutoSize()

    def search_show(self, keyword, value):
        " 为了搜索显示的帮助函数 "
        keyword_index = self.dict[keyword]
        new_data = []
        self.row = []
        self.show_index = []
        for i, row in enumerate(self.data):
            if str(row[keyword_index]) == str(value):
                new_data.append(row)
                self.row.append(i)
                self.show_index.append(i)                   # 查找到的记录所在行的索引
        self.DisplayGrid(new_data)


class main_panel(wx.Panel):
    def __init__(self, parent, column_titles, data, table_index, show_flag=None):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.book_info = None
        self.customer_info = None
        """ 表格 控件"""
        grid_data = data             # data 包含3个表的数据
        self.mygrid = myGrid(self, column_titles, grid_data, table_index, show_flag, self.book_info, self.customer_info)

        self.mygrid.DisplayGrid(grid_data)

        self.myquery = Query(parent=self, columns=column_titles, mygrid=self.mygrid)
        self.mymodify = modify(parent=self, mygrid=self.mygrid)
        left_sizer.Add(self.myquery.StaticBoxSizer, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.mymodify.StaticBoxSizer, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(left_sizer, 1, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(self.mygrid, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(main_sizer)


"""
表2(顾客信息表: 办卡)
"""
class customer_panel(main_panel):
    def __init__(self, parent, column_titles, data, table_index, show_flag, book_info):
        main_panel.__init__(self, parent, column_titles, data, table_index, show_flag=show_flag)
        # book_info 为表1的 mygrid 对象
        self.book_info = book_info            # 顺序执行,上面的父类初始化后,才会改写self.book_info

"""
表3(订单信息表: 借书, 还书)
"""
class order_panel(main_panel):
    def __init__(self, parent, column_titles, data, table_index, show_flag, book_info, customer_info):
        main_panel.__init__(self, parent, column_titles, data, table_index, show_flag=show_flag)
        self.book_info = book_info
        self.customer_info = customer_info

""" 主界面左边 "查询" 框"""


class Query(wx.StaticBox):
    def __init__(self, parent, columns, mygrid):
        super(Query, self).__init__(parent)
        self.parent = parent
        self.CreateQueryRecord()
        self.grid = mygrid
        self.ID = []
        for column in columns:
            self.ID.append(self.AddWidgets(column))

    def CreateQueryRecord(self):
        self.staticBox = wx.StaticBox(self.parent, label="查询")
        self.StaticBoxSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)

    def AddWidgets(self, label_text):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_label = wx.StaticText(self.staticBox, label=label_text, size=(50, -1))
        if label_text == "办卡日期" or label_text == "借书日期" or label_text == "还书日期":
            text_ctrl = \
                wx.adv.GenericDatePickerCtrl(self.staticBox, style=wx.TAB_TRAVERSAL
                                                         | wx.adv.DP_DROPDOWN
                                                         | wx.adv.DP_SHOWCENTURY
                                                         | wx.adv.DP_ALLOWNONE, name="日期", size=self.size)
        elif label_text == "办卡类型":
            text_ctrl = wx.Choice(self.staticBox, choices=["月卡", "季卡", "年卡"], name="办卡类型", size=self.size)
        else:
            text_ctrl = wx.TextCtrl(self.staticBox,style=wx.TE_PROCESS_ENTER, name=label_text)
            text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.press_button)
            self.size = text_ctrl.GetSize()
        text_button = wx.Button(self.staticBox, label="查询", name=label_text, size=(5, -1))
        text_button_rollback = wx.Button(self.staticBox, label="返回", name=label_text)

        row_sizer.Add(text_label, 1, wx.ALL, 2)
        if label_text == "办卡日期" or label_text == "借书日期" or label_text == "还书日期":
            row_sizer.Add(text_ctrl, 1, wx.ALL, 2)
        elif label_text == "办卡类型":
            row_sizer.Add(text_ctrl, 1, wx.ALL, 2)
        else:
            row_sizer.Add(text_ctrl, 1, wx.ALL, 2)
        row_sizer.Add(text_button, 1, wx.ALL, 2)
        row_sizer.Add(text_button_rollback, 1, wx.ALL, 2)
        self.StaticBoxSizer.Add(row_sizer, 1, wx.ALL, 2)

        text_button.Bind(event=wx.EVT_BUTTON, handler=self.press_button)
        text_button_rollback.Bind(event=wx.EVT_BUTTON, handler=self.press_rollback)
        return text_ctrl.GetId()

    def press_button(self, event):
        button = event.GetEventObject()
        label = button.GetName()  # 获取标签名
        index = self.grid.dict[label]  # 标签的序号
        text_ctrl = self.FindWindowById(self.ID[index], self.staticBox)
        if label == "办卡类型":
            value= text_ctrl.GetString(text_ctrl.GetCurrentSelection())   # 办卡类型
        elif label == "借书日期" or label == "还书日期" or label == "办卡日期":
            value = wxdate2pydate(text_ctrl.GetValue(), "%Y-%m-%d")    # 把wxdate --> pydate
        else:
            value = text_ctrl.GetValue()
        self.grid.search_show(keyword=label, value=value)
        self.grid.ForceRefresh()
        event.Skip()

    def press_rollback(self, event):
        self.grid.DisplayGrid(self.grid.data)
        self.grid.ForceRefresh()
        button = event.GetEventObject()
        label = button.GetName()  # 获取标签名
        index = self.grid.dict[label]  # 标签的序号
        text_ctrl = self.FindWindowById(self.ID[index], self.staticBox)
        if label == "办卡类型":
            text_ctrl.SetStringSelection("")
        elif label == "借书日期" or label == "还书日期" or label == "办卡日期":
            text_ctrl.SetValue(pydate2wxdate(datetime.date.today()))
        else:
            text_ctrl.SetValue("")
        self.grid.show_index = []


""" 左下角的 管理 控件 """


class modify(wx.StaticBox):
    def __init__(self, parent, mygrid, book_info=None):
        super(modify, self).__init__(parent)
        self.parent = parent
        self.book_info = book_info
        self.grid = mygrid
        self.CreateQueryRecord()
        self.AddWidgets()


    def CreateQueryRecord(self):
        self.staticBox = wx.StaticBox(self.parent, label="管理")
        self.StaticBoxSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)

    def AddWidgets(self):
        label1 = "录书"
        if isinstance(self.parent, customer_panel):
            label1 = "办卡"
        elif isinstance(self.parent, order_panel):
            label1 = "借书"
        row_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        text_button11 = wx.Button(self.staticBox, label=label1)
        text_button11.Bind(wx.EVT_BUTTON, self.addItem)

        label2 = "删除"
        if isinstance(self.parent, order_panel):
            label2 = "还书"
        text_button12 = wx.Button(self.staticBox, label=label2)
        text_button12.Bind(wx.EVT_BUTTON, self.deleteItem)

        row_sizer1.Add(text_button11, 1, wx.ALL | wx.EXPAND, 5)
        row_sizer1.Add(text_button12, 1, wx.ALL | wx.EXPAND, 5)

        row_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        text_button21 = wx.Button(self.staticBox, label="修改")
        text_button21.Bind(wx.EVT_BUTTON, self.modifyItem)

        text_button22 = wx.Button(self.staticBox, label="统计")
        text_button22.Bind(wx.EVT_BUTTON, self.statistic)

        row_sizer2.Add(text_button21, 1, wx.ALL | wx.EXPAND, 5)
        row_sizer2.Add(text_button22, 1, wx.ALL | wx.EXPAND, 5)

        row_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        text_button31 = wx.Button(self.staticBox, label="返回")
        text_button31.Bind(wx.EVT_BUTTON, self.rollback)

        text_button32 = wx.Button(self.staticBox, label="提交")
        text_button32.Bind(wx.EVT_BUTTON, self.commit)

        row_sizer3.Add(text_button31, 1, wx.ALL | wx.EXPAND, 5)
        row_sizer3.Add(text_button32, 1, wx.ALL | wx.EXPAND, 5)

        self.StaticBoxSizer.Add(row_sizer1, 1, wx.ALL | wx.EXPAND, 5)
        self.StaticBoxSizer.Add(row_sizer2, 1, wx.ALL | wx.EXPAND, 5)
        self.StaticBoxSizer.Add(row_sizer3, 1, wx.ALL | wx.EXPAND, 5)

        if isinstance(self.parent, order_panel):
            row_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
            text_button41 = wx.Button(self.staticBox, label="删除")
            text_button41.Bind(wx.EVT_BUTTON, self.deleteItem)

            row_sizer4.Add(text_button41, 1, wx.ALL | wx.EXPAND, 5)

            self.StaticBoxSizer.Add(row_sizer4, 1, wx.ALL | wx.EXPAND, 5)


    def addItem(self, event):
        widget = event.GetEventObject()
        widget_label = widget.GetLabel()
        attribute = self.grid.table_label.copy() # 获得表格控件的属性列表(当心remove方法改变table_label)
        dialog = EditDialog(attribute, title="添加条目", mygrid=self.grid, label=widget_label)
        dialog.ShowModal()
        dialog.Destroy()

    def deleteItem(self, event):
        widget = event.GetEventObject()
        label = widget.GetLabel()
        index_value = self.grid.GetSelectedRows()  # 第几行(以0算起)
        if self.grid.GetNumberRows() == 0:         # 没有选上任何一行
            return
        if label == "还书":
            if index_value:
                if self.grid.show_index:
                    self.grid.data[self.grid.show_index[index_value[0]]][-1] = datetime.date.today()
                    value = self.grid.data[self.grid.show_index[index_value[0]]]      # 所还的书在的行的数据
                else:
                    self.grid.data[index_value[0]][-1] = datetime.date.today()
                    value = self.grid.data[index_value[0]]
                if self.grid.show_index:
                    self.grid.SetCellValue(index_value[0], len(self.grid.show_title)-1, str(datetime.date.today()))
                else:
                    self.grid.DisplayGrid(self.grid.data)
                " 还书 库存+1 逻辑 "
                main_frame = app.GetTopWindow()
                tab1 = main_frame.grid[0]
                tab1.data_copy = copy.deepcopy(tab1.data)
                for row in tab1.data:
                    if row[0] == value[2]:  # ISBN相同
                        row[-1] = row[-1] + 1  # 库存+1
                tab1.DisplayGrid(tab1.data)
        else:
            if index_value != None:
                if self.grid.show_index:
                    self.grid.data_copy = copy.deepcopy(self.grid.data)
                    del self.grid.data[self.grid.show_index[index_value[0]]]
                    self.grid.DeleteRows(pos=index_value[0], numRows=1)
                    return
                self.grid.data_copy = copy.deepcopy(self.grid.data)
                self.grid.data = [i for num, i in enumerate(self.grid.data) if num not in index_value]
                self.grid.DeleteRows(pos=0, numRows=len(index_value))
                self.grid.DisplayGrid(self.grid.data)

    def modifyItem(self, event):
        widget = event.GetEventObject()
        label = widget.GetLabel()
        attribute = self.grid.show_title # 获得表格控件的属性列表
        try:
            index = self.grid.GetSelectedRows()[0]
        except:
            return
        self.show_index = self.grid.show_index
        if self.show_index:
            attribute_value = get_show_data(self.grid.data, self.grid.show_flag)[self.show_index[index]]
        else:
            attribute_value = get_show_data(self.grid.data, self.grid.show_flag)[index]
        dialog = EditDialog(attribute, attribute_value, title="修改条目", mygrid=self.grid, index=index, label=label)
        dialog.ShowModal()
        dialog.Destroy()

    def statistic(self, event):
        type_panel = self.parent
        mydata = self.grid.data
        if type(type_panel) == main_panel:       # 因为isinstance 不考虑继承(认为子类也属于父类)
            kind_num = len(mydata)
            book_num = sum([int(a[3]) for a in mydata])
            price_sum = sum(float(a[2]) * float(a[3]) for a in mydata)
            statistic_info = ["统计数据", f"1. 书的种类:  {kind_num}种", f"2. 书的总量: {book_num}本",
                              f"3. 书的总金额为: {price_sum:.2f}块"]
            dialog = IntroDialog(*statistic_info, parent=None, title="星月书店库存信息")
            dialog.ShowModal()
            dialog.Destroy()
        elif type(type_panel) == customer_panel:
            total_customer = len(mydata)           # 总共办卡人数
            total_month = len([row for row in mydata if row[2] == "月卡"])
            total_season = len([row for row in mydata if row[2] == "季卡"])
            total_year = len([row for row in mydata if row[2] == "年卡"])
            statistic_info = ["统计数据", f"1. 总共办卡人数:  {total_customer}人",
                              f"2. 总共月卡人数: {total_month}人",
                              f"3. 总共季卡人数: {total_season}人",
                              f"4. 总共年卡人数: {total_year}人"]
            dialog = IntroDialog(*statistic_info, parent=None, title="星月书店会员信息")
            dialog.ShowModal()
            dialog.Destroy()

        elif type(type_panel) == order_panel:
            total_order_num = len(mydata)    # 总共借出的书总数
            cur_outbook_num = len([row for row in mydata if row[-1] == None])  # 一共有多少本书在外面(没还)
            cur_inbook_num  = total_order_num - cur_outbook_num                # 借出去已经还的书有多少本
            statistic_info = ["统计数据", f"1. 总共借书记录次数: {total_order_num}次",
                              f"2. 没有还的书总共有: {cur_outbook_num}本",
                              f"3. 借出已经还的书有: {cur_inbook_num}本"]
            dialog = IntroDialog(*statistic_info, parent=None, title="星月书店借书信息")
            dialog.ShowModal()
            dialog.Destroy()



    def rollback(self, event):
        if len(self.grid.data_copy) > len(self.grid.data):
            self.grid.AppendRows(1)
        if len(self.grid.data_copy) < len(self.grid.data):
            self.grid.DeleteRows(pos=0, numRows=1)
        self.grid.DisplayGrid(self.grid.data_copy)
        self.grid.data = copy.deepcopy(self.grid.data_copy)

    def commit(self, event):
        table_index = self.grid.table_index
        try:
            write_to_db([self.grid.data], table_index=table_index)
            wx.MessageBox("恭喜你~已经成功提交到数据库", "恭喜", wx.OK)
        except:
            wx.MessageBox("提交到数据库失败, 请核对是否有非法数据", "警告", wx.OK)


' 修改对话框 '


class EditDialog(wx.Dialog):
    def __init__(self, keyword, value=None, title=None, mygrid=None, index=None, label=None):
        """
        添加或者修改对话框
        :param data: 添加的话不需要提供数据,修改需要提供原先的数据
        """
        super().__init__(parent=None, title=f"正在{title}")
        self.value = value        # 属性的值
        self.index = index
        self.grid = mygrid
        self.table_index = self.grid.table_index
        self.show_index = mygrid.show_index
        self.label = label        # 弹出修改对话框所对应按钮的名称
        self.attribute = keyword  # 属性列表
        self.flag = False
        if self.label == "借书":
            self.attribute.remove("还书日期")
            self.flag = True           # 特殊处理, 多加几个ISBN和书名框
        self.attribute_value = value if (value != None) else ["" for i in range(len(keyword))]

        # 对应属性的值

        self.ID = []
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(len(keyword)):
            if self.grid.GetParent().book_info != None:   # 第2和第3个表格
                " 始终建立一个 textctrl(根据属性建立不一样的控制框) "
                if self.attribute[i] == "ISBN" and self.flag:
                    self.staticBox = wx.StaticBox(self, label="租书信息")
                    self.StaticBoxSizer = wx.StaticBoxSizer(self.staticBox, wx.HORIZONTAL)

                    self.sizer1 = wx.BoxSizer(wx.VERTICAL)  # 装第一个书本信息
                    self.attribute_ctrl01 = wx.TextCtrl(self.staticBox, value=str(self.attribute_value[i]),
                                                        name="text01", style=wx.TE_PROCESS_ENTER)   # ISBN
                    self.attribute_ctrl01.Bind(wx.EVT_TEXT_ENTER, self.OnISBNEnter)
                    self.add_widgets(self.attribute[i], self.attribute_ctrl01)
                    self.attribute_ctrl11 = wx.TextCtrl(self.staticBox, value=str(self.attribute_value[i+1]),
                                                        name="text11") # 租书书名
                    self.add_widgets(self.attribute[i+1], self.attribute_ctrl11)

                    self.sizer2 = wx.BoxSizer(wx.VERTICAL)  # 装第二本书的信息
                    self.attribute_ctrl02 = wx.TextCtrl(self.staticBox, value=str(self.attribute_value[i]),
                                                        name="text02", style=wx.TE_PROCESS_ENTER)   # ISBN
                    self.attribute_ctrl02.Bind(wx.EVT_TEXT_ENTER, self.OnISBNEnter)
                    self.add_widgets(self.attribute[i], self.attribute_ctrl02)
                    self.attribute_ctrl12 = wx.TextCtrl(self.staticBox, value=str(self.attribute_value[i+1]),
                                                        name="text12") # 租书书名
                    self.add_widgets(self.attribute[i+1], self.attribute_ctrl12)

                    self.sizer3 = wx.BoxSizer(wx.VERTICAL)  # 装第三本书的信息
                    self.attribute_ctrl03 = wx.TextCtrl(self.staticBox, value=str(self.attribute_value[i]),
                                                        name="text03", style=wx.TE_PROCESS_ENTER)   # ISBN
                    self.attribute_ctrl03.Bind(wx.EVT_TEXT_ENTER, self.OnISBNEnter)
                    self.add_widgets(self.attribute[i], self.attribute_ctrl03)
                    self.attribute_ctrl13 = wx.TextCtrl(self.staticBox, value=str(self.attribute_value[i+1]),
                                                        name="text13") # 租书书名
                    self.add_widgets(self.attribute[i+1], self.attribute_ctrl13)

                    self.StaticBoxSizer.Add(self.sizer1)
                    self.StaticBoxSizer.Add(self.sizer2)
                    self.StaticBoxSizer.Add(self.sizer3)

                    self.main_sizer.Add(self.StaticBoxSizer)
                elif self.attribute[i] == "租书书名" and self.flag:
                    pass
                elif self.attribute[i] == "办卡日期" or self.attribute[i]=="借书日期" or self.attribute[i]=="还书日期":
                    self.attribute_ctrl =\
                        wx.adv.GenericDatePickerCtrl(self, style=wx.TAB_TRAVERSAL
                                                              | wx.adv.DP_DROPDOWN
                                                              | wx.adv.DP_SHOWCENTURY
                                                              | wx.adv.DP_ALLOWNONE, name="日期",
                                                     dt = pydate2wxdate(self.attribute_value[i]))
                    if type(self.grid.GetParent()) == customer_panel:            # 只有customer_panel需要计算到期天数
                        self.attribute_ctrl.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged)
                elif self.attribute[i] == "办卡类型":
                    self.attribute_ctrl = wx.Choice(self, choices=["月卡", "季卡", "年卡"], name="办卡类型")
                    if not self.attribute[i]:
                        pass
                    elif self.attribute[i] == "月卡":
                        self.attribute_ctrl.SetSelection(0)
                    elif self.attribute[i] == "季卡":
                        self.attribute_ctrl.SetSelection(1)
                    else:
                        self.attribute_ctrl.SetSelection(2)
                    self.attribute_ctrl.Bind(wx.EVT_CHOICE, self.OnDateChanged)
                elif self.attribute[i] == "剩余天数":
                    self.attribute_ctrl = wx.TextCtrl(self, value=str(self.attribute_value[i]), name="剩余天数")
                    try:
                        card_type = self.FindWindowByName("办卡类型", self)
                        choice = card_type.GetString(card_type.GetCurrentSelection())
                        start_date_ctrl = self.FindWindowByName("日期", self)
                        start_date = start_date_ctrl.GetValue()
                        if choice and start_date:
                            self.attribute_ctrl.SetValue(str(cal_num_date(choice, start_date)))
                    except Exception as e:
                        print("自动生成剩余天数错误:", e)
                elif self.attribute[i] == "顾客编号":
                    self.attribute_ctrl = wx.TextCtrl(self, value=str(self.attribute_value[i]), name="顾客编号",
                                                      style=wx.TE_PROCESS_ENTER)
                    self.attribute_ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
                elif self.attribute[i] == "顾客姓名":
                    self.attribute_ctrl = wx.TextCtrl(self, value=str(self.attribute_value[i]), name="顾客姓名",
                                                    style=wx.TE_PROCESS_ENTER)
                    self.attribute_ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
                elif self.attribute[i] == "ISBN":
                    self.attribute_ctrl = wx.TextCtrl(self, value=str(self.attribute_value[i]), name="ISBN",
                                                      style=wx.TE_PROCESS_ENTER)
                    self.attribute_ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnISBNEnter)
                elif self.attribute[i] == "租书书名":
                    self.attribute_ctrl = wx.TextCtrl(self, value=str(self.attribute_value[i]), name="租书书名",
                                                      style=wx.TE_PROCESS_ENTER)
                else:
                    self.attribute_ctrl = wx.TextCtrl(self, value=str(self.attribute_value[i]))

            else:
                " 对于第一个表格 "
                self.attribute_ctrl = wx.TextCtrl(self, value=str(self.attribute_value[i]))
            if (self.attribute[i] == "ISBN" or self.attribute[i] == "租书书名") and self.flag:
                " 如果是第三个表格的 借书控件 "
                pass
            else:
                self.add_widgets(self.attribute[i], self.attribute_ctrl)
                self.ID.append(self.attribute_ctrl.GetId())
        btn_sizer = wx.BoxSizer()
        save_btn = wx.Button(self, label='保存')
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, id=wx.ID_CANCEL), 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.CENTER)
        # self.SetSizer(self.main_sizer)
        self.SetSizerAndFit(self.main_sizer)

    def OnDateChanged(self, event):
        text_ctrl = self.FindWindowByName(name="办卡类型", parent=self)
        choice = text_ctrl.GetString(text_ctrl.GetCurrentSelection())   # 办卡类型
        text_ctrl = self.FindWindowByName(name="日期", parent=self)
        sel_date = text_ctrl.GetValue()          # wx.Datetime (办卡日期)
        # 计算剩余天数:
        widget = event.GetEventObject()
        if widget.GetName() == "日期":   # 修改日期
            sel_date = event.GetDate()
        num_days = cal_num_date(choice, sel_date)

        # 找到剩余天数对话框
        save_days_ctrl = self.FindWindowByName(name="剩余天数", parent=self)
        save_days_ctrl.SetValue(str(num_days))

    def OnTextEnter(self, event):
        text_ctrl_uid = self.FindWindowByName(name="顾客编号", parent=self)
        text_ctrl_uname = self.FindWindowByName(name="顾客姓名", parent=self)
        text_uid = text_ctrl_uid.GetValue()
        text_uname = text_ctrl_uname.GetValue()
        widget = event.GetEventObject()
        if widget.GetName() == "顾客编号":
            text_ctrl_uname.SetValue(str(get_uid_uname(self.grid.GetParent().customer_info.data, uid=text_uid, flag=0)))
        else:
            if self.value == None:
                text_ctrl_uid.SetValue(str(self.grid.get_next_uid()))
            else:
                text_ctrl_uid.SetValue(str(get_uid_uname(self.grid.GetParent().customer_info.data, uname=text_uname, flag=1)))

    def OnISBNEnter(self, event):
        def get_bname_from_isbn(data, isbn):
            " data 为表1的数据 "
            for row in data:
                if row[0] == isbn:
                    return row[1]
            return "没有录入该书, 请回到表1手动录入后再试"
        text_ctrl_isbn01 = self.FindWindowByName(name="text01", parent=self)
        text_ctrl_bname11 = self.FindWindowByName(name="text11", parent=self)

        text_ctrl_isbn02 = self.FindWindowByName(name="text02", parent=self)
        text_ctrl_bname12 = self.FindWindowByName(name="text12", parent=self)

        text_ctrl_isbn03 = self.FindWindowByName(name="text03", parent=self)
        text_ctrl_bname13 = self.FindWindowByName(name="text13", parent=self)

        " 修改order 对话框的 "
        modify_ctrl_isbn = self.FindWindowByName(name="ISBN", parent=self)
        modify_ctrl_bname = self.FindWindowByName(name="租书书名", parent=self)

        widget = event.GetEventObject()
        if widget.GetName() == "text01":
            text_isbn = text_ctrl_isbn01.GetValue()
            text_ctrl_bname11.SetValue(str(get_bname_from_isbn(self.grid.GetParent().book_info.data, text_isbn)))
        elif widget.GetName() == "text02":
            text_isbn = text_ctrl_isbn02.GetValue()
            text_ctrl_bname12.SetValue(str(get_bname_from_isbn(self.grid.GetParent().book_info.data, text_isbn)))
        elif widget.GetName() == "text03":
            text_isbn = text_ctrl_isbn03.GetValue()
            text_ctrl_bname13.SetValue(str(get_bname_from_isbn(self.grid.GetParent().book_info.data, text_isbn)))
        elif widget.GetName() == "ISBN":
            text_isbn = modify_ctrl_isbn.GetValue()
            modify_ctrl_bname.SetValue(str(get_bname_from_isbn(self.grid.GetParent().book_info.data, text_isbn)))


    def add_widgets(self, label_text, text_ctrl):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        if (label_text == "ISBN" or label_text == "租书书名") and self.flag:
            label = wx.StaticText(self.staticBox,label=label_text,
                              size=(100, -1))
            row_sizer.Add(label, 0, wx.ALL, 5)
            row_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            if text_ctrl.GetName()[-1] == "1":
                self.sizer1.Add(row_sizer, 0, wx.EXPAND)
            elif text_ctrl.GetName()[-1] == "2":
                self.sizer2.Add(row_sizer, 0, wx.EXPAND)
            elif text_ctrl.GetName()[-1] == "3":
                self.sizer3.Add(row_sizer, 0, wx.EXPAND)

        else:
            label = wx.StaticText(self, label=label_text,
                                  size=(100, -1))
            row_sizer.Add(label, 0, wx.ALL, 5)
            row_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            self.main_sizer.Add(row_sizer, 0, wx.EXPAND)

    def on_save(self, event):
        self.grid.data_copy = copy.deepcopy(self.grid.data)
        value = []
        for id in self.ID:
            text_ctrl = self.FindWindowById(id, self)
            if isinstance(text_ctrl, wx.Choice):
                value.append(text_ctrl.GetString(text_ctrl.GetCurrentSelection()))
            elif isinstance(text_ctrl, wx.adv.GenericDatePickerCtrl):
                value.append(wxdate2pydate(text_ctrl.GetValue(), "%Y-%m-%d"))
            else:
                value.append(text_ctrl.GetValue())
        if self.label == "借书":              # 借书的对话框, 要加上还书日期(设为空)
            new_value = []
            isbn01 = self.attribute_ctrl01.GetValue()
            bname11 = self.attribute_ctrl11.GetValue()

            isbn02 = self.attribute_ctrl02.GetValue()
            bname12 = self.attribute_ctrl12.GetValue()

            isbn03 = self.attribute_ctrl03.GetValue()
            bname13 = self.attribute_ctrl13.GetValue()

            value.append("")
            if isbn01:
                value1 = value.copy()
                value1.insert(2, isbn01)
                value1.insert(3, bname11)
                new_value.append(value1)
            if isbn02:
                value2 = value.copy()
                value2.insert(2, isbn02)
                value2.insert(3, bname12)
                new_value.append(value2)
            if isbn03:
                value3 = value.copy()
                value3.insert(2, isbn03)
                value3.insert(3, bname13)
                new_value.append(value3)

            # 完成库存减1的逻辑
            main_frame = app.GetTopWindow()
            tab1 = main_frame.grid[0]
            tab1.data_copy = copy.deepcopy(tab1.data)
            for row in self.grid.GetParent().book_info.data:
                if row[0] in [value[2] for value in new_value]:           # ISBN相同
                    row[-1] = int(row[-1]) -1                 # 库存-1
            tab1.DisplayGrid(tab1.data)
            value = new_value                                             # 统一符号
        cur_grid_data = self.grid.data                                    # 做一个引用

        if self.label == "修改":
            row_data = value
            if self.show_index:
                origin_data = cur_grid_data[self.show_index[self.index]]
            else:
                origin_data = cur_grid_data[self.index]

            " 完成同步书名的操作(保证数据一致性) "
            main_frame = app.GetTopWindow()
            if self.table_index == 0:
                edit_isbn = row_data[0]
                edit_bname = row_data[1]
                if edit_bname == origin_data[1]:  # 没有修改书名:
                    pass
                else:
                    tab3_grid = main_frame.grid[2]
                    tab3_data = tab3_grid.data
                    tab3_grid.data_copy = copy.deepcopy(tab3_data)
                    for row in tab3_data:
                        if row[2] == edit_isbn:
                            row[3] = edit_bname
                    tab3_grid.DisplayGrid()
            elif self.table_index == 2:
                edit_isbn = row_data[1]
                edit_bname = row_data[2]
                if edit_bname == origin_data[3]:
                    pass
                else:
                    tab1_grid = main_frame.grid[0]
                    tab1_data = tab1_grid.data
                    tab1_grid.data_copy = copy.deepcopy(tab1_data)  # 备份
                    for row in tab1_data:
                        if row[0] == edit_isbn:
                            row[1] = edit_bname
                    tab1_grid.DisplayGrid()

        if self.value == None:  # 增加一列,不是修改
            if not isinstance(value[0], (list, tuple)):
                value = [value]
            self.grid.AppendRows(len(value))
            for row in value:
                cur_grid_data.append(row)  # 先插入
            if self.show_index:
                cur_num = len(self.show_index)
                for i in range(len(value)):
                    for j in range(len(value[0])):
                        self.grid.SetCellValue(i+cur_num, j, str(value[i][j]))
                self.grid.ForceRefresh()
                self.grid.AutoSize()
                self.Destroy()
                return
        else:                                               # 修改的情况
            if self.show_index:
                origin_value = cur_grid_data[self.show_index[self.index]]
            else:
                origin_value = cur_grid_data[self.index]
            p = 0
            for index, flag in enumerate(self.grid.show_flag):
                if flag == 1:
                    origin_value[index] = value[p]          # 修改origin_value 就已经修改了self.grid.data
                    p += 1
            if self.show_index:
                for j in range(len(value)):
                    self.grid.SetCellValue(self.index, j, str(value[j]))  # 只重新更新修改的那一行
                self.Destroy()
                return
        self.grid.DisplayGrid(self.grid.data)               # 常规修改:没有查询 不是删除一行
        self.Destroy()
        return


" 菜单栏对话框 "


# 1.关于
class AboutDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        headline = "星月书店管理系统"
        headline_text = wx.StaticText(self, label=headline, size=(-1, 50))
        self.main_sizer.Add(headline_text, 0, wx.CENTER | wx.Top, 100)
        self.add_staticText("版本号", "2.1")
        self.add_staticText("制作人", "万力")
        self.add_staticText("完成段", "2021-02")
        self.SetSizer(self.main_sizer)
        # self.SetSizerAndFit(self.main_sizer)

    def add_staticText(self, label_key, label_value):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_key_ = wx.StaticText(self, label=label_key, size=(50, -1))
        label_value_ = wx.StaticText(self, label=label_value, size=(50, -1))
        row_sizer.Add(label_key_, 0, wx.ALL, 5)
        row_sizer.Add(label_value_, 0, wx.ALL, 5)
        self.main_sizer.Add(row_sizer, 0, wx.CENTER)


# 2. 使用说明
class IntroDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(IntroDialog, self).__init__(**kwargs)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        headline = args[0]
        headline_text = wx.StaticText(self, label=headline, size=(-1, 50))
        self.main_sizer.Add(headline_text, 0, wx.CENTER | wx.Top, 50)
        for text in args[1:]:
            self.add_staticText(specification=text)
        self.SetSizer(self.main_sizer)
        # self.SetSizerAndFit(self.main_sizer)

    def add_staticText(self, specification):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_key_ = wx.StaticText(self, label=specification)
        row_sizer.Add(label_key_, 0, wx.ALL, 5)
        self.main_sizer.Add(row_sizer, 0, wx.LEFT)


class Chose_tables(wx.Dialog):
    """
    导入导出时选择表项
    """

    def __init__(self, mygrid=None, **kwargs):
        super(Chose_tables, self).__init__(**kwargs)
        self.grid = mygrid           #
        self.InitUI()

    def InitUI(self):
        """主控制器"""
        mbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(self, label="表项")
        " radiobutton控制器 "
        sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)

        file1 = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckBox1 = wx.CheckBox(self, label="表1(图书信息表)", name="check1")
        file1.Add(self.CheckBox1, 1, wx.EXPAND | wx.ALL, 10)

        file2 = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckBox2 = wx.CheckBox(self, label="表2(顾客信息表)", name="check2")
        file2.Add(self.CheckBox2, 1, wx.EXPAND | wx.ALL, 10)

        file3 = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckBox3 = wx.CheckBox(self, label="表3(订单信息表)", name="check3")
        file3.Add(self.CheckBox3, 1, wx.EXPAND | wx.ALL, 10)

        sbs.Add(file1, 1, wx.ALL | wx.EXPAND, 2)
        sbs.Add(file2, 1, wx.ALL | wx.EXPAND, 2)
        sbs.Add(file3, 1, wx.ALL | wx.EXPAND, 2)

        selectfile_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.FileButton = wx.Button(self, label="浏览", size=(10, -1))
        if self.GetTitle() == "选择导入的表":
            self.FileButton.Bind(wx.EVT_BUTTON, self.SelectFile)
        elif self.GetTitle() == "选择导出的表":
            self.FileButton.Bind(wx.EVT_BUTTON, self.OnSaveAs)

        self.filename = wx.TextCtrl(self, value="C:")
        selectfile_sizer.Add(self.FileButton, 1, wx.ALL | wx.EXPAND, 10)
        selectfile_sizer.Add(self.filename, 1, wx.ALL | wx.EXPAND, 10)

        sbs.Add(selectfile_sizer, 1, wx.ALL | wx.EXPAND, 2)
        " 确定和取消按钮控制器 "
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label="确定")
        closeButton = wx.Button(self, label="取消")
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=50)

        " 绑定上面的文件选择框 和 下面的确定和取消按钮 "
        mbox.Add(sbs, flag=wx.EXPAND | wx.ALL, border=5)
        mbox.Add(hbox, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=5)

        " 绑定函数 "
        okButton.Bind(wx.EVT_BUTTON, self.pressok)
        closeButton.Bind(wx.EVT_BUTTON, self.pressclose)

        self.SetSizer(mbox)
        self.SetSizerAndFit(mbox)

    def pressok(self, event):
        """
        检测当前复选框有几个被选上
        :param event:
        :return:
        """
        filename = self.filename.GetValue()
        checkbox1 = wx.FindWindowByName("check1", self)
        checkbox2 = wx.FindWindowByName("check2", self)
        checkbox3 = wx.FindWindowByName("check3", self)
        index_flag = []
        if checkbox1.IsChecked():
            index_flag.append(0)
        if checkbox2.IsChecked():
            index_flag.append(1)
        if checkbox3.IsChecked():
            index_flag.append(2)
        # print("index_flag = %s" % index_flag)
        if filename != "C:":  # 选择了文件
            if self.GetTitle() == "选择导出的表":
                # print("导出")
                self.export_file(filename=filename, table_index=index_flag)
            elif self.GetTitle() == "选择导入的表":
                self.import_file(filename=filename, table_index=index_flag)
                # print("导入")
        else:
            wx.MessageBox("你还没有选择文件", "友情提示", wx.OK | wx.CANCEL)

    def pressclose(self, event):
        self.Destroy()

    def SelectFile(self, event):
        title = "选择一个文件"
        dlg = wx.FileDialog(self, title,
                            style=wx.DD_DEFAULT_STYLE, wildcard="Excel 工作簿(*.xlsx)|*.xlsx")
        if dlg.ShowModal() == wx.ID_OK:  # 如果用户按下OK button
            self.filename.SetValue(dlg.GetPath())
        dlg.Destroy()  # 好像会自动destroy;有个close方法,但是那仅仅隐藏


    def import_file(self, table_index, filename):
        """
        根据导入excel表单, 进行导入
        :param table: index (0,1,2)
        :param filename: absolute filename 
        :return:  None
        """
        data = []
        for index in table_index:
            grid = self.grid[index]
            data_tmp = read_excel(filename, index)
            if index == 1:
                for row in data_tmp[1:]:
                    if isinstance(row, (datetime.date, datetime.datetime)):
                        row[4] = row[4].strftime("%Y-%m-%d")      # datetime.datetime(2021, 1, 24, 0, 0)
            elif index == 2:
                for row in data_tmp[1:]:
                    if row[-1]: # 防止 还书日期 为空时 出现错误
                        if isinstance(row[-1], (datetime.date, datetime.datetime)):
                            row[-1] = row[-1].strftime("%Y-%m-%d")
                    else:
                        row[-1] = ""
                    if isinstance(row[-2], (datetime.date, datetime.datetime)):
                        row[-2] = row[-2].strftime("%Y-%m-%d")
            grid.data = data_tmp[1:]                    # 1. 设置表格数据
            grid.data_copy = copy.deepcopy(grid.data)   # 2. 备份表格数据
            grid.DisplayGrid()                          # 3. 显示表格数据
            data.append(data_tmp[1:])
        try:
            write_to_db(data, table_index)   # 写到数据库
            wx.MessageBox("恭喜你~, 导入成功", "恭喜", wx.OK)
            self.Destroy()   # 销毁
        except Exception as e:
            print(e)
            wx.MessageBox("导入错误, 请检察导入的文件是否合法", "警告", wx.OK)
            self.Destroy()

    def export_file(self, table_index, filename):
        """
        导出
        :param table: index
        :param filename:
        :return:
        """
        data = []
        for index in table_index:
            data_except_title = self.grid[index].data
            data_except_title.insert(0, self.grid[index].table_label)
            data.append(data_except_title)
        try:
            write_excel(filename=filename, sheet_index=table_index, data=data)
            wx.MessageBox(f"写入:{filename}成功", "恭喜你", wx.OK)
            self.Destroy()
        except:
            wx.MessageBox("导出错误, 请检察是否有非法的数据", "警告", wx.OK)
            self.Destroy()

    def OnSaveAs(self, event):
        filename = f"星月书店数据备份-{(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'))}.xlsx"
        with wx.DirDialog(self, "选择一个目录--保存Excel文件",
                        style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON) \
                as DirDialog:
            if DirDialog.ShowModal() == wx.ID_OK:
                pathname = DirDialog.GetPath() + "\\" + filename
                self.filename.SetValue(pathname)

def pydate2wxdate(date):
    " 把datetime -> wx.datetime"
    try:
        assert isinstance(date, (datetime.datetime, datetime.date))
    except:
        date = datetime.date.today()
    tt = date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTime.FromDMY(*dmy)

def wxdate2pydate(wxdate, formate):
    string = wxdate.Format(formate)
    return datetime.date(*tuple(list(map(int, string.split('-')))))

def get_uid_uname(data, uid=None, uname=None, flag=0):
    """
    根据uid返回uname(flag = 0)
    根据uname 返回uid(flag = 1)
    """
    return_value0 = return_value1 = '没有该顾客, 请重新输入'
    for row in data:
        if str(row[0]) == str(uid):
            return_value0 = row[1]
        if str(row[1]) == str(uname):
            return_value1 = row[0]
    if flag == 0:
        return return_value0
    else:
        return return_value1



def get_show_data(data, show_flag):
    """
    根据show_flag 从 data 中获得 show_data
    设 data 的数据格式为: [[xx, xx, xx] , [xx, xx, xx] , [xx...]]
    设 flag 的数据格式为: [1, 0 , 1]
    :param data:
    :param show_flag:
    :return:
    """
    if not data:                                # 防止data 为空
        return []
    if not isinstance(data[0], (list, tuple)):  # 防止data不是上述数据结构
        data = [data]
    return [get_show_data_helper(row, show_flag) for row in data]

def get_show_data_helper(row, show_flag):
    show_data = []
    for i, cell in enumerate(row):
        if show_flag[i] == 1:
            show_data.append(row[i])
    return show_data

def get_data_from_db():
    """
    从数据库中获取数据(用于刷新)
    :return: [(column_title, data, show_flag), ( ), ( )]
    column_title: ['ISBN', '书名', '单价', '库存']
    data :
        (('9787115376534', '自我', 88.0, 2),
        ('9787309069976', '人类动物园', 30.0, 1),
        ('9787309086232', '什么是数学', 43.0, 1),
        ('9787530214947', '愿生命从容', 39.8, 2),
        ('9787532742929', '挪威的森林', 23.0, 3),
        ('9787533936020', '月亮与六便士', 39.8, 2),
        ('9787544253994', '百年孤独', 39.5, 1),
        ('9787544294126', '毕业', 49.5, 5))
    show_title: ['书名', '单价', '库存']
    show_flag : [0, 1, 1, 1]

    """
    table_names = ["book_item", "customer_info", "order_info"]
    show_flag = [[1,1,1,1], [1,1,1,1,1,1], [0,1,1,1,1,1]]

    def get_tab_info(table_name):
        with Mysql_db(**db_connect) as db:  # db是__enter__方法的返回值, 即这个数据库对象
            data = db.search(f"select * from {table_name}")
            data = [list(row) for row in data]  # 把tuple转化为list
            if table_name == "customer_info":   # 每次打开软件都从新计算剩余天数
                for row in data:
                    row[-1] = cal_num_date(type_card=row[-3], start_date=row[-2])
            if table_name == "order_info":      # 把还书日期为None的改为''
                for row in data:
                    if row[-1] == None:
                        row[-1] = ''
            column_title = db.search(f"SHow full columns from {table_name}")  # 除了有列名外还有其它属性
            column_title = [column_title[i][-1] for i in range(len(column_title))]
            return [column_title, data, show_flag[table_names.index(table_name)]]
    tab_list = [get_tab_info(table_name) for table_name in table_names]
    return tab_list

def cal_num_date(type_card, start_date):
    """
    计算剩余天数
    :param type_card:  String: [月卡, 季卡, 年卡]
    :param start_date:  wx.DateTime(<wx.DateTime: "2021/2/16 0:00:00">) 或者 String(2020-02-12)
    :return: 返回int
    """
    today = datetime.date.today()

    if isinstance(start_date, wx.DateTime):
        start_date = start_date.Format("%Y-%m-%d")  # 先转化为str
    if isinstance(start_date, (datetime.date, datetime.datetime)): # 先转化为str
        start_date = start_date.strftime("%Y-%m-%d")
    start_date_list = list(map(int, start_date.split('-')))  # 转化为[年, 月, 日]
    end_date_list = start_date_list.copy()
    if type_card == "月卡":
        if start_date_list[1] + 1 > 12:
            end_date_list[0] = start_date_list[0] + 1   # 年份
        end_date_list[1] = (start_date_list[1] + 1) % 12
    elif type_card == "季卡":
        if start_date_list[1] + 3 > 12:
            end_date_list[0] = start_date_list[0] + 1
        end_date_list[1] = (start_date_list[1] + 3) % 12
    elif type_card == "年卡":
        end_date_list[0] = start_date_list[0] + 1

    " 计算两者之差 "
    days = (datetime.date(*tuple(end_date_list)) - today).days
    return 0 if days <= 0 else days


if __name__ == '__main__':
    app = wx.App()
    tab_list = get_data_from_db()

    frame = MyFrame("星月书店v2.1", icon=img, table_info=tab_list)
    app.MainLoop()
