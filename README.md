# 🧠 ChatPDF Backend — FastAPI

Backend API for **ChatPDF**, a question–answering system built around uploaded PDF documents.  
Developed with **FastAPI** and **PostgreSQL**, integrated with **ChromaDB** for vector storage and **transformer models** from Hugging Face.

---

## 🚀 Key Features

- 🔐 **JWT Authentication** (Login, Register, Authorization)
- 📄 **Upload & Manage PDF Documents**
- 🧩 **Extract and Store Vector Embeddings (ChromaDB)**
- 💬 **Chat with Your PDF (Ask Document)**
- 🧠 **LLM Integration** with Sentence Transformers & Mistral
- 🗄️ **SQLAlchemy ORM + Alembic Migrations**
- ⚡ **High-performance** API using FastAPI + Uvicorn

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone git@github.com:robbype/Ask-PDF-Backend.git
cd Ask-PDF-Backend
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a .env file in the project root:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/chatpdf
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
CHROMA_PERSIST_DIR=./chroma
PDF_SAMPLE_PATH=app/uploads
```


## 🗄️ Database Migration

Initialize Alembic (if not yet initialized):
```bash
alembic init alembic
```

Run migration:
```bash
alembic upgrade head
```

## ▶️ Run the Server
```bash
uvicorn app.main:app --reload
```

Server will be available at:
```bash
http://127.0.0.1:8000
```