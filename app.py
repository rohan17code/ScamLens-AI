from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from ai_service import analyze_text_with_ai
from pdf_service import extract_text_from_pdf
from image_service import extract_text_from_image


app = Flask(__name__)
CORS(app)


MAX_ANALYSIS_TEXT = 2000


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json

        contact_name = data.get("contact_name", "")
        message = data.get("message", "")

        text = f"Contact Name: {contact_name}\nMessage: {message}"
        text = text[:MAX_ANALYSIS_TEXT]

        result = analyze_text_with_ai(text, "Message")

        return jsonify({"result": result})

    except Exception as e:
        print("MESSAGE ANALYSIS ERROR:", str(e), flush=True)
        return jsonify({
            "result": (
                "Risk Level: Medium\n"
                "Reason: Message analysis failed due to a server issue, so please try again."
            )
        })


@app.route("/analyze-pdf", methods=["POST"])
def analyze_pdf():
    try:
        if "pdf" not in request.files:
            return jsonify({
                "result": (
                    "Risk Level: Medium\n"
                    "Reason: No PDF file was uploaded, so the document risk cannot be checked properly."
                )
            })

        pdf_file = request.files["pdf"]
        pdf_text = extract_text_from_pdf(pdf_file)

        if len(pdf_text.strip()) < 5:
            return jsonify({
                "result": (
                    "Risk Level: Medium\n"
                    "Reason: The PDF text could not be read clearly, so a safer review is needed."
                )
            })

        pdf_text = pdf_text[:MAX_ANALYSIS_TEXT]

        result = analyze_text_with_ai(pdf_text, "PDF")

        return jsonify({"result": result})

    except Exception as e:
        print("PDF ANALYSIS ERROR:", str(e), flush=True)
        return jsonify({
            "result": (
                "Risk Level: Medium\n"
                "Reason: PDF analysis failed due to a server issue, so please try again."
            )
        })


@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    try:
        if "image" not in request.files:
            return jsonify({
                "result": (
                    "Risk Level: Medium\n"
                    "Reason: No image file was uploaded, so the screenshot risk cannot be checked properly."
                )
            })

        image_file = request.files["image"]
        image_text = extract_text_from_image(image_file)

        print("OCR TEXT FROM IMAGE:", flush=True)
        print(image_text, flush=True)

        if len(image_text.strip()) < 3:
            return jsonify({
                "result": (
                    "Risk Level: Medium\n"
                    "Reason: Text could not be clearly read from the image, so upload a clearer screenshot."
                )
            })

        image_text = image_text[:MAX_ANALYSIS_TEXT]

        result = analyze_text_with_ai(image_text, "Image")

        return jsonify({"result": result})

    except Exception as e:
        print("IMAGE ANALYSIS ERROR:", str(e), flush=True)
        return jsonify({
            "result": (
                "Risk Level: Medium\n"
                "Reason: Image analysis failed due to a server issue, so please try again with a clearer or smaller image."
            )
        })


@app.route("/analyze-link", methods=["POST"])
def analyze_link():
    try:
        data = request.json

        link = data.get("link", "")

        if not link.strip():
            return jsonify({
                "result": (
                    "Risk Level: Medium\n"
                    "Reason: No link was provided, so the website risk cannot be checked properly."
                )
            })

        link = link[:MAX_ANALYSIS_TEXT]

        result = analyze_text_with_ai(link, "Link")

        return jsonify({"result": result})

    except Exception as e:
        print("LINK ANALYSIS ERROR:", str(e), flush=True)
        return jsonify({
            "result": (
                "Risk Level: Medium\n"
                "Reason: Link analysis failed due to a server issue, so please try again."
            )
        })


@app.route("/test-ocr")
def test_ocr():
    import pytesseract

    return jsonify({
        "tesseract_path": pytesseract.pytesseract.tesseract_cmd
    })


@app.route("/debug-image", methods=["POST"])
def debug_image():
    try:
        if "image" not in request.files:
            return jsonify({
                "error": "No image file uploaded. Use key name exactly: image"
            })

        from image_service import get_ocr_attempts

        image_file = request.files["image"]
        best_text, attempts = get_ocr_attempts(image_file)

        return jsonify({
            "ocr_text": best_text,
            "length": len(best_text.strip()),
            "attempts": attempts
        })

    except Exception as e:
        print("DEBUG IMAGE ERROR:", str(e), flush=True)
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)