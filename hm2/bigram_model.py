from string import punctuation
import numpy as np

dostoevsky = open('besy_dostoevsky.txt', encoding='cp1251').read()
tolstoy = open('anna_karenina.txt').read()

def normalize(text):
    normalized_text = [word.strip(punctuation) for word \
                                                            in text.lower().split()]
    normalized_text = [word for word in normalized_text if word]
    return normalized_text
