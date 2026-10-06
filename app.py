import os 
from flask import Flask,request,jsonify
from dotenv import load_dotenv
from llm import ask_llm

load_dotenv()

app=Flask(__name__)

@app.route("/")
def home():
    return{
        "message":"Tool calling API is running"
    }

@app.route("/chat",methods=["POST"])
def chat():
    data=request.get_json(
    )

    if not data:
        return jsonify({"error":"Request body is required"}),400
    message=data.get("message")

    if not message:
        return jsonify({
            "error":"message is required"
        })
    try:
        answer=ask_llm(message)
        return jsonify({"answer":answer})
    except Exception as e:
        print("ERROR:",e)
        return jsonify({
            "error":str(e)
        }),500


# Terminal chat function
def terminal_chat():

    print("\n================================")
    print("       AI TOOL-CALLING CHAT")
    print("================================")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:

        # Get input from the user
        user_message = input("You: ").strip()

        # Stop the loop if the user wants to exit
        if user_message.lower() in ["exit", "quit"]:
            print("AI: Goodbye!")
            break

        # Prevent empty messages
        if not user_message:
            print("AI: Please enter a message.")
            continue

        try:
            # Send the message to the LLM
            response = ask_llm(user_message)

            # Display the response
            print(f"\nAI: {response}\n")

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":

    # Run the terminal chat
    terminal_chat()