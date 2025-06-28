from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from config import file_paths
from config.api_key_config import api_key
from lib.rag_util import base_context_creation_and_retrieval_vector_db
from lib import text_file_util
from prompt_engineering import output_format, tone, role


def ask_hr_assistant_ai_agent(query: str) -> str:
    # 1 - Retrieve Base Context Document(s)
    retriever = base_context_creation_and_retrieval_vector_db(file_paths.KNOWLEDGE_BASE_DIRECTORY_PATH)
    docs = retriever.get_relevant_documents(query)
    context_text = "\n".join([doc.page_content for doc in docs])

    # 2 - Prompt Template
    prompt = PromptTemplate(
        input_variables=["query","role","context","tone", "output_format"],
        template=text_file_util.read_text_file(file_paths.PROMPT_TEMPLATE_PATH)
    )

    # 3 - Creating LLMChain
    chain = LLMChain(
        llm=ChatOpenAI(model_name="gpt-4o", openai_api_key=api_key),
        prompt=prompt
    )

    # 4 - Input for the Prompt as dict
    inputs = {
        "query": query,
        "role": role.POLICY_LEGAL_PROFESSIONAL,
        "context": context_text,
        "tone": tone.FORMAL + ", " + tone.POLITE + ", " + tone.THOUGHTFUL,
        "output_format": output_format.HTML
    }

    # 5 - Invoking chain
    result = chain.invoke(inputs)
    response = result["text"]

    print(response)
    return response
