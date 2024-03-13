import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import sqlite3
import random


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None,
            title="Сервис автоматического распределения задач для выездных сотрудников",
        )

        panel = self.populate()
        panel.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Calibri"))

        self.initialize_db()
        self.resized = False  # the dirty flag
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.Show()
        self.Maximize(True)

    def OnSize(self, event):
        self.resized = True  # set dirty
        event.Skip()

    def OnIdle(self, event):
        if self.resized:
            # take action if the dirty flag is set
            print("New size:", self.GetSize())
            self.resized = False  # reset the flagass
            for i in range(3):
                self.list.SetColumnWidth(i, int(self.GetSize()[0] / 3))

    def initialize_db(self):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute(
            f"""
        CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
            )
        """
        )
        cursor.execute(
            f"""
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            assigned_to TEXT
            )
        """
        )
        conn.commit()
        conn.close()

    def populate(self):
        panel = wx.Panel(self)
        widgetSizerV = wx.BoxSizer(wx.VERTICAL)
        taskListSizer = wx.BoxSizer(wx.HORIZONTAL)
        widgetSizerH = wx.BoxSizer(wx.HORIZONTAL)
        addEmployeeSizer = wx.BoxSizer(wx.VERTICAL)
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        addTaskSizer = wx.BoxSizer(wx.VERTICAL)
        taskNameSizer = wx.BoxSizer(wx.VERTICAL)

        # Создаём виджет для добавления сотрудника в БД
        bs1 = wx.BoxSizer(wx.VERTICAL)
        bs2 = wx.BoxSizer(wx.VERTICAL)
        bs3 = wx.BoxSizer(wx.VERTICAL)
        l1 = wx.StaticText(panel, label="Фамилия")
        l2 = wx.StaticText(panel, label="Имя")
        l3 = wx.StaticText(panel, label="Отчество")
        bs1.Add(l1, 0, wx.ALL | wx.CENTER, 5)
        bs2.Add(l2, 0, wx.ALL | wx.CENTER, 5)
        bs3.Add(l3, 0, wx.ALL | wx.CENTER, 5)
        for widget in [l1, l2, l3]:
            widget.SetFont(
                wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Calibri")
            )
        self.surname = wx.TextCtrl(panel)
        bs1.Add(self.surname, 1, wx.ALL | wx.EXPAND, 5)
        self.name = wx.TextCtrl(panel)
        bs2.Add(self.name, 1, wx.ALL | wx.EXPAND, 5)
        self.middlename = wx.TextCtrl(panel)
        bs3.Add(self.middlename, 1, wx.ALL | wx.EXPAND, 5)
        for element in [bs1, bs2, bs3]:
            nameSizer.Add(element, 1, wx.ALL | wx.CENTER, 5)

        addEmployeeConfirm = wx.Button(panel, label="Добавить")
        addEmployeeConfirm.Bind(wx.EVT_BUTTON, self.on_addEmployeeConfirmPress)
        addEmployeeSizer.Add(
            wx.StaticText(panel, label="Добавить сотрудника"), 0, wx.ALL | wx.CENTER, 5
        )
        addEmployeeSizer.Add(nameSizer, 0, wx.ALL | wx.EXPAND, 5)
        addEmployeeSizer.Add(addEmployeeConfirm, 0, wx.ALL | wx.CENTER, 5)

        # Создаём виджет для создания задачи

        addTaskConfirm = wx.Button(panel, label="Создать")
        addTaskConfirm.Bind(wx.EVT_BUTTON, self.on_addTaskConfirmPress)
        st = wx.StaticText(panel, label="Создать задачу")

        st.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Calibri"))
        addTaskSizer.Add(st, 0, wx.ALL | wx.CENTER, 5)
        self.taskName = wx.TextCtrl(panel)
        taskNameSizer.Add(self.taskName, 1, wx.ALL | wx.EXPAND, 5)
        addTaskSizer.Add(taskNameSizer, 0, wx.ALL | wx.EXPAND, 5)
        addTaskSizer.Add(addTaskConfirm, 0, wx.ALL | wx.CENTER, 5)

        widgetSizerH.Add(addEmployeeSizer, 1, wx.ALL | wx.EXPAND, 50)
        widgetSizerH.Add(addTaskSizer, 1, wx.ALL | wx.EXPAND, 50)

        widgetSizerV.Add(widgetSizerH, 1, wx.ALL | wx.EXPAND, 50)

        st = wx.StaticText(panel, label="Текущие задачи")
        st.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Calibri"))
        widgetSizerV.Add(st, 0, wx.ALL | wx.CENTER, 5)
        self.list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.list.InsertColumn(0, "№ задачи")
        self.list.InsertColumn(1, "Название задачи")
        self.list.InsertColumn(2, "Назначенный сотрудник")
        widgetSizerV.Add(self.list, 1, wx.ALL | wx.EXPAND)

        showTasks = wx.Button(panel, label="Показать текущие задачи")
        showTasks.Bind(wx.EVT_BUTTON, self.on_showTasksPress)
        taskListSizer.Add(showTasks, 0, wx.ALL | wx.CENTER, 50)
        giveTasks = wx.Button(panel, label="Распределить задачи по сотрудникам")
        giveTasks.Bind(wx.EVT_BUTTON, self.on_giveTasksPress)
        taskListSizer.Add(giveTasks, 0, wx.ALL | wx.CENTER, 50)
        widgetSizerV.Add(taskListSizer, 0, wx.ALL | wx.CENTER)
        panel.SetSizer(widgetSizerV)
        for widget in [
            self.surname,
            self.middlename,
            self.name,
            self.taskName,
            self.list,
        ]:
            widget.SetFont(
                wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Calibri")
            )
        for widget in [addEmployeeConfirm, addTaskConfirm, showTasks, giveTasks]:
            widget.SetFont(
                wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Calibri")
            )
        return panel

    def on_showTasksPress(self, event):
        self.list.DeleteAllItems()
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT * FROM Tasks""")
            tasks = cursor.fetchall()
            for task in tasks:
                self.list.Append(list(task))

    def on_giveTasksPress(self, event):
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT id FROM Tasks WHERE assigned_to IS NULL""")

            task_ids = [task[0] for task in cursor.fetchall()]
            cursor.execute(f"""SELECT id FROM Employees""")
            ids = [rec[0] for rec in cursor.fetchall()]
            if ids:
                for task_id in task_ids:
                    sql = f"""UPDATE Tasks SET assigned_to = 
                    (SELECT name FROM Employees WHERE id = {ids[random.randint(0, len(ids)-1)]}) WHERE id = {task_id}"""
                    cursor.execute(sql)
                conn.commit()
            else:
                wx.MessageBox(
                    "Чтобы распределить задачи по сотрудникам, нужен хотя бы один сотрудник",
                    "Не хватает сотрудников для распределения задач",
                    wx.OK | wx.ICON_ERROR,
                )
            self.on_showTasksPress(event)

    def on_addEmployeeConfirmPress(self, event):
        try:
            name = self.name.GetValue()
            surname = self.surname.GetValue()
            middlename = self.middlename.GetValue() or ""
            if name and surname:
                fullname = " ".join([name.strip(), middlename.strip(), surname.strip()])
                with sqlite3.connect("tasks.db") as conn:
                    cursor = conn.cursor()
                cursor.execute(f"""INSERT INTO Employees(name) values ('{fullname}')""")
                conn.commit()
                for widget in [self.name, self.surname, self.middlename]:
                    widget.SetValue("")
            else:
                wx.MessageBox(
                    "Имя и фамилия являются обязательными полями",
                    "Недопустимое имя",
                    wx.OK | wx.ICON_ERROR,
                )
        except Exception as exc:
            print(exc)

    def on_addTaskConfirmPress(self, event):
        try:
            taskname = self.taskName.GetValue()
            if taskname:
                with sqlite3.connect("tasks.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"""INSERT INTO Tasks(name) values ('{taskname}')""")
                    conn.commit()
                self.taskName.SetValue("")
            else:
                wx.MessageBox(
                    "Название задачи не может быть пустым",
                    "Недопустимое имя задачи",
                    wx.OK | wx.ICON_ERROR,
                )
        except Exception as exc:
            print(exc)


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
