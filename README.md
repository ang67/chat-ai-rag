# Home Notebook LLM - Documentation Backend

## 📚 Vue d'ensemble

Application de chat RAG (Retrieval Augmented Generation) avec backend Python et frontend React.

Le backend permet d'interroger des documents PDF locaux en utilisant :
- **Ollama** (LLM local - llama3)
- **LangChain** (orchestration RAG)
- **ChromaDB** (base de données vectorielle)
- **Flask** (API REST)

---

## 🏗️ Architecture Backend

```
Frontend React (port 5173)
    ↓ HTTP POST /chat/ask
Flask API (port 5000)
    ↓
RAG Service (LangChain)
    ↓
├─ Retriever → ChromaDB (Vector Store)
│               ↓
│           Embeddings (nomic-embed-text)
│               ↓
│           Documents pertinents
└─ LLM (llama3 via Ollama)
    ↓
Réponse JSON
```
---

## 🔧 Configuration

### Fichier `.env`

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
EMBEDDING_MODEL=nomic-embed-text
DOC_PATH=../data/docs/
CHROMADB_PATH=./chroma_db
FLASK_PORT=5000
```

### Prérequis Ollama

Les modèles suivants doivent être installés :

```bash
# Modèle LLM pour la génération
ollama pull llama3

# Modèle d'embedding pour la vectorisation
ollama pull nomic-embed-text
```

---

## 📦 Installation

### 1. Environnement virtuel

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 2. Dépendances

```bash
pip install -r requirements.txt
```

**Packages principaux :**
- `flask` (3.0.0) - API REST
- `flask-cors` - Support CORS
- `langchain` - Orchestration RAG
- `langchain-ollama` - Intégration Ollama
- `langchain-community` - Loaders et vector stores
- `chromadb` - Base de données vectorielle

### 3. Indexation des documents

Placer les PDFs dans `/data/docs/` puis créer le vector store :

```bash
python test_vector_store.py
```

Cela va :
1. Charger tous les PDFs du dossier
2. Découper en chunks (1000 tokens, overlap 200)
3. Créer les embeddings avec `nomic-embed-text`
4. Stocker dans ChromaDB (`chroma_db/`)

---

## 🚀 Lancement

### Backend

```bash
cd backend
source .venv/bin/activate
python app.py
```

Le serveur démarre sur `http://127.0.0.1:5000`

**Note :** Utiliser `127.0.0.1` au lieu de `localhost` (problème résolution DNS macOS/Chrome)

### Vérification

```bash
# Test route santé
curl http://127.0.0.1:5000/

# Test RAG
curl -X POST http://127.0.0.1:5000/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Quel est le sujet du stage ?"}'
```

---

## 🔍 Composants Détaillés

### 1. Document Loader (`utils/document_loader.py`)

**Fonctions :**
- `load_documents(directory_path)` : Charge les PDFs avec `PyPDFLoader`
- `split_documents(documents, chunk_size=1000, chunk_overlap=200)` : Découpe en chunks

**Pourquoi le chunking ?**
- Optimise la recherche de similarité
- Évite de surcharger le contexte du LLM
- Permet de récupérer uniquement les passages pertinents

### 2. Vector Store (`services/vector_store.py`)

**Fonctions :**
- `create_vector_store(documents_path)` : Crée le vector store initial
- `load_vector_store()` : Charge le vector store existant
- `get_retriever(k=5)` : Retourne un retriever pour chercher les k documents les plus pertinents

**Technologie :**
- ChromaDB : stockage des vecteurs + index de similarité
- Embeddings : `nomic-embed-text` via Ollama
- Distance : cosinus (par défaut)

### 3. RAG Service (`services/rag_service.py`)

**Pipeline LangChain (LCEL) :**

```python
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)
```

**Flux :**
1. **Question** → Retriever récupère les k documents pertinents
2. **format_docs** → Convertit les Documents en texte
3. **Prompt Template** → Structure la requête (contexte + question + instructions)
4. **LLM** (llama3) → Génère la réponse basée sur le contexte
5. **StrOutputParser** → Extrait le texte brut

**Prompt Template :**
```
Tu es un assistant qui répond aux questions basées sur un contexte fourni.

Contexte: {context}

Question: {question}

Réponds uniquement en te basant sur le contexte fourni. 
Si tu ne trouves pas la réponse dans le contexte, 
dis "Je ne trouve pas cette information dans les documents fournis."
```

### 4. API Flask (`routes/chat.py`)

**Endpoint :** `POST /chat/ask`

**Request :**
```json
{
  "question": "Quelle est la durée du stage ?"
}
```

**Response :**
```json
{
  "answer": "La durée du stage est de 6 mois."
}
```

**Validation :**
- Vérifie la présence de `question`
- Vérifie que la question n'est pas vide
- Gestion d'erreurs avec codes HTTP appropriés (400, 500)

---

## 🧪 Tests

### Test du Vector Store

```bash
python test_vector_store.py
```

Teste :
- Chargement des documents
- Création du vector store
- Recherche de similarité

### Test du RAG complet

```bash
python test_rag.py
```

Teste :
- Questions avec réponses dans les docs
- Questions sans réponse (vérifie l'absence d'hallucinations)
- Performance de génération

---

## 🔄 Workflow RAG

### Indexation (une fois au démarrage)

```
Documents PDFs
    ↓ PyPDFLoader
Texte brut
    ↓ RecursiveCharacterTextSplitter
Chunks (1000 tokens, overlap 200)
    ↓ OllamaEmbeddings (nomic-embed-text)
Vecteurs (embeddings)
    ↓
ChromaDB (persisté sur disque)
```

### Requête (à chaque question)

```
Question utilisateur
    ↓ OllamaEmbeddings (nomic-embed-text)
Vecteur question
    ↓ Recherche similarité (ChromaDB)
Top-k documents pertinents (k=5)
    ↓ format_docs (concaténation)
Contexte textuel
    ↓ Prompt Template
Requête structurée (question + contexte + instructions)
    ↓ ChatOllama (llama3)
Réponse générée
    ↓ StrOutputParser
Texte brut → JSON
```

---

## ⚙️ Paramètres Configurables

### Chunking
- `chunk_size` : 1000 tokens (ajustable dans `document_loader.py`)
- `chunk_overlap` : 200 tokens (évite de couper les informations)

### Retrieval
- `k` : 5 documents retournés (ajustable dans `get_retriever(k=5)`)
- `search_type` : similarité (par défaut dans ChromaDB)

### LLM
- Modèle : `llama3` (configurable dans `.env`)
- Température : défaut Ollama (~0.8)
- Context window : 8k tokens (llama3)

---

## 📝 Notes Importantes

### Ajout de nouveaux documents

Lorsque de nouveaux PDFs sont ajoutés dans `/data/docs/` :

```bash
# Supprimer l'ancien vector store
rm -rf chroma_db/

# Recréer avec tous les documents
python test_vector_store.py
```

**Pourquoi ?** Les embeddings sont créés une seule fois lors de l'indexation.

### Utilisation des embeddings

Le modèle d'embedding (`nomic-embed-text`) est utilisé **2 fois** :
1. **Indexation** : transformer les documents en vecteurs
2. **Requête** : transformer la question en vecteur

**Crucial :** Le même modèle doit être utilisé pour garantir que les vecteurs sont comparables (même espace vectoriel).

### Performance

- **Première requête** : ~15-30s (chargement modèles Ollama)
- **Requêtes suivantes** : ~5-10s (modèles en cache)
- **Indexation** : dépend du nombre de documents (~1-2 min pour 10 PDFs)

### Limitations

- **Context window** : llama3 = 8k tokens (limité par la taille des chunks + question)
- **Stockage** : ChromaDB persiste sur disque (peut devenir lourd avec beaucoup de docs)
- **Langue** : Prompt en français, mais fonctionne mieux avec documents anglais

---

## 🐛 Troubleshooting

### Ollama ne répond pas
```bash
# Vérifier qu'Ollama tourne
ollama list

# Si nécessaire, démarrer manuellement
ollama serve
```

---

## 🚀 Améliorations Futures

- [ ] Streaming des réponses (SSE)
- [ ] Historique de conversation
- [ ] Support multi-format (Markdown, DOCX, TXT)
- [ ] Interface d'administration des documents
- [ ] Métriques de performance (temps de réponse, pertinence)
- [ ] Authentification/autorisation
- [ ] Déploiement production (Gunicorn, Docker)

---

## 📖 Ressources

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama](https://ollama.ai/)
- [ChromaDB](https://www.trychroma.com/)
- [Flask](https://flask.palletsprojects.com/)
