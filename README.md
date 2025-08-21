# 🤖 AI Customer Support ChatBot



A web-based AI ChatBot built using Python, Flask, and NLP. It handles FAQs, provides customer support answers, logs conversations, and gracefully handles queries it can’t understand.

# 🌟 Features

💬 Web-based chat interface using Flask

📚 Handles common FAQs: support hours, password reset, refund & return policies, orders, profile updates

⚠️ Provides fallback suggestions for unrecognized queries

🗂 Stores all conversations in SQLite database for tracking and analysis

🔧 Easy to extend: add new FAQs or improve responses

# 🖼 Demo Screenshot

|     GUI    | Recommendations  |
|------------|------------------|
| ![GUI Input](gui.png) | ![Recommendations](recommendations.png) |


Sample chat interface with user & bot messages.

# 📂 Project Structure
AI-ChatBot/

│

├── app.py             # Main Flask app and web UI

├── chatbot_core.py    # Bot logic using NLP and FAQ matching

├── database.py        # SQLite DB handler for logging conversations

├── chat_logs.db       # Database file (auto-created)

└── README.md          # Project documentation

# ⚙️ Installation

Clone the repository

[GitHub rep.](https://github.com/Prabhakarrayal), 

           cd AI-ChatBot


Create a virtual environment

    python -m venv venv
    source venv/bin/activate      # Linux/macOS
    venv\Scripts\activate         # Windows


Install dependencies

    pip install flask nltk


Run the app

    python app.py


Open in browser

    Go to: http://127.0.0.1:5000/ and start chatting!

# 🔍 How it Works

Frontend (app.py)

    Provides a browser chat interface

    Sends user messages to backend via POST /chat API

    Displays bot replies dynamically

Bot Logic (chatbot_core.py)

    Normalizes user input: lowercase, remove stopwords, keep meaningful words

    Uses Jaccard similarity to find the closest FAQ match

    Returns fallback message if no FAQ matches

Database Logging (database.py)

    Saves user messages and bot replies with timestamps

    Stores in SQLite database (chat_logs.db)

# ✨ How to Extend

Add new FAQs in FAQ_KB in chatbot_core.py:

    FAQ_KB.append(("new question", "new answer"))


Adjust Jaccard similarity threshold in faq_match() to make the bot more/less strict:

    kb_ans = faq_match(user_message, threshold=0.3)


Update UI text or styling in app.py under <style> or <script>

# 🛠 Technologies Used

Python 3.x

Flask (Web framework)

NLTK (Natural Language Processing)

SQLite (Lightweight database)

HTML/CSS/JS (Frontend chat interface)

# 🚀 Future Improvements

Add ML-based intent recognition for better understanding

Integrate external APIs for real-time data & queries

Deploy on cloud platforms like Heroku, AWS, or Render

Add user authentication and personalized chat history

# 📄 License

MIT License – feel free to use, modify, and share!

## ✍️ Author
**Prabhakar Rayal**  
B.Tech CSE | Graphic Era Hill University  
📍 Rishikesh, Uttarakhand, India  
[GitHub Profile](https://github.com/Prabhakarrayal), 
[LinkedIn Profile](https://in.linkedin.com/in/prabhakar-rayal-6639682)
