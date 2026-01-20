
# 🩺 Doctor Appointment Chat System — Powered by LangGraph, LangChain, and FastAPI

This project is a smart conversational assistant for managing doctor appointments using natural language. Whether a user wants to book, cancel, or reschedule a session, this system understands their request and takes care of the action by updating doctor availability behind the scenes.

It’s built using **LangChain** for the LLM interface, **LangGraph** for handling multi-step logic (like workflows), and **FastAPI** to expose everything through a simple API.

---

## 💡 What This Project Can Do

- ✅ **Book an appointment** with a doctor
- ❌ **Cancel an appointment**
- 🔁 **Reschedule an existing appointment**
- 🔍 **Check doctor or specialist availability**
- 💬 Accepts **user-friendly, conversational input**
- 📅 Works on top of a **CSV-based doctor availability system**

---

## 🔧 Tech Stack

- **LangChain** — For managing language model chains and agents
- **LangGraph** — For creating structured, stateful workflows
- **OpenAI** — To extract intent and useful info from user inputs
- **FastAPI + Uvicorn** — Backend API and web server
- **Pandas** — To work with doctor data in CSV format
- **Pydantic** — For validating API input

---

## 🧠 Behind the Scenes

The core logic lives in a **LangGraph workflow**, where user queries go through a supervisor node to detect the intent (book, cancel, reschedule, or check info). Based on that, the graph directs the request to the appropriate function.

Each tool handles a separate operation — like setting a session or checking if a doctor is available. CSV files get updated accordingly.

---

## 📥 Example Questions It Understands

Here are some real example inputs you can try out:

```python
# Booking a session
question = "I want to set session with doctor john doe on 09-08-2024 13:00"

# Cancelling a session
question = "I want to cancel session with doctor john doe on 09-08-2024 13:00"

# Rescheduling a session
question = "I want to reschedule session with doctor john doe on 09-08-2024 13:00 which was held on 08-08-2024 12:30"

# Checking availability of a doctor
question = "Is Dr. Jane Smith available on 10-08-2024?"

# Checking available doctors of a specific specialization
question = "Are there any pediatric dentists available on 11-08-2024?"
````

Each input is passed as:

```python
inputs = {"question": question, "user_id": 1000041.0}
```

## 📝 Sample doctor\_availability.csv

```csv
doctor_name,specialization,date_slot,is_available,patient_to_attend
john doe,general_dentist,09-08-2024 13:00,True,
jane smith,pediatric_dentist,10-08-2024 11:00,True,
```

Whenever a user books, cancels, or reschedules an appointment, this file gets updated to reflect the change.

---

## ▶️ Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/doctor-appointment-ai.git
cd doctor-appointment-ai
```

2. **Set up a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use .\venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the FastAPI server**

```bash
uvicorn main:app --reload
```

5. **Open your browser**
   Go to `http://localhost:8000/docs` to try the API out with Swagger UI.

---

## 🔍 Try It Out

Paste this into the Swagger UI:

```json
{
  "question": "I want to cancel session with doctor john doe on 09-08-2024 13:00",
  "user_id": 1000041.0
}
```

You'll get a structured response and updated availability in the CSV file.

---

## 🛠️ What's Next?

* Use a proper database (e.g., PostgreSQL) instead of CSV
* Add user login and session tracking
* Build a simple UI with Streamlit or React
* Add email or SMS reminders via Twilio

---

## 👨‍💻 Made by Abhay

I built this project to explore how **LangGraph**, **LangChain**, and **FastAPI** can work together in a practical, real-world use case. It’s a great way to combine conversational AI and stateful workflows — and honestly, it’s been a fun challenge!

If you're into GenAI and want to collab or chat — feel free to reach out!

---


```

---


```

