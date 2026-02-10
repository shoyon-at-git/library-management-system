
import tkinter as tk
from models.issued import issue_book, return_book, get_issued

class IssueFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self,text="Book ID").grid(row=0,column=0)
        tk.Label(self,text="Student ID").grid(row=1,column=0)

        self.b=tk.Entry(self); self.s=tk.Entry(self)
        self.b.grid(row=0,column=1); self.s.grid(row=1,column=1)

        tk.Button(self,text="Issue",command=self.issue).grid(row=2,columnspan=2)

        tk.Label(self,text="Return Issue ID").grid(row=3,column=0)
        self.r=tk.Entry(self)
        self.r.grid(row=3,column=1)
        tk.Button(self,text="Return",command=self.ret).grid(row=4,columnspan=2)

        self.list=tk.Listbox(self,width=50)
        self.list.grid(row=5,columnspan=2)
        self.refresh()

    def issue(self):
        issue_book(int(self.b.get()), int(self.s.get()))
        self.refresh()

    def ret(self):
        return_book(int(self.r.get()))
        self.refresh()

    def refresh(self):
        self.list.delete(0,"end")
        for i in get_issued():
            self.list.insert("end", i)
