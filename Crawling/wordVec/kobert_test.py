import torch
from transformers import BertTokenizer, BertForTokenClassification, pipeline

# 사전 훈련된 NER 모델 이름
model_name = 'monologg/kobert'  # NER 태스크에 맞게 fine-tuning된 모델

# 모델과 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)

# 장치 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# NER 파이프라인 생성
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

# 리뷰 데이터 로드
test_text = "김철수와 이영희가 함께 공원에서 산책을 했습니다."
ner_results = ner_pipeline(test_text)
for entity in ner_results:
    print(f"Entity: {entity['word']}, Label: {entity['entity']}")



