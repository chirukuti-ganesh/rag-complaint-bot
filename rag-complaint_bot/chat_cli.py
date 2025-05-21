from chatbot.bot import get_rag_chain
import requests
import re

# Initialize RAG chain
qa_chain = get_rag_chain()
API = "http://localhost:8000"

def chat():
    print("🤖 Welcome to the Complaint Chatbot Assistant!")
    print("Type your question, or use the following commands:")
    print(" - `file`                 : File a new complaint")
    print(" - `fetch <complaint_id>` : Retrieve a complaint by ID")
    print(" - `exit`                 : Exit the chatbot\n")

    while True:
        # user = (input("You: ") + ' no preamble').strip()
        # if user.lower() == "exit" or user.lower()=='exit not preamble':
        user= input("You: ").strip()
        if user.lower() == "exit":
            print("Bot: bye!")
            break

        # Automatically detect 8-character complaint ID (uppercase letters and digits)
        elif re.fullmatch(r"[A-Z0-9]{8}", user.upper()):
            comp_id = user.upper()
            try:
                res = requests.get(f"{API}/complaints/{comp_id}")
                if res.status_code == 200:
                    print("Bot:", res.json())
                else:
                    print(f"Bot:  Complaint not found. Status: {res.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Bot:  Failed to connect to server. Error: {e}")

        elif user.lower().startswith("fetch"):
            parts = user.split(" ")
            if len(parts) < 2:
                print("Bot: Please provide a complaint ID. Usage: fetch <complaint_id>")
                continue
            comp_id = parts[1].strip().upper()
            try:
                res = requests.get(f"{API}/complaints/{comp_id}")
                if res.status_code == 200:
                    print("Bot:", res.json())
                else:
                    print(f"Bot:  Complaint not found. Status: {res.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Bot:  Failed to connect to server. Error: {e}")

        elif (
            user.lower() == "file"
            or "register a complaint" in user.lower()
            or "new complaint" in user.lower()
            or "raise a complaint" in user.lower()
            or "log a complaint" in user.lower()
        ):
            try:
                name = input("Name: ")
                phone = input("Phone: ")
                email = input("Email: ")
                details = input("Complaint: ")
                payload = {
                    "name": name,
                    "phone_number": phone,
                    "email": email,
                    "complaint_details": details
                }
                res = requests.post(f"{API}/complaints", json=payload)
                if res.status_code == 200:
                    print("Bot: ", res.json())
                else:
                    print("Bot:  Failed to file complaint.", res.text)
            except requests.exceptions.RequestException as e:
                print(f"Bot:  Error communicating with backend. {e}")

        # else:
        #     try:
        #         # Use `.invoke()` instead of deprecated `.run()`
        #         # response = qa_chain.invoke({"input": user})
        #         response = qa_chain.invoke({"query": user})

        #         print("Bot:", response)
        #     except Exception as e:
        #         print(f"Bot:  Error from RAG assistant. {e}")
        else:
            try:
                response = qa_chain.invoke({"query": user})
                # Only print the result part if it's a dict with "result"
                if isinstance(response, dict) and "result" in response:
                    print("Bot:", response["result"])
                else:
                    print("Bot:", response)
            except Exception as e:
                print(f"Bot:  Error from RAG assistant. {e}")

if __name__ == "__main__":
    chat()
