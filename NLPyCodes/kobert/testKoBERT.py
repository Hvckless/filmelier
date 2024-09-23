from kobert_tokenizer import KoBERTTokenizer
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
hello = tokenizer.encode("한국어 모델을 공유합니다.")

print(hello)

hello2 = tokenizer.encode("한국어 배웁시다.")

print(hello2)