import tkinter as tk
from tkinter import filedialog, scrolledtext
from docx import Document
import PyPDF2
import re
import os
import sqlite3

# ------------------ Database Functions ------------------

def create_database():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT
        )
    """)
    conn.commit()
    conn.close()

def view_all_records():
    try:
        conn = sqlite3.connect("resumes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resumes")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.DatabaseError:
        return []


def save_to_database(name, email, phone, skills):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resumes (name, email, phone, skills)
        VALUES (?, ?, ?, ?)
    """, (name, email, phone, ", ".join(skills)))
    conn.commit()
    conn.close()

# ------------------ Resume Parsing Functions ------------------

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-()]{7,}\d', text)
    return match.group() if match else None

def extract_skills(text, skill_set):
    return [skill for skill in skill_set if skill.lower() in text.lower()]

def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines[:5]:
        if len(line.split()) >= 2 and all(word[0].isupper() for word in line.split()[:2]):
            return line.strip()
    return "Name not confidently detected"

def parse_resume(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        return "Unsupported file format."

    common_skills = ['Python', 'Java', 'C++', 'Django', 'Flask', 'HTML', 'CSS', 'JavaScript', 'SQL', 'Git']

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text, common_skills)

    # Save to database
    create_database()
    save_to_database(name, email, phone, skills)

    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Skills": skills
    }

# ------------------ GUI Setup ------------------

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Resumes", "*.pdf *.docx")])
    if file_path:
        result = parse_resume(file_path)
        display_result(result)

def display_result(result):
    output_text.delete(1.0, tk.END)
    if isinstance(result, dict):
        for key, value in result.items():
            output_text.insert(tk.END, f"{key}: {value}\n")
    else:
        output_text.insert(tk.END, result)

def display_all_records():
    records = view_all_records()
    output_text.delete(1.0, tk.END)

    if not records:
        output_text.insert(tk.END, "No records found in database.\n")
        return

    for record in records:
        output_text.insert(tk.END, f"ID: {record[0]}\nName: {record[1]}\nEmail: {record[2]}\nPhone: {record[3]}\nSkills: {record[4]}\n{'-'*40}\n")

# ------------------ Main App Window ------------------

app = tk.Tk()
app.title("Resume Parser with Database")
app.geometry("550x500")

tk.Label(app, text="Resume Parser", font=("Arial", 16)).pack(pady=10)

# Resume upload button
tk.Button(app, text="Select Resume File", command=browse_file, font=("Arial", 12)).pack(pady=5)

# View DB records button
tk.Button(app, text="View Database Records", command=display_all_records, font=("Arial", 12)).pack(pady=5)

# Scrollable output text area
output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=65, height=20, font=("Arial", 10))
output_text.pack(padx=10, pady=10)

# Start GUI loop
app.mainloop()
