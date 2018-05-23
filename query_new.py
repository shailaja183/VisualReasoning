import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import json
import os
from nltk.parse import stanford

os.environ['CLASSPATH'] = "/Users/shailajasampat/Downloads/stanford-corenlp-full-2018-02-27"
os.environ['STANFORD_PARSER'] = "/Users/shailajasampat/Downloads/stanford-parser-full-2018-02-27/stanford-parser.jar"
os.environ['STANFORD_MODELS'] = "/Users/shailajasampat/Downloads/stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar"

example_sent = "There are exactly two yellow blocks and a black block."

numberDict = { 
"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", 
"nine": "9", "ten": "10"
}

example_sent = example_sent.replace(' a ', ' 1 ')
for key in numberDict:
	for i in example_sent.split():
		if i==key:
			example_sent = example_sent.replace(i, numberDict[key])
   
print(example_sent)

parser=stanford.StanfordParser(model_path="/Users/shailajasampat/Downloads/englishPCFG.ser.gz")
sentences = list(parser.raw_parse(example_sent))
		
print(sentences)
print(sentences[0])

'''
tokenizer = RegexpTokenizer(r'\w+')
word_tokens = tokenizer.tokenize(example_sent)
 
stop_words = set(stopwords.words('english'))
 
#word_tokens = word_tokenize(example_sent)
 
filtered_sentence = [w for w in word_tokens if not w in stop_words]
 
filtered_sentence = []
 
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)
 
print(filtered_sentence)
untok_sentence = ' '.join(filtered_sentence) 
'''

#raw_parsed_query = list(parser.raw_parse(query))
#print(raw_parsed_query)

'''
{ 
"circle": "has(_,shape,circle)",
"triangle": "has(_,shape,triangle)",
"square": "has(_,shape,square)",
"black": "has(_,color,red)",
"yellow": "has(_,color,yellow)"
"blue": "has(_,color,blue)"
"not": "not",
"item": "object(_)",
"block": "block(_)",
"blocks": "block(_)",
}
'''
