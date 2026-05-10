import os
import sys
import time

try:
    import google.generativeai as genai
except ImportError:
    print("Error: The 'google-generativeai' library is not installed. Please install it using 'pip install -r requirements.txt'")
    sys.exit(1)

# Default system prompt provided by the service provider
SYSTEM_PROMPT = """You are a customer service chatbot for an e-commerce website. Please communicate in a casual Saudi Arabic dialect. Your primary role is to assist human customers with tracking their orders (checking if shipped or not), answering product inquiries (describing product features and differences), and providing helpful product recommendations.
When you don't know an answer, respond politely and guide the customer to contact human support via WhatsApp at {whatsapp_number}. Do not create information. Maintain a friendly, human-like persona, acting as a helpful customer service representative."""

class SaudiEcommerceChatbot:
    def __init__(self, api_key=None, whatsapp_number="[Insert WhatsApp Number Here]", model_name="gemini-1.5-flash", max_concurrent_users=15):
        """
        Initialize the Chatbot Manager.

        :param api_key: Gemini API key. If not provided, it will look for the GEMINI_API_KEY environment variable.
        :param whatsapp_number: The WhatsApp number to provide to users when human support is needed.
        :param model_name: The Gemini model to use. Default is gemini-1.5-flash.
        :param max_concurrent_users: Maximum number of simultaneous users.
        """
        self.api_key = api_key or os.environ.get("AIzaSyBMO3krmKETKrpiRSyED85rEvzMnmeO1Lo")
        if not self.api_key:
            raise ValueError("Gemini API key must be provided either via the api_key parameter or the GEMINI_API_KEY environment variable.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
            
        self.whatsapp_number = whatsapp_number
        self.model_name = model_name
        self.max_concurrent_users = max_concurrent_users
        
        formatted_system_prompt = SYSTEM_PROMPT.format(whatsapp_number=self.whatsapp_number)
        
        # Initialize the model with the system instruction
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=formatted_system_prompt
        )
        
        # Dictionary to keep track of active user chat sessions
        self.active_sessions = {}
        # Keep track of last interaction time to clean up inactive sessions
        self.session_last_active = {}

    def _cleanup_inactive_sessions(self, timeout_seconds=3600):
        """Cleans up sessions that haven't been active for a while (default 1 hour)."""
        current_time = time.time()
        expired_users = [user_id for user_id, last_active in self.session_last_active.items() 
                         if current_time - last_active > timeout_seconds]
        for user_id in expired_users:
            self.end_session(user_id)

    def end_session(self, user_id):
        """Ends the session for a given user to free up capacity."""
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
        if user_id in self.session_last_active:
            del self.session_last_active[user_id]

    def reset_conversation(self, user_id):
        """Resets the conversation history for a specific user."""
        if user_id in self.active_sessions:
            self.active_sessions[user_id] = self.model.start_chat()
            self.session_last_active[user_id] = time.time()

    def chat(self, user_id, user_message):
        """
        Sends a message to the chatbot for a specific user and returns its response.
        If the maximum number of concurrent users is reached, returns a busy message.

        :param user_id: A unique identifier for the user (e.g., session ID, phone number).
        :param user_message: The message from the user.
        :return: The chatbot's response string.
        """
        # Periodic cleanup of inactive sessions to free up slots
        self._cleanup_inactive_sessions()

        if user_id not in self.active_sessions:
            if len(self.active_sessions) >= self.max_concurrent_users:
                # Casual Saudi Arabic dialect busy message
                return "المعذرة، فريقنا مشغول حالياً، ثواني وبنكون معاك، شكراً لانتظارك."
            else:
                # Start a new chat session for this user
                self.active_sessions[user_id] = self.model.start_chat()
        
        # Update last active time
        self.session_last_active[user_id] = time.time()
        chat_session = self.active_sessions[user_id]

        try:
            response = chat_session.send_message(user_message)
            return response.text

        except Exception as e:
            error_msg = f"حدث خطأ (An error occurred): {str(e)}"
            return error_msg

def main():
    print("=== Saudi E-commerce Chatbot CLI (Gemini Edition) ===")
    print("This is a standalone test script for the chatbot.")
    print("Press Ctrl+C or type 'exit' or 'quit' to stop.")
    print("-" * 35)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY environment variable is not set.")
        print("Please set it to your Gemini API key to test the chatbot.")
        print("Example: export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)

    whatsapp_num = input("Enter the customer support WhatsApp number (or press Enter to use default '[Insert WhatsApp Number Here]'): ").strip()
    if not whatsapp_num:
        whatsapp_num = "[Insert WhatsApp Number Here]"

    try:
        # Initializing with the default of 15 max concurrent users
        chatbot = SaudiEcommerceChatbot(api_key=api_key, whatsapp_number=whatsapp_num, max_concurrent_users=15)
        print("\\nChatbot initialized! Start chatting:")
        print("------------------------------------\\n")
        
        # Using a dummy user_id for the CLI tester
        my_user_id = "cli_tester_1"

        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                if not user_input.strip():
                    continue
                
                print("Bot is typing...")
                response = chatbot.chat(my_user_id, user_input)
                print(f"Bot: {response}\\n")
            
            except KeyboardInterrupt:
                print("\\nGoodbye!")
                break

    except Exception as e:
        print(f"Failed to initialize chatbot: {e}")

if __name__ == "__main__":
    main()
