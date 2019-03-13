'''
Sentiment analysis using SentiWordNet
'''

import nltk
from nltk.corpus import sentiwordnet as swn

#sentence = '''This is a really horrible movie
#'''


import pandas as pd


def estimate_sentiment(sentence, verbose = False):
    words = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)
    pos_score = 0
    neg_score = 0
    token_count = 0
    obj_score = 0
    final_sentiment = 0
    ##print tagged_words
    for word, tag in tagged_words:
        # print (word, tag)
        ss_set = None
        ## show
        ## swn.senti_synsets('loved', 'v')
        
        if 'NN' in tag:
            x = list(swn.senti_synsets(word, 'n'))
            if len(x) > 0:
                ss_set = x[0]
        if 'VB' in tag:
            x = list(swn.senti_synsets(word, 'v'))
            if len(x) > 0:
                ss_set = x[0]
        if 'JJ' in tag:
            x = list(swn.senti_synsets(word, 'a'))
            if len(x) > 0:
                ss_set = x[0]
        if 'RB' in tag:
            x = list(swn.senti_synsets(word, 'r'))
            if len(x) > 0:
                ss_set = x[0]
           

        

        if ss_set:
            #print ('word', ss_set, ss_set.pos_score(), ss_set.neg_score(), ss_set.obj_score())

            # add scores for all found synsets
            pos_score += ss_set.pos_score()
            neg_score += ss_set.neg_score()
            obj_score += ss_set.obj_score()
            token_count += 1

            ##print pos_score

            
    # aggregate final scores
    ##print token_count
    final_score = pos_score - neg_score
    norm_final_score = round(float(final_score) / token_count, 2)
    # can change the threshold if you like.  Could make 0 and close values be neutral.
    final_sentiment = 'positive' if norm_final_score >= 0 else 'negative'

    # the rest is just for pretty display of detailed results
    if verbose:
        norm_obj_score = round(float(obj_score) / token_count, 2)
        norm_pos_score = round(float(pos_score) / token_count, 2)
        norm_neg_score = round(float(neg_score) / token_count, 2)
        # to display results in a nice table
        sentiment_frame = pd.DataFrame([[final_sentiment, norm_obj_score,
                                         norm_pos_score, norm_neg_score,
                                         norm_final_score]],
                                         columns=pd.MultiIndex(levels=[['SENTIMENT STATS:'], 
                                                                      ['PredictedSentiment', 'Objectivity',
                                                                       'Positive', 'Negative', 'Overall']], 
                                                              labels=[[0,0,0,0,0],[0,1,2,3,4]]))
        # print ( sentiment_frame)
    
    return final_sentiment, norm_final_score
                
    
# decision, score = estimate_sentiment(sentence, False)

