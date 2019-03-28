"""
    Author: Chinmay Bhoir
    Created on: 26/3/19 2:06 PM
"""
import difflib
import operator
import math


def f_name_score(search_term, names_list):
    """
    Calculates the measure of sequence's similarity between search_term and first name
     using SequenceMatcher
    Similar to Levenshtein distance
    :param search_term:
    :param names_list:
    :return: scores: list of dict objects with 'name' and 'score'
    """
    scores = list()
    for name in names_list:
        f_name_instance = dict()
        f_name_instance['name'] = name['name']
        f_name_instance['score'] = difflib.SequenceMatcher(isjunk=None,
                                                           a=search_term.lower(),
                                                           b=name['f_name'].lower()).ratio()
        scores.append(f_name_instance)
    return scores


def m_name_score(search_term, names_list):
    """
    Calculates the measure of sequence's similarity between search_term and middle name
     using SequenceMatcher
    Similar to Levenshtein distance
    :param search_term:
    :param names_list:
    :return: scores: list of dict objects with 'name' and 'score'
    """
    scores = list()
    for name in names_list:
        m_name_instance = dict()
        m_name_instance['name'] = name['name']
        m_name_instance['score'] = difflib.SequenceMatcher(isjunk=None,
                                                           a=search_term.lower(),
                                                           b=name['m_name'].lower()).ratio()
        scores.append(m_name_instance)
    return scores


def l_name_score(search_term, names_list):
    """
    Calculates the measure of sequence's similarity between search_term and middle name
     using SequenceMatcher
    Similar to Levenshtein distance
    :param search_term:
    :param names_list:
    :return: scores: list of dict objects with 'name' and 'score'
    """
    scores = list()
    for name in names_list:
        l_name_instance = dict()
        l_name_instance['name'] = name['name']
        l_name_instance['score'] = difflib.SequenceMatcher(isjunk=None,
                                                           a=search_term.lower(),
                                                           b=name['l_name'].lower()).ratio()
        scores.append(l_name_instance)
    return scores


def len_closeness(source, target):
    """
    Calculate the measure of closeness of two strings according to their length
    The closeness measured is calculated by using the bell-shaped curve
    X-axis denotes the difference in lengths, and Y-axis denotes the rating
    This is similar to a cosine curve, and hence formula used is y = cos(x*pi/180)
    :param source:
    :param target:
    :return: Measure of length closeness between two strings
    """
    diff = math.fabs(len(target) - len(source))
    closeness_score = math.cos(diff * math.pi/180)
    return closeness_score


def score_aggregator(search_term, names_list):
    """
    Calculate the aggregated score from sequence match score with first name, middle name, and last name
    :param search_term:
    :param names_list:
    :return:
    """
    scores = list()
    # Calculate sequence match scores with first name, last name, and middle name
    f_name_scores = f_name_score(search_term, names_list)
    m_name_scores = m_name_score(search_term, names_list)
    l_name_scores = l_name_score(search_term, names_list)
    # Aggregate the score from first name, middle name, and last name scores for each entry in names
    for i, name in enumerate(names_list):
        name_instance = dict()
        name_instance['name'] = name['name']
        # Get max score among first name score, last name score, and middle name score
        # Also get index of which name (among first, middle, and last) gives the most the score, to be
        # later used for length closeness
        index, score = max(enumerate([f_name_scores[i]['score'],
                                     m_name_scores[i]['score'],
                                     l_name_scores[i]['score']]), key=operator.itemgetter(1))
        names = [names_list[i]['f_name'],
                 names_list[i]['m_name'],
                 names_list[i]['l_name']]
        name_instance['score'] = score
        # If score > 0.75, take the length measure into account to compare score among top choices
        if score > 0.75 and len(search_term) > 0:
            closeness = len_closeness(search_term, names[index])
            # print("name:", name['name'], " closeness:", closeness)
            name_instance['score'] = (score + closeness)/2
        scores.append(name_instance)
    # Sort the list according to scores
    scores_sorted = sorted(scores, key=lambda x: x['score'], reverse=True)
    return scores_sorted


if __name__ == '__main__':
    searches = score_aggregator("Vij")
    print(sorted(searches, key=lambda x: x['score']))
