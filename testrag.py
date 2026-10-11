from backend.rag import retrieve_context
from backend.mistral_model import generate_answer

print("\nChatbot is running (Ask questions or type 'exit' to quit)\n")

while True:
    question = input("Question : ")

    if question.lower() in ["exit", "quit"]:
        print("Chat ended.")
        break

    context, sources = retrieve_context(question)

    if not context.strip():
        print("Bot: No relevant information found in the documents.\n")
        continue

    answer = generate_answer(context, question)
    print("\nBot:", answer, "\n")

    print("SOURCES:")
    for s in sources:
        print("-", s)
    print("\n")