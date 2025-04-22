from langchain_community.chat_models import ChatOpenAI

def load_model(model):
    MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
    
    return ChatOpenAI(
        model_name=MODEL_NAME,
        openai_api_base="http://10.3.0.96:8888/v1",
        openai_api_key="not-needed-for-vllm",  # <--- this is the fix
        temperature=0.5,
        max_tokens=1024
    )

def test_model():
    llm = load_model("deepseek-ai/DeepSeek-R1-Distill-Qwen-14B")
    
    # Using .invoke() with a message dictionary
    response = llm.invoke([
        {"role": "user", "content": "What is the capital of France?"}
    ])
    
    print("Model response:", response.content)

    # Basic checks
    assert response is not None, "The model did not return a response."
    assert "Paris" in response.content, "The model did not return the expected answer."

    print("✅ Test passed: The model returned the expected answer.")

if __name__ == "__main__":
    test_model()
