import re


pattern = "(summarization|summarisation|text|nlg|nlp)|(automatic)[^.]*(generation|summary|summarization|summarisation)|(abstractive|extractive)[^.]*(model|summary|modelling|modeling|summarization|summarisation|processing)|(semantic)[^.]*(retrieval|graph|model|modelling|modeling|summarization|summarisation|processing|representations)|(natural|language)[^.]*(language|generation|processing)|(information)[^.]*(retrieval|graph|summary|summarization|summarisation)"

sentence = "Automatic Generation of Summeries for the Web"

if re.match(pattern, sentence.lower()):
    print('Found a match')
else:
    print('Not a match')