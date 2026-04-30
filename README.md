# ScamLens AI

ScamLens AI is an AI-based scam and risk detection project. It can check messages, links, PDFs, and screenshots to find whether the content looks safe, suspicious, or risky.

I made this project to detect common online scam patterns like OTP fraud, fake reward messages, phishing links, suspicious PDFs, and scam screenshots.

## Features

- Analyze text messages
- Analyze suspicious links
- Upload and analyze PDF files
- Upload and analyze images/screenshots using OCR
- Uses AI to classify risk level
- Uses RAG with a small scam knowledge file
- Shows result as Safe, Medium, or High risk
- Color glow effect based on risk level

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Groq API
- LLaMA model
- RAG
- scikit-learn
- TF-IDF
- Cosine similarity
- pypdf
- pytesseract
- Tesseract OCR
- Pillow
- python-dotenv

## Project Files

- `app.py` – Flask routes and app start point
- `ai_service.py` – AI response and prompt handling
- `image_service.py` – image text extraction using OCR
- `pdf_service.py` – PDF text extraction
- `risk_rules.py` – simple rule-based scam checks
- `rag.py` – retrieves related scam knowledge from `scams.txt`
- `data/scams.txt` – scam awareness knowledge file
- `templates/index.html` – frontend UI
- `.env.example` – sample file for API key
- `requirements.txt` – required Python libraries

## How to Run

Clone the repository:

```bash
git clone https://github.com/rohan17code/ScamLens-AI.git
cd ScamLens-AI