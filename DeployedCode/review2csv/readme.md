# requirements.txt 파일 목록의 패키지를 설치하는 방법

cmd 입력
```bash
pip install -r requirements.pip
```

## review2csv 사용법

1. 해당 폴더에 ignore 파일을 만들고 fasttext의 cc.ko.100.bin 파일을 넣어주세요.
2. movielist 폴더를 만들고 categoryList.txt와 movie_filterList.txt 파일을 준비해주세요.
3. 이 텍스트 파일들은 개행으로 각 구분하며 갯수 제한이 없습니다. 
4. reviews 폴더를 만들고 그 안에 영화 목록을 넣어주세요. 일단은 코드상으로는 txt 확장자만 작동합니다.
5. review2csv에서 export2CSV 함수에 영화 제목을 넣어주세요. reviews에 넣은 영화 리뷰 이름이 martian.txt라면 martian만 적어주세요.
