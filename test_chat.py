
from app.services.chat import ask_question

question = "How do I troubleshoot my VPN connection?"

answer = ask_question(question)

print("\nRetail AI Assistant:")
print(answer)
