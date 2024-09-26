from transformers import AutoTokenizer, AutoModel
import torch

# KoBERT 모델과 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained("skt/kobert-base-v1")
model = AutoModel.from_pretrained("skt/kobert-base-v1")

# 입력 문장 (한국어 텍스트)
sentence = "극적으로 살아난 마크는 화성 탐사 기지에 남은 식량과 식물학자로서의 지식을 활용하여 생존기를 시작하고, NASA에 전달한다."

# 토크나이저로 문장 토큰화
inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)

# BERT 모델을 통해 문장의 임베딩 추출
with torch.no_grad():
    outputs = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])

# 출력값에서 필요한 부분(임베딩) 추출
embeddings = outputs.last_hidden_state

print(embeddings)


