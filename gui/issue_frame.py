import tkinter as tk
from tkinter import messagebox
from datetime import date

from models.issued import issue_book, return_book, get_issued, pay_fine
from gui.ui_theme import COLORS, page_header, card, form_label, entry, button, treeview, apply_app_theme, metric_chip


class IssueFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS["app_bg"])
        apply_app_theme(self)

        page_header(
            self,
            "🔁 Issue / Return Books",
            "Handle lending, returns, and fine payment from one unified operations screen.",
            "Admin only",
        )

        self._build_top_sections()
        self._build_list_section()
        self.refresh()

    def _build_top_sections(self):
        row = tk.Frame(self, bg=COLORS["app_bg"])
        row.pack(fill="x", padx=20, pady=(0, 14))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        issue_wrap, issue_body = card(
            row,
            "Issue Book to Student",
            "Enter the Book ID and Student ID, then confirm the issue. Logic remains untouched.",
        )
        issue_wrap.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        issue_grid = tk.Frame(issue_body, bg=COLORS["surface"])
        issue_grid.pack(fill="x")
        issue_grid.grid_columnconfigure(0, weight=1)
        issue_grid.grid_columnconfigure(1, weight=1)

        form_label(issue_grid, "Book ID").grid(row=0, column=0, sticky="w", pady=(0, 6))
        form_label(issue_grid, "Student ID").grid(row=0, column=1, sticky="w", padx=(12, 0), pady=(0, 6))
        self.b = entry(issue_grid)
        self.b.grid(row=1, column=0, sticky="ew", ipady=8)
        self.s = entry(issue_grid)
        self.s.grid(row=1, column=1, sticky="ew", padx=(12, 0), ipady=8)
        button(issue_body, "📤 Issue Book", self.issue, "success").pack(anchor="w", pady=(16, 0))

        return_wrap, return_body = card(
            row,
            "Return Book / Pay Fine",
            "Use an existing issue record ID and a return date. Paying fines uses the same record-level workflow as before.",
        )
        return_wrap.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        return_grid = tk.Frame(return_body, bg=COLORS["surface"])
        return_grid.pack(fill="x")
        return_grid.grid_columnconfigure(0, weight=1)
        return_grid.grid_columnconfigure(1, weight=1)

        form_label(return_grid, "Issue Record ID").grid(row=0, column=0, sticky="w", pady=(0, 6))
        form_label(return_grid, "Return Date (YYYY-MM-DD)").grid(row=0, column=1, sticky="w", padx=(12, 0), pady=(0, 6))
        self.r = entry(return_grid)
        self.r.grid(row=1, column=0, sticky="ew", ipady=8)
        self.return_date = entry(return_grid)
        self.return_date.grid(row=1, column=1, sticky="ew", padx=(12, 0), ipady=8)
        self.return_date.insert(0, str(date.today()))

        actions = tk.Frame(return_body, bg=COLORS["surface"])
        actions.pack(fill="x", pady=(16, 0))
        button(actions, "📥 Return Book", self.ret, "danger").pack(side="left", padx=(0, 10))
        button(actions, "💳 Pay Fine", self.pay_fine_dialog, "info").pack(side="left")

    def _build_list_section(self):
        wrap, body = card(
            self,
            "Issued Books Records",
            "Overdue items are highlighted so they stop hiding in plain sight.",
            padx=14,
            pady=14,
        )
        wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        chips = tk.Frame(body, bg=COLORS["surface"])
        chips.pack(fill="x", pady=(0, 12))
        metric_chip(chips, "Today", str(date.today())).pack(side="left", padx=(0, 10))
        metric_chip(chips, "Overdue highlight", "Soft red rows").pack(side="left")

        columns = ("ID", "Book ID", "Student ID", "Issue Date", "Due Date", "Return Date", "Fine Amount")
        table_wrap = tk.Frame(body, bg=COLORS["surface"])
        table_wrap.pack(fill="both", expand=True)

        self.tree = treeview(table_wrap, columns=columns, height=15)
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Book ID", width=90, anchor="center")
        self.tree.column("Student ID", width=120, anchor="center")
        self.tree.column("Issue Date", width=130, anchor="center")
        self.tree.column("Due Date", width=130, anchor="center")
        self.tree.column("Return Date", width=130, anchor="center")
        self.tree.column("Fine Amount", width=120, anchor="center")

        for col in columns:
            self.tree.heading(col, text=col)

        scroll = tk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview, bg=COLORS["surface_alt"])
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.tag_configure("alt", background=COLORS["row_alt"])
        self.tree.tag_configure("overdue", background="#fde8e8", foreground="#9b1c1c")

    def issue(self):
        try:
            b_id = int(self.b.get().strip())
            s_id = self.s.get().strip()
            if b_id <= 0:
                messagebox.showerror("Error", "Book ID must be a positive number")
                return
            if not s_id:
                messagebox.showerror("Error", "Please enter Student ID")
                return

            due_date = issue_book(b_id, s_id)
            self.b.delete(0, tk.END)
            self.s.delete(0, tk.END)
            self.refresh()
            messagebox.showinfo("Success", f"Book issued successfully!\n\nDue date: {due_date}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid IDs")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {str(e)}")

    def ret(self):
        try:
            issue_id = int(self.r.get().strip())
            if issue_id <= 0:
                messagebox.showerror("Error", "Issue ID must be a positive number")
                return

            return_date_str = self.return_date.get().strip()
            try:
                return_date = date.fromisoformat(return_date_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                return

            fine = return_book(issue_id, return_date)
            self.r.delete(0, tk.END)
            self.return_date.delete(0, tk.END)
            self.return_date.insert(0, str(date.today()))
            self.refresh()

            if fine > 0:
                messagebox.showinfo("Success", f"Book returned successfully!\n\nOverdue Fine: BDT {fine}")
            else:
                messagebox.showinfo("Success", "Book returned successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Issue ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def pay_fine_dialog(self):
        try:
            issue_id = int(self.r.get().strip())
            if issue_id <= 0:
                messagebox.showerror("Error", "Issue ID must be a positive number")
                return

            records = get_issued()
            record = None
            for record_item in records:
                if record_item[0] == issue_id:
                    record = record_item
                    break

            if not record:
                messagebox.showerror("Error", f"Issue record #{issue_id} not found")
                return

            fine_amount = record[6]
            if fine_amount > 0:
                result = messagebox.askyesno(
                    "Pay Fine",
                    f"Issue ID: {issue_id}\nFine Amount: BDT {fine_amount}\n\nConfirm payment?",
                )
                if result:
                    pay_fine(issue_id)
                    self.refresh()
                    messagebox.showinfo("Success", f"Fine of BDT {fine_amount} paid successfully!")
            else:
                messagebox.showinfo("Info", "No fine due for this record")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Issue ID")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        today = date.today()
        for index, record in enumerate(get_issued()):
            due_date = record[4]
            return_date = record[5]
            is_overdue = return_date is None and due_date and due_date < today

            if is_overdue:
                tags = ("overdue",)
            elif index % 2:
                tags = ("alt",)
            else:
                tags = ()
            self.tree.insert("", "end", values=record, tags=tags)
