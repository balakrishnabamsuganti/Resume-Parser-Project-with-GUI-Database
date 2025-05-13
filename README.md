
# 📄 Resume Parser Project with GUI & Database

A Python-based application to extract key information (Name, Email, Phone, Skills) from resumes in **PDF or DOCX** format. It features a **Tkinter GUI**, stores data in an **SQLite database**, and allows viewing all parsed resume records.

---

## 📌 Features

- 🗂 Parse resumes in PDF or DOCX format  
- 📤 Upload resumes through a user-friendly GUI  
- 📬 Extract key details: Name, Email, Phone, Skills  
- 💾 Store parsed data into a local SQLite database (`resumes.db`)  
- 👁️ View all saved records using a button in the GUI  
- 🛡 Error handling for missing or corrupted files

---

## 🛠 Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python     | Core programming language |
| Tkinter    | GUI interface |
| PyPDF2     | Read PDF files |
| python-docx | Read DOCX files |
| SQLite3    | Local database to store resume data |
| re         | Regex for extracting structured data |

---

## 📁 Project Structure

```
Resume_Parser_Project/
│
├── resume_parser.py       # Main Python script
├── resumes.db             # SQLite database file (auto-created)
├── README.md              # Project documentation
└── sample_resume.pdf      # (Optional) Resume for testing
```

---

## 🔧 How to Run the Project

### Step 1: Install Dependencies

Run this in your terminal or PyCharm Terminal:

```bash
pip install PyPDF2 python-docx
```

### Step 2: Run the Script

If you're using **PyCharm**:

- Open the project folder
- Open `resume_parser.py`
- Click **Run**

Or use the terminal:

```bash
python resume_parser.py
```

---

## 🖥 GUI Features

- `Select Resume File` – Upload a `.pdf` or `.docx` resume
- `View Database Records` – Display all saved resume data from `resumes.db`
- Scrollable output box to view results

---

## 💡 Example Output

```
Name: veerendra medavarthi
Email: medavarthiveerendra@gmail.com
Phone: +91987654321
Skills: HTML, CSS, Java

----------------------------------------
ID: 1
Name: veerendra medavarthi
Email: medavarthiveerendra@gmail.com
Phone: +91987654321
Skills: Python, Django
----------------------------------------
```

---

## 🐞 Error Handling

- ✔ Invalid resume type or unreadable content: Displayed as a message in the output box
- ✔ SQLite database corruption: Handled gracefully
- ✔ Missing or empty fields: Marked as "Not Found"

---

## 📌 Future Enhancements (Optional Ideas)

- Export parsed data to CSV
- Add resume ranking or matching algorithm
- Integrate with cloud-based resume storage
- Add resume preview in the GUI

---

## 📧 Contact

For any questions or suggestions:  
📬 **Balakrishna Bamsuganti**  
📨 Email: [balakrishnabamsuganti@gmail.com]
