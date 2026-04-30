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
- Docker
- Render
- Netlify

## Project Files

- `app.py` – Flask routes and app start point
- `ai_service.py` – AI response and prompt handling
- `image_service.py` – image text extraction using OCR
- `pdf_service.py` – PDF text extraction
- `risk_rules.py` – simple rule-based scam checks
- `rag.py` – retrieves related scam knowledge from `scams.txt`
- `data/scams.txt` – scam awareness knowledge file
- `templates/index.html` – frontend UI for Flask/local use
- `frontend/index.html` – frontend UI for Netlify deployment
- `.env.example` – sample file for API key
- `requirements.txt` – required Python libraries
- `Dockerfile` – Docker setup for Render deployment with Tesseract OCR

## Note

Image analysis works best with clear screenshots containing readable text. Very large or blurry images may take longer or may not be processed properly on free hosting.

For image analysis, Tesseract OCR must be installed on your system.

Default Windows path used in this project:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/rohan17code/ScamLens-AI.git
cd ScamLens-AI
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Run the project:

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

## How It Works

The project takes input from the user and first extracts text from it.

- Message input is directly sent for analysis
- Link input is checked as a URL
- PDF text is extracted using `pypdf`
- Image text is extracted using OCR

After extracting text, the project uses:

- rule-based checks
- RAG knowledge from `data/scams.txt`
- AI model response from Groq

Then it returns:

- Risk Level
- Reason

## Risk Levels

| Risk Level | Meaning |
|---|---|
| Safe | Content looks normal |
| Medium | Content is unclear or slightly suspicious |
| High | Content has strong scam or phishing signs |

## Deployment

The project uses:

- Render for backend deployment
- Docker on Render for installing Tesseract OCR
- Netlify for frontend deployment

The frontend calls the deployed backend API to analyze messages, links, PDFs, and images.

## Disclaimer

This project is made for learning and awareness. It can help detect suspicious content, but it is not a complete cybersecurity or antivirus tool.

## Built By

Built by [Rohan Tyagi](https://www.linkedin.com/in/rohan-tyagi-0b4424270/)