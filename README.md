Sure! Here is a **clean, simple, professional README.md** — **only the README file**, nothing extra.

---

# **README.md**

## 📘 EDUSAGE – AI Academic Content Generator

EDUSAGE is a Streamlit-based application that allows users to upload a PDF and automatically generate high-quality academic materials. The tool is designed for students, teachers, researchers, and professionals who want fast, organized educational content.

---

## 🚀 Features

### **1. Summary Notes**

* Extracts text from uploaded PDFs
* Produces clean academic notes
* Includes short summary, key points, and explanations
* Preview inside the app
* Download as **DOCX**

### **2. PPT Outline Generator**

* Creates slide-wise outline
* Each slide includes title, sub-points & a one-line explanation
* Download as **PPTX**

### **3. Research Analysis**

Generated content includes:

* Short Summary
* Research Objectives
* Methodology
* Key Findings
* Conclusion
* Significance
* Downloadable formats: DOCX / TXT

### **4. Question Bank Generator**

* MCQs with four options
* Correct answers
* Exam-style descriptive questions
* Downloadable formats: DOCX / TXT

### **5. User File Management**

* Each user gets a dedicated folder:

  ```
  user_files/<username>/
  ```
* All generated files (notes, ppt, analysis, question bank) are automatically saved.

### **6. Content Preview**

Each generated output can be viewed in a preview box before downloading.

---

## 🛠️ Technology Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **AI Models:** Gemini / OpenAI / Any LLM API
* **Document Export:** python-docx, python-pptx
* **PDF Extraction:** PyPDF2 / pdfplumber
* **Storage:** Local directory

---

## 📦 Installation

### 1. Clone the repository

```
git clone <repository-url>
cd edusage
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Set API keys

Create a `.env` file:

```
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
```

### 4. Run the application

```
streamlit run app.py
```

---

## 📂 Project Structure

```
edusage/
│── app.py
│── README.md
│── requirements.txt
│── utils/
│   ├── pdf_reader.py
│   ├── generate_notes.py
│   ├── generate_ppt.py
│   ├── generate_research.py
│   ├── generate_questions.py
│   └── file_utils.py
│── user_files/
│   └── <username>/
```

---

## 🧠 How It Works

1. Upload a PDF
2. Text is extracted and cleaned
3. User selects what to generate
4. AI produces output
5. Preview appears inside the app
6. Download file in required format

---

## 📌 Notes

* Preview boxes appear inside content sections (expanders)
* For large content, Streamlit may auto-scroll
* Popup modals are optional and not required

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first.
