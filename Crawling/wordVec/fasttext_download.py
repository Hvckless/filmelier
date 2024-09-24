#pip install fasttext
#위가 오류가 발생하면
#pip install fasttext-wheel

import fasttext.util
import fasttext
fasttext.util.download_model('ko', if_exists='ignore')
ft = fasttext.load_model('cc.ko.300.bin')
ft.save_model('src/filmelier/Crawling/wordVec/cc.ko.300.bin')


