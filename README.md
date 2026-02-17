# 🐘 AI-Powered PostgreSQL Chatbot (LangChain + Streamlit + RAG)

An intelligent **SQL Chatbot** that allows users to query a PostgreSQL database using natural language.

This project demonstrates three different approaches:

1. 🔹 Basic LLM → SQL Generator
2. 🔹 Dynamic Few-Shot + RAG (Semantic Example Selection)
3. 🔹 SQL Agent (Tool-Using Agent with local LLM)

Built using:

* LangChain
* Streamlit
* PostgreSQL
* Google Gemini
* HuggingFace Embeddings
* Chroma Vector Store
* Ollama (Local LLM option)

---

## 🚀 Features

* ✅ Natural language to SQL conversion
* ✅ Strict PostgreSQL query generation rules
* ✅ Automatic schema extraction
* ✅ Dynamic Few-Shot learning using semantic similarity
* ✅ RAG-based example retrieval
* ✅ Natural language answer generation
* ✅ SQL safety (SELECT only)
* ✅ Streamlit UI
* ✅ Local LLM support via Ollama

---

# 📂 Project Structure

```
├── basic.py          # Basic NL → SQL chatbot
├── dynamic.py        # RAG + Dynamic Few-Shot chatbot
├── agent toolkit.py  # SQL Agent using Ollama
├── deploy.py         # Upload CSV files to PostgreSQL
├── examples.py       # Few-shot examples for RAG
├── .env              # Environment variables
├── data.csv              # tables' files in csv
└── README.md
```

---

# 🛠️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # windows
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_google_api_key
DB_URL=postgresql://username:password@host:port/database
```

---

# 🗄️ Database Setup

To upload CSV files into PostgreSQL:

```bash
python deploy.py
```

This will:

* Read CSV files
* Create corresponding tables
* Upload data
* Verify upload

---

# 💡 How to Run

## 🔹 1. Basic Version

```bash
streamlit run basic.py
```

Features:

* Static prompt
* Strict SQL formatting rules
* Natural language answer generation

---

## 🔹 2. Dynamic Few-Shot + RAG Version (Recommended)

```bash
streamlit run dynamic.py
```

Features:

* Semantic similarity example selection
* Chroma vector store
* HuggingFace embeddings
* More accurate SQL generation

Architecture:

```
User Question
     ↓
Semantic Similarity Search (Chroma)
     ↓
Few-Shot Prompt Construction
     ↓
LLM → SQL
     ↓
Execute Query
     ↓
LLM → Natural Language Answer
```

---

## 🔹 3. SQL Agent (Tool-Based)

Run:

```bash
python "agent toolkit.py"
```

Uses:

* Ollama local LLM (llama3 / mistral)
* LangChain SQL Agent
* Autonomous tool usage

Make sure Ollama is installed:

```bash
ollama pull llama3
```

---

# 🧠 Technologies Used

* LangChain
* Streamlit
* PostgreSQL
* Google Gemini (gemini-2.5-flash)
* Hugging Face Embeddings
* Chroma Vector Store
* Ollama

---

# 🔒 Security Rules

The system enforces:

* Only `SELECT` queries allowed
* No INSERT / UPDATE / DELETE
* No hallucinated tables
* Schema-restricted generation
* Proper GROUP BY handling
* Automatic LIMIT protection

---

# 📊 Example Questions

* "List all customers"
* "Count total invoices"
* "Top 5 best selling tracks"
* "Total revenue"
* "What are the top 5 best selling products?"

---

# 🏗️ Architecture Comparison

| Version     | Accuracy  | Flexibility | Complexity |
| ----------- | --------- | ----------- | ---------- |
| Basic       | Medium    | Low         | Simple     |
| Dynamic RAG | High      | High        | Medium     |
| Agent       | Very High | Very High   | Advanced   |

---

# 📈 Future Improvements

* Role-based access control
* Query explanation mode
* Query cost estimation
* Caching frequent queries
* Multi-database support
* Chart visualization

---

Focused on:

* Machine Learning
* NLP
* LLM Applications
* AI Systems Engineering
