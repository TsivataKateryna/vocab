from flask import Flask, request, send_from_directory
import os
import json

app = Flask(__name__)

WORDS_FILE = "words.txt"

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/add", methods=["POST"])
def add_word():
    try:
        data = request.get_json()
        french = data.get("french", "").strip()
        english = data.get("english", "").strip()

        if not french or not english:
            return "⚠️ Les champs ne doivent pas être vides.", 400

        with open(WORDS_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{french} # {english}")

        return "✅ Mot ajouté !"
    except Exception as e:
        return f"❌ Erreur : {str(e)}", 500

@app.route("/words", methods=["GET"])
def get_words():
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "(aucun mot enregistré)"

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    app.run(debug=True)
