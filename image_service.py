import pytesseract
from PIL import Image, ImageOps, ImageFilter


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")

    attempts = []

    attempts.append(image)

    gray = image.convert("L")
    attempts.append(gray)

    big = gray.resize((gray.width * 3, gray.height * 3))
    attempts.append(big)

    contrast = ImageOps.autocontrast(big)
    attempts.append(contrast)

    sharp = contrast.filter(ImageFilter.SHARPEN)
    attempts.append(sharp)

    inverted = ImageOps.invert(gray)
    inverted_big = inverted.resize((inverted.width * 3, inverted.height * 3))
    attempts.append(inverted_big)

    configs = ["--psm 6", "--psm 11", "--psm 12"]

    best_text = ""

    for img in attempts:
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config)

                if len(text.strip()) > len(best_text.strip()):
                    best_text = text

            except Exception:
                pass

    return best_text