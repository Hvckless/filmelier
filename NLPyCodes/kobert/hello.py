from gluonnlp.data import SentencepieceTokenizer
from kobert import get_tokenizer
tok_path = get_tokenizer()
sp  = SentencepieceTokenizer(tok_path)
hello = sp('BPE-dropout을 이용하면 서비스에 적합한 띄어쓰기에 강건한 모델로 튜닝 할 수 있습니다. 학습시 아래와 유사한 토크나이저 설정으로 학습을 진행할 수 있습니다. 자세한 옵션 설명은 이곳을 참고하세요.')

print(hello)