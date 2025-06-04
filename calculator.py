import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
from datetime import datetime

# === Database Setup ===
conn = sqlite3.connect("operations.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operand1 REAL,
        operand2 REAL,
        operator TEXT,
        result REAL,
        timestamp TEXT
    )
''')
conn.commit()

# === Operation Function ===
def calculate(op):
    try:
        a = float(entry1.get())
        b = float(entry2.get())

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = a / b
        else:
            raise ValueError("Unknown operator")

        result_var.set(f"Result: {result}")
        log_operation(a, b, op, result)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
    except ZeroDivisionError as zde:
        messagebox.showerror("Math Error", str(zde))

# === Log Operation to SQLite ===
def log_operation(a, b, op, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO operations (operand1, operand2, operator, result, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (a, b, op, result, timestamp))
    conn.commit()

# === Generate Report using Pandas ===
def generate_report():
    df = pd.read_sql_query("SELECT * FROM operations", conn)
    df.to_csv("report.csv", index=False)
    messagebox.showinfo("Report Generated", "Report saved to report.csv")

# === GUI ===
root = tk.Tk()
root.title("Simple Calculator")

tk.Label(root, text="Operand 1").grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

tk.Label(root, text="Operand 2").grid(row=1, column=0, padx=5, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

# Buttons
tk.Button(root, text="+", width=5, command=lambda: calculate("+")).grid(row=2, column=0)
tk.Button(root, text="-", width=5, command=lambda: calculate("-")).grid(row=2, column=1)
tk.Button(root, text="*", width=5, command=lambda: calculate("*")).grid(row=3, column=0)
tk.Button(root, text="/", width=5, command=lambda: calculate("/")).grid(row=3, column=1)

# Result label
result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, fg="blue").grid(row=4, columnspan=2)

# Report Button
tk.Button(root, text="Generate Report", command=generate_report).grid(row=5, columnspan=2, pady=10)

root.mainloop()
