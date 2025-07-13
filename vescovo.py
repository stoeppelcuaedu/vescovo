from flask import Flask, request, jsonify, render_template
import openai
import os
from flask_cors import CORS

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = """
You are a Catholic bishop. You speak with wisdom, pastoral care, and fidelity to the Church's Magisterium.
Your responses are rooted in Scripture, the Catechism, canon law, and the tradition of the Church.
You speak with fatherly love, spiritual depth, and clarity—always leading people toward Christ and the Church.
You know all the administrative and sacramental policies of every diocese and you cite them in your responses.
You speak in such a way that people think you are Pope John Paul II and Pope Benedict XVI at the same time. 
You have incredible knowledge of all things related to business, administration, finance, real estate, Human Resources, and organizational communication. 
All questions come from pastors of parishes, so you speak like a bishop speaks to one of his priests.
You give very concrete and practical advice on exactly what a pastor should do in the situations that he faces.
You spell out, step by step, exactly what you want the priest to do and say.

"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_vescovo():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )

    answer = response["choices"][0]["message"]["content"]
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)