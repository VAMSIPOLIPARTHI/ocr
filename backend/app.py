from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import threading


from services.ocr_service import extract_text, get_ocr
from services.text_match import match_details

# NEW
from services.field_extractor import extract_fields
from services.validator import validate_data
from services.action_engine import trigger_action

app = Flask(__name__)
CORS(app)

print("APP STARTED")

def load_ocr_background():
    try:
        print("Loading OCR in background...")
        get_ocr()
        print("OCR Loaded")
    except Exception as e:
        print("OCR Load Error:", e)

threading.Thread(target=load_ocr_background).start()


@app.route("/", methods=["GET"])
def health():
    return jsonify({"message": "Document Processing API running"})


@app.route("/process-document", methods=["POST"])
def process_document():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        ext = file.filename.rsplit(".", 1)[-1].lower()
        file_bytes = file.read()

        # In-memory extraction
        ocr_text = extract_text(file_bytes, ext)

        # NEW PIPELINE
        data = extract_fields(ocr_text)
        validation = validate_data(data)
        action = trigger_action(data, validation)

        return jsonify({
            "status": "success",
            "ocr_text": ocr_text,
            "data": data,
            "validation": validation,
            "action": action
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# OPTIONAL (OLD KYC)
@app.route("/verify-kyc", methods=["POST"])
def verify_kyc():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        ext = file.filename.rsplit(".", 1)[-1].lower()
        file_bytes = file.read()

        # In-memory extraction
        ocr_text = extract_text(file_bytes, ext)

        result = match_details("", "", "", "", "", ocr_text)

        return jsonify({
            "status": "success",
            "verification": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
