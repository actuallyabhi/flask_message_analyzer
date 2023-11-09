import spacy
import concurrent.futures
import numpy as np
from fuzzywuzzy import fuzz
from itertools import chain
from collections import defaultdict
from scipy.spatial.distance import cosine

from .formatters import merge_duplicates

# nlp = spacy.load("en_core_web_sm") # when using en_core_web_sm
nlp = spacy.load("en_core_web_md")


def _calculate_similarity(subject, key):
    subject_vector = nlp(subject).vector
    key_vector = nlp(key).vector

    if np.all(subject_vector == 0) or np.all(key_vector == 0):
        return 0

    return 1 - cosine(subject_vector, key_vector)

# merge similar questions using spaCy similarity  (Slow)
def merge_similar_questions_using_nlp(messagesList, similarity_threshold=0.8):
    unique_messages = merge_duplicates(messagesList)

    merged_qna_dict = defaultdict(lambda: {"answers": [], "times_asked": 0})
    def process_qna(qna):
        question = qna["question"]
        answer = qna["answer"]
        times_asked = qna.get("times_asked", 1)
        found_similar_question = False

        for key in merged_qna_dict:
            # similarity = nlp(question).similarity(nlp(key)) # when using en_core_web_sm
            similarity = _calculate_similarity(question, key)

            if similarity >= similarity_threshold:
                for item in answer:
                    merged_qna_dict[key]["answers"].append(item)
                merged_qna_dict[key]["times_asked"] += times_asked
                found_similar_question = True
                break

        if not found_similar_question:
            for item in answer:
                merged_qna_dict[question]["answers"].append(item)
            merged_qna_dict[question]["times_asked"] = times_asked

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_qna, unique_messages)

    merged_messagesList = [{"question": key, "answers": value.get(
        "answers"), "times_asked": value["times_asked"]} for key, value in merged_qna_dict.items()]
    return merged_messagesList

# Reference:  https://towardsdatascience.com/find-text-similarities-with-your-own-machine-learning-algorithm-7ceda78f9710

# merge similar questions using fuzzywuzzy (Slow)
def merge_similar_questions_using_fuzzy(messagesList, similarity_threshold=80):
    ## Step 1: Merge duplicate questions
    unique_messages = merge_duplicates(messagesList)

    ## Step 2: Merge semantically similar questions
    # create a dictionary to store the merged data
    merged_qna_dict = defaultdict(lambda: {"answers": [], "times_asked": 0})
    # iterate over each question-answer pair in the messagesList
    for qna in unique_messages:
        question = qna["question"]
        answer = qna["answer"]
        times_asked = qna.get("times_asked", 1)

        # create a flag to indicate whether a similar question was found
        found_similar_question = False

        # iterate over each key in the merged_qna_dict
        for key in merged_qna_dict:
            similarity = fuzz.ratio(key, question)

            if similarity >= similarity_threshold:
                for item in answer:
                    merged_qna_dict[key]["answers"].append(item)
                merged_qna_dict[key]["times_asked"] += times_asked
                found_similar_question = True
                break

        if not found_similar_question:
            for item in answer:
                merged_qna_dict[question]["answers"].append(item)
            merged_qna_dict[question]["times_asked"] = times_asked

    # convert the merged_data dictionary into a list of dictionaries
    merged_messagesList = [{"question": key, "answers": value.get(
        "answers"), "times_asked": value["times_asked"]} for key, value in merged_qna_dict.items()]

    return merged_messagesList

# merge similar answers using spaCy similarity (Fast)
def merge_similar_answers_using_nlp(messages, similarity_threshold=0.8):
    for message in messages:
        message['answers'] = list(set(message.get('answers')))
        merged_answers = []
        for answer in message['answers']:
            found_similar_answer = False
            for index, existing_answer in enumerate(merged_answers):
                # similarity = nlp(answer).similarity(nlp(existing_answer)) # when using en_core_web_sm
                similarity = _calculate_similarity(answer, existing_answer)
                if similarity >= similarity_threshold:
                    found_similar_answer = True
                    break
            if not found_similar_answer:
                merged_answers.append(answer)

        message['answers'] = merged_answers
    return messages

# merge similar answers using fuzzywuzzy (Fast)
def merge_similar_answers(answer_list, similarity_threshold=80):
    # Remove duplicates from each answer list
    for x in answer_list:
        x['answers'] = list(set(x.get('answers')))

    # Iterate over answers and merge similar answers
    merged_answers = []
    for answer in x['answers']:
        found_similar_answer = False
        for index, existing_answer in enumerate(merged_answers):
            similarity = fuzz.token_set_ratio(answer, existing_answer)
            if similarity >= similarity_threshold:
                found_similar_answer = True
                break
        if not found_similar_answer:
            merged_answers.append(answer)

    x['answers'] = merged_answers

    return answer_list
