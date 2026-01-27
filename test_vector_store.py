from services.vector_store import create_vector_store, get_retriever
from config import DOC_PATH

# Test 1 : Créer le vector store
print("=== Création du vector store ===")
create_vector_store(str(DOC_PATH))
print("✅ Vector store créé !\n")

# Test 2 : Tester la recherche
print("=== Test de recherche ===")
retriever = get_retriever(k=3)
if retriever:
    results = retriever.invoke("kubernetes")
    print(f"Nombre de résultats : {len(results)}")
    for i, doc in enumerate(results, 1):
        print(f"\n--- Document {i} ---")
        print(doc.page_content[:200])  # Premiers 200 caractères
    print("\n✅ Recherche réussie !")
else:
    print("❌ Erreur lors de la création du retriever")