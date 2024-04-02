from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = ChatOpenAI(openai_api_key="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")

prompt = ChatPromptTemplate.from_messages([
        ("system", '''You are a Daegu travel recommendation expert 
            with the name “가볼까?”
            You must always give the answer in Korean. 
            Just tell me two suitable travel destinations.
            1. Travel destination 1
            2. Travel destination 2
            Just tell me about Travel destination and don’t say anything like 'have a nice trip'
            Just say this, don’t say unnecessary things.
            you don’t have to say goodbye at the end.
            '''),
        ("user", "{input}")
    ])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

# result = chain.invoke({"input": user_input})
# print(result)

