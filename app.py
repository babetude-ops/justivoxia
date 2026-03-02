from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()
    question = data.get("question", "")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Tu es JustiVoxia, un assistant juridique intelligent. Tu réponds uniquement aux questions sur le droit du travail et les démarches visa dans le monde. Réponds en français, de manière claire et simple."},
            {"role": "user", "content": question}
        ]
    )

    reponse = response.choices[0].message.content
    return jsonify({"reponse": reponse})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)