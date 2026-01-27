from services.rag_service import ask_question

print("=== Test du système RAG ===\n")

# Test 1
question1 = "Quel est le sujet du stage ?"
print(f"Question: {question1}")
print(f"Réponse: {ask_question(question1)}\n")

# Test 2
question2 = "Quelles technologies sont utilisées ?"
print(f"Question: {question2}")
print(f"Réponse: {ask_question(question2)}\n")

# Test 3 - Question sans réponse dans les docs
question3 = "Quelle est la capitale de la France ?"
print(f"Question: {question3}")
print(f"Réponse: {ask_question(question3)}\n")

# Test 4 - bonus
question4 = "où va se deroule le stage ?"
print(f"Question: {question4}")
print(f"Réponse: {ask_question(question4)}\n")