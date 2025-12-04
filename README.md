# EduBridge – Multilingual Learning Companion  
*A Fully Offline AI Tutor Built Using Streamlit + Ollama*

EduBridge is a lightweight, offline-first AI learning assistant designed to help students ask academic questions in **English, Telugu, and Hindi**.  
It is built for the GHCI 2025 Hackathon – Round 2.

---

## 🚀 Features
- 🔤 **Multilingual Support** – English, Telugu, Hindi  
- ⚡ **Completely Offline** – Runs locally using Ollama (no internet required)  
- 🤖 **AI Tutor** – Answers academic questions in simple, student-friendly language  
- 🧑‍🏫 **Teacher Dashboard (Demo)** – Allows teachers to write lesson titles & lesson content  
- 🎨 **Clean UI** built using Streamlit  
- 🔧 **Easy to Run** – Only Python + Streamlit + Ollama required  

---

## 🧠 Tech Stack
| Component | Technology |
|----------|-------------|
| Backend AI | Ollama Models (LLaMA 3.1, Gemma, or Qwen depending on language) |
| Frontend UI | Streamlit |
| Language Support | English / Telugu / Hindi |
| Local Execution | 100% offline |

---

## 📌 How It Works
EduBridge connects to `Ollama` running locally on your machine and generates answers through models like:

- `llama3.1:8b` – English  
- `gemma:2b` – Telugu & Hindi  

The app provides:
- A student section to ask doubts  
- A teacher section for lesson creation (demo mode)

---

## 📂 Folder Structure
```
EduBridge/
│
├── app.py
├── venv/               (ignored)
├── .streamlit/         (ignored)
└── README.md
```

---

## ▶️ How to Run Locally

### **Step 1 – Install Ollama**
Download from: https://ollama.com/download  
Then pull models:
```
ollama pull gemma:2b
ollama pull llama3.1:8b
```

### **Step 2 – Create Virtual Environment**
```
python -m venv venv
venv\Scripts\activate
```

### **Step 3 – Install Dependencies**
```
pip install -r requirements.txt
```

### **Step 4 – Start Ollama Service**
```
ollama serve
```

### **Step 5 – Run EduBridge**
```
streamlit run app.py
```

---

## 📽️ Demo Video  
🔗 **Video Link:** https://drive.google.com/file/d/1NIDcZP0V7z5cnBWATn-Cidfz4zbwSp1O/view?usp=drive_link

---

## 💻 Source Code Repository  
🔗 **GitHub Link:** https://github.com/sowmya-palivela/EduBridge

---

## 👥 Team Details
- **Team Name:** CodeForChange  
- **Team Lead:** Satya Sowmya Palivela  
- **Team Members:** Divyasruthi Nagireddy, Shanmukha Srivalli Devika Garaga 
- **Round:** Qualified for Round 2  

---

## 📝 License
This project is created for GHCI Hackathon – educational/demo use only.

---


