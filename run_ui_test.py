import tkinter as tk
from db import init_db
from main import build_main_ui

init_db()
root = tk.Tk()
root.title('UI Test')
root.geometry('800x600')
try:
    build_main_ui(root, lambda: None, role='admin', student_id=None)
    print('build_main_ui completed')
    # destroy after short delay
    root.update()
    root.destroy()
except Exception as e:
    import traceback
    traceback.print_exc()
    print('Exception:', e)
