# app.py

import nltk  # importing nltk so I can split sentences into words
nltk.download('punkt')  # download basic tokenizer just in case
nltk.download('punkt_tab')  # download tab-aware tokenizer too

from flask import Flask, request, jsonify  # flask to run web app
from chatbot_core import get_response  # my function that generates bot replies
from database import log_conversation, init_db  # to save chats in DB

# just making sure nltk tokenizer is available, won't download again if already there
nltk.download("punkt", quiet=True)

app = Flask(__name__)  # creating the flask app
init_db()  # setup DB/table so we can log chats

# --- Home route with a tiny browser chat UI ---
@app.route("/", methods=["GET"])
def home():
    # returning a small HTML page with chat interface
    return """
    <html>
      <head>
        <title>AI Chatbot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          /* basic page and chat container styling */
          body {
            display: flex;
            justify-content: center;  /* center horizontally */
            align-items: center;      /* center vertically */
            height: 100vh;            /* full page height */
            margin: 0;
            background: #f5f5f5;
            font-family: Arial, sans-serif;
          }
          .chat-container {
            width: 400px;
            max-width: 90%;
            height: 500px;
            border: 2px solid #333;
            border-radius: 10px;
            background: white;
            display: flex;
            flex-direction: column;
            padding: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
          }
          #chatbox {
            flex: 1;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 10px;
            overflow-y: auto;
            margin-bottom: 10px;
          }
          #userInput {
            width: 75%;
            padding: 8px;
          }
          button {
            padding: 8px 12px;
            border: none;
            border-radius: 6px;
            background: #007bff;
            color: white;
            cursor: pointer;
          }
          button:hover {
            background: #0056b3;
          }
        </style>
      </head>
      <body>
        <div class="chat-container">
          <h3 style="text-align:center; margin:0 0 10px 0;">AI Chatbot</h3>
          <div id="chatbox">
            <!-- initial bot message -->
            <div><em>Bot:</em> Hi! Ask me about support hours, password reset, refund policy, orders, or contacting support.</div>
          </div>
          <div>
            <input type="text" id="userInput" placeholder="Type your question..." />
            <button onclick="sendMessage()">Send</button>
          </div>
        </div>

        <script>
          // function to add messages to chat window
          function addBubble(sender, text) {
            const chat = document.getElementById("chatbox");
            const div = document.createElement("div");
            div.style.margin = "8px 0";  // add some spacing
            div.innerHTML = "<strong>" + sender + ":</strong> " + text;  // show sender name
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;  // scroll down automatically
          }

          // send user message to backend and get response
          async function sendMessage() {
            const input = document.getElementById("userInput");
            const msg = input.value.trim();  // clean spaces
            if (!msg) return;  // do nothing if empty
            addBubble("You", msg);  // show user message
            input.value = "";  // clear input

            try {
              // call backend API
              const res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: msg})
              });
              const data = await res.json();
              addBubble("Bot", data.response || data.error || "(no reply)");  // show bot reply
            } catch (e) {
              addBubble("Bot", "Network error. Is the server running?");  // handle errors
            }
          }

          // send message when Enter key is pressed
          document.getElementById("userInput").addEventListener("keydown", (e) => {
            if (e.key === "Enter") sendMessage();
          });
        </script>
      </body>
    </html>
    """

# --- JSON API: POST /chat ---
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}  # get json from frontend
    user_message = data.get("message", "").strip()  # extract message
    if not user_message:
        return jsonify({"error": "No message provided"}), 400  # handle empty message

    bot_response = get_response(user_message)  # get reply from bot
    # try to save conversation
    try:
        log_conversation(user_message, bot_response)
    except Exception:
        # don't break API if logging fails
        pass

    return jsonify({"response": bot_response})  # return reply

if __name__ == "__main__":
    # start dev server
    app.run(debug=True)
