from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv

load_dotenv()

persistent_directory = "db/chroma_db"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
db = Chroma(
    embedding_function = embedding_model,
    persist_directory = persistent_directory,
    collection_metadata = {"hnsw:space" : "cosine"}
)

query = "When did microsoft overtake ExxonMobil?"

#retriever = db.as_retriever(search_kwargs={"k":5}) #retrieve top5 chunks with with highest cosine similarity
retriever = db.as_retriever(
    search_type = "similarity_score_threshold",
    search_kwargs = {
        "k" : 5,
        "score_threshold" : 0.3 #returns chunks only with cosine similarity >= 0.3
    }
)

relevant_docs = retriever.invoke(query)

print(f"User query: {query}")

for i,doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")

#combine the query and the relevant_docs retrieved 
combined_prompt = f"""Based on the following documents, answer: {query}

Documents: 
{chr(10).join([f"-{doc.page_content}" for doc in relevant_docs])}

Please provide a clear, helpful answer using only the information from these documents. If you can not find the answer in the documents say "I don't have enough information to answer that question based on the provided documents."

"""

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content=combined_prompt),
]

#invoking the model
result = model.invoke(messages)

print("Full result:")
print(result)
print("Content only:")
print(result.content)