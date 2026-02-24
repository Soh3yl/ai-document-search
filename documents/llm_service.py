from langchain_community.llms import FakeListLLM
from langchain.prompts import PromptTemplate

def generate_answer(query, relevant_docs):
    if not relevant_docs:
        return "سند مرتبطی برای پاسخ به این پرسش یافت نشد."

    context_text = "\n\n".join([item['document'].content for item in relevant_docs])

    template = """
    The following information is extracted from the database documents:
    {context}
    
    Based on the information above, please answer the user's question.
    
    Question: {question}
    
    Answer:
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    fake_responses = [
        "پاسخ هوش مصنوعی (تولید شده توسط LangChain FakeLLM): با توجه به اسناد موجود در پایگاه داده، اطلاعات شما با موفقیت پردازش شد. این یک پاسخ شبیه‌سازی شده برای ارزیابی عملکرد زنجیره (Chain) است."
    ]
    
    llm = FakeListLLM(responses=fake_responses)

    chain = prompt | llm
    answer = chain.invoke({"context": context_text, "question": query})
    
    return answer