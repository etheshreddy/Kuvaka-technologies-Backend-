# Lead Scoring Backend (FastAPI)

A backend service to upload, parse, and score leads from CSV files.  
Built with **FastAPI**, following a clean modular design.

---

## Features
- Upload leads via CSV file  
- Parse and validate CSV data  
- Rule-based scoring pipeline  
- AI-assisted scoring layer (optional)  
- REST API with Swagger UI (`/docs`)  
- Deployment ready (Render, Railway, Vercel, Heroku)  

---

## Setup

### 1. Clone the Repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

### 2. Create Virtual Environment
python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Configure Environment Variables
Create a `.env` file in the project root with:

OPENAI_API_KEY=your_openai_or_openrouter_api_key

### 5. Run the Application
uvicorn app.main:app --reload

Server runs at: http://127.0.0.1:8000

---

## API Endpoints

### 1. Upload Leads (CSV)
**POST** `/leads/upload`  

Upload a CSV file containing leads.

**cURL Example:**
curl -X POST "http://127.0.0.1:8000/leads/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@leads.csv"

**Response Example:**
{
  "message": "50 leads uploaded successfully"
}

---

### 2. Score Leads
**POST** `/score`  

Score all uploaded leads using rule-based and AI logic.

**Response Example:**
{
  "message": "Scored 50 leads successfully"
}

---

### 3. Get Results
**GET** `/results`  

Fetch all scored leads.

**Response Example:**
[
  {
    "name": "John Doe",
    "role": "Marketing Manager",
    "company": "TechSolutions",
    "intent": "High",
    "score": 85,
    "reasoning": "Fits ICP SaaS mid-market and role is decision maker."
  }
]

---

### 4. Health Check
**GET** `/health`  

**Response Example:**
{
  "status": "ok"
}

---

## Rule Logic

Leads are scored based on:  
- CSV data completeness (all required fields present)  
- Role hierarchy (decision-maker vs influencer)  
- Industry match (exact or partial)  
- AI scoring (High / Medium / Low, optional)  

---

## AI Integration

To enable AI scoring:  
1. Add your API key in `.env`:

OPENAI_API_KEY=your_key_here

2. Default provider: OpenRouter with `gpt-3.5-turbo`.
