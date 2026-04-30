from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_knowledge():
    with open("data/scams.txt", "r", encoding="utf-8") as file:
        documents = file.readlines()

    documents = [doc.strip() for doc in documents if doc.strip()]
    return documents


documents = load_knowledge()

vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(documents)


def get_relevant_knowledge(query):
    if not query.strip():
        return ""

    query_vector = vectorizer.transform([query])
    similarity = cosine_similarity(query_vector, doc_vectors)

    top_indexes = similarity[0].argsort()[-3:][::-1]

    relevant_lines = []

    for index in top_indexes:
        relevant_lines.append(documents[index])

    return "\n".join(relevant_lines)