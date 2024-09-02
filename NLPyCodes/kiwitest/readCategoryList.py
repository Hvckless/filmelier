import codecs

categoryFile = codecs.open('./movielist/categoryList.txt', 'r', encoding='utf-8')
categoryTextContent = categoryFile.read()

print(categoryTextContent.split('\n'))



text_dict = {}

for token in categoryTextContent.split('\n'):
    text_dict[token]