import os
import json
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader, WebBaseLoader
)
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from config.api_key_config import api_key


def get_file_state(root_folder):
    file_state = {}
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                modified_time = os.path.getmtime(filepath)
                file_state[filepath] = modified_time
            except Exception as e:
                print(f"Error reading file time for {filepath}: {e}")
    return file_state


def has_file_changes(root_folder, state_file=".file_state.json"):
    current_state = get_file_state(root_folder)
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            previous_state = json.load(f)
        if current_state != previous_state:
            with open(state_file, "w") as f:
                json.dump(current_state, f)
            return True
        return False
    else:
        with open(state_file, "w") as f:
            json.dump(current_state, f)
        return True


def base_context_creation_and_retrieval_vector_db(
    root_folder=None,
    urls=None,
    persist_directory="rag_db",
    forceRewriteVectorDB=False
):
    all_docs = []
    vector_db = None

    # Create rag_db directory if it don't exist
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    state_file = os.path.join(persist_directory, ".file_state.json")

    chroma_exists = os.path.exists(os.path.join(persist_directory, "chroma.sqlite3"))
    local_changed = has_file_changes(root_folder, state_file) if root_folder else False

    should_rewrite = forceRewriteVectorDB or not chroma_exists or local_changed or urls

    if should_rewrite:
        print("🔄 Rebuilding vector DB due to changes or force flag.")

        # Load local files (if folder provided)
        if root_folder:
            for root, dirs, files in os.walk(root_folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    ext = os.path.splitext(filepath)[1].lower()

                    if ext == ".txt":
                        loader = TextLoader(filepath)
                    elif ext == ".pdf":
                        loader = PyPDFLoader(filepath)
                    elif ext == ".docx":
                        loader = Docx2txtLoader(filepath)
                    elif ext == ".csv":
                        loader = CSVLoader(filepath)
                    else:
                        print(f"Unsupported file type: {filepath}")
                        continue

                    try:
                        docs = loader.load()
                        all_docs.extend(docs)
                    except Exception as e:
                        print(f"❌ Failed to load {filepath}: {e}")

        # Load URLs (if provided)
        if urls:
            for url in urls:
                try:
                    loader = WebBaseLoader(url)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source"] = url
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"❌ Failed to load URL {url}: {e}")

        # Handle empty document case
        if not all_docs:
            print("⚠️ No documents to embed. Skipping vector DB creation.")
            return None

        # Split and embed
        splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        split_docs = splitter.split_documents(all_docs)

        embedding = OpenAIEmbeddings(openai_api_key=api_key)
        vector_db = Chroma.from_documents(split_docs, embedding, persist_directory=persist_directory)
        vector_db.persist()
        print(f"✅ Vector DB updated at '{persist_directory}'")
    else:
        print("✅ Vector DB unchanged. Using existing.")
        embedding = OpenAIEmbeddings(openai_api_key=api_key)
        vector_db = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    return vector_db.as_retriever(search_kwargs={"k": 50})
