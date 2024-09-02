import fasttext.util
import fasttext
fasttext.util.download_model('ko', if_exists='ignore')
ft = fasttext.load_model('cc.ko.300.bin')