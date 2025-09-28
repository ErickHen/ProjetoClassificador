# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from ml_model import classify_email

app = Flask(__name__)
CORS(app)

# Extrai texto de arquivos .txt e .pdf
def extract_text(file):
    if file.filename.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")
    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join(page.extract_text() or "" for page in reader.pages)
    return ""

@app.route("/api/process", methods=["POST"])
def process():
    uploaded_file = request.files.get("file")
    email_text = request.form.get("text", "")

    if uploaded_file:
        email_text = extract_text(uploaded_file)

    if not email_text.strip():
        return jsonify({"error": "Nenhum texto encontrado"}), 400

    category, answer = classify_email(email_text)

    return jsonify({
        "category": category,
        "suggested_answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)
