import streamlit as st
import bs4 as bs
import urllib.request
import re
import heapq
import nltk

# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download()

#______________________________________________________
##     FRONT END

#title and placeholer text using streamlit
st.title("AUTO TEXT SUMMARIZATION TOOL")
st.write("### Enter text or provide URL")

#input city name using single line text widget and storing it in a var
txt = st.text_input("Input:") #arguements as label and value when text widget is first rendered
#creating the submit button
Submit = st.button("Submit")

if txt==None:
    st.write("Input something!")
    

#____________________________________________________    
##    BACKEND
container = st.container()

if txt:
    # if URL is provided
    if txt[:5] == 'https':
        scraped_data = urllib.request.urlopen(txt)
        article = scraped_data.read()

        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""   

        for p in paragraphs:
            article_text += p.text

    # if text is provided
    else:
        article_text = txt


    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1


    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]


    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    container.write(summary)

# In case in input provided
else:
    container.write("Input something!")