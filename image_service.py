import os
import pytesseract
from PIL import Image, ImageOps, ImageFilter


# Windows local system
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Render/Linux server
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def resize_image(image, max_width=900):
    width, height = image.size

    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        image = image.resize((max_width, new_height))

    return image


def clean_ocr_text(text):
    text = text.replace("|", "")
    text = text.replace("‘", "'")
    text = text.replace("’", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text.strip()


def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = resize_image(image)

    gray = image.convert("L")
    gray = ImageOps.autocontrast(gray)

    sharp = gray.filter(ImageFilter.SHARPEN)

    inverted = ImageOps.invert(gray)
    inverted = ImageOps.autocontrast(inverted)

    attempts = [
        ("gray", gray),
        ("sharp", sharp),
        ("inverted", inverted)
    ]

    best_text = ""

    important_words = [
        "lottery", "winner", "won", "prize", "claim",
        "congratulations", "reward", "giveaway",
        "otp", "password", "bank", "payment", "click",
        "link", "http", "www",
        "student", "result", "semester", "marks",
        "grade", "sgpa", "cgpa", "institute", "university"
    ]

    print("TESSERACT PATH:", pytesseract.pytesseract.tesseract_cmd, flush=True)

    for name, img in attempts:
        try:
            text = pytesseract.image_to_string(
                img,
                config="--oem 3 --psm 6",
                timeout=6
            )

            text = clean_ocr_text(text)

            print("OCR attempt:", name, flush=True)
            print(text, flush=True)

            if len(text) > len(best_text):
                best_text = text

            lower_text = best_text.lower()

            if len(best_text.strip()) > 25:
                if any(word in lower_text for word in important_words):
                    return best_text

        except Exception as e:
            print("OCR failed:", name, str(e), flush=True)

    return best_text