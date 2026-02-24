from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Document

def find_relevant_documents(user_query, top_n=3):
    """
    این تابع پرسش کاربر را می‌گیرد و N سند مرتبط را با استفاده از TF-IDF برمی‌گرداند.
    """
    all_docs = list(Document.objects.all())
    
    if not all_docs:
        return []

    doc_texts = []
    for doc in all_docs:
        tag_names = " ".join([tag.name for tag in doc.tags.all()])
        
        full_text = f"{doc.title} {doc.content} {tag_names}"
        doc_texts.append(full_text)
    
    doc_texts.append(user_query)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(doc_texts)

    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    related_docs_indices = cosine_similarities.argsort()[:-top_n-1:-1]

    relevant_documents = []
    for index in related_docs_indices:
        if cosine_similarities[index] > 0:
            relevant_documents.append({
                'document': all_docs[index],
                'score': round(cosine_similarities[index], 2) 
            })

    return relevant_documents