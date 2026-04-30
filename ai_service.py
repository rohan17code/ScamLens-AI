import os
from groq import Groq
from dotenv import load_dotenv

from risk_rules import rule_based_check
from rag import get_relevant_knowledge


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def clean_ai_output(output):
    lines = output.splitlines()

    risk_line = ""
    reason_line = ""

    for line in lines:
        line = line.strip()

        if line.lower().startswith("risk level:"):
            risk_line = line

        if line.lower().startswith("reason:"):
            reason_line = line

    if risk_line and reason_line:
        return risk_line + "\n" + reason_line

    return output.strip()


def analyze_text_with_ai(text, title="Unknown"):
    rule_result = rule_based_check(text)

    if rule_result:
        return rule_result

    relevant_knowledge = get_relevant_knowledge(text)

    prompt = f"""
You are a general scam and document risk detection API.

Return exactly 2 lines only.
No paragraph.
No extra text.

Content Source: {title}

Relevant scam knowledge from RAG:
{relevant_knowledge}

Content to analyze:
{text}

Classify the content generally:

Safe:
- normal document
- resume
- academic result
- certificate
- invoice
- portfolio
- notes
- normal conversation
- document with normal links only

Medium:
- unclear document
- unknown link without clear scam request
- suspicious wording but no direct demand
- text is confusing or incomplete

High:
- asks for OTP, password, PIN, CVV, bank details
- asks for money or payment
- asks user to click a link to claim prize, reward, gift, lottery, or account unlock
- creates urgency and asks for sensitive action

Important:
- Use the RAG knowledge only if it is relevant to the content.
- Do not force scam classification just because RAG mentions scam examples.
- Do not mark a PDF risky only because it contains a link.
- Do not mark a resume risky because it has GitHub, LinkedIn, email, phone number, or portfolio links.
- Base the result on the actual content.
- If content is unreadable or random characters, classify as Medium.
- The Reason must be one complete sentence with at least 10 words.

Output format:
Risk Level: (Safe / Medium / High)
Reason: (one complete sentence explaining the main reason in at least 10 words)
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Return exactly 2 lines only. The Reason must be one complete sentence of at least 10 words."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return clean_ai_output(result)