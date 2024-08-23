import openai

with open('cert.txt', 'r', encoding='utf-8') as file:
    keyval = file.read()

OPENAI_API_KEY = keyval

openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"

# 질문 작성하기
query = "텍스트를 이미지로 그려주는 모델에 대해 알려줘."

# 메시지 설정하기
messages = [{
    "role": "system",
    "content": "You are a helpful assistant."
}, {
    "role": "user",
    "content": query
}]


response = openai.ChatCompletion.create(model=model, messages=messages)
answer = response['choices'][0]['message']['content']
print(answer)