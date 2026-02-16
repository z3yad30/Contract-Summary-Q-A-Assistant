from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/aurora-alpha",
    temperature=0.1,
    streaming=True,
    api_key="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",  # ← add this
)

print("Sending test message...")

for chunk in llm.stream("Say hello world in Arabic"):
    print(chunk.content, end="", flush=True)