import torch
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('skt/kobert-base-v1')
model = AutoModel.from_pretrained('skt/kobert-base-v1')
text = "KoBERT는 Apache-2.0 라이선스 하에 공개되어 있습니다. 모델 및 코드를 사용할 경우 라이선스 내용을 준수해주세요. 라이선스 전문은 LICENSE 파일에서 확인하실 수 있습니다."
inputs = tokenizer.batch_encode_plus([text])
out = model(input_ids = torch.tensor(inputs['input_ids']),
              attention_mask = torch.tensor(inputs['attention_mask']))
out.pooler_output.shape
torch.Size([1, 768])

print(out)