import spacy
from collections import defaultdict
from fuzzywuzzy import fuzz
from itertools import chain

nlp = spacy.load("en_core_web_sm")
# merge similar questions using spaCy similarity (Slow)
def merge_similar_questions_using_nlp(messageArr, similarity_threshold=0.8):
    merged_qna_dict = defaultdict(lambda: {"answers": [], "times_asked": 0})
    for qna in messageArr:
        question = qna["question"]
        answer = qna["answer"]
        times_asked = qna.get("times_asked", 1)
        found_similar_question = False

        for key in merged_qna_dict:
            similarity = nlp(question).similarity(nlp(key))

            if similarity >= similarity_threshold:
                for item in answer:
                    merged_qna_dict[key]["answers"].append(item)
                merged_qna_dict[key]["times_asked"] += times_asked
                found_similar_question = True
                break

        # If not similar to any existing question, create a new entry with an array
        if not found_similar_question:
                for item in answer:
                    merged_qna_dict[question]["answers"].append(item)
                merged_qna_dict[question]["times_asked"] = times_asked

    merged_qna_list = [{"question": key, "answers": value.get(
        "answers"), "times_asked": value["times_asked"]} for key, value in merged_qna_dict.items()]
    return merged_qna_list

            





# Reference:  https://towardsdatascience.com/find-text-similarities-with-your-own-machine-learning-algorithm-7ceda78f9710

# merge similar questions using fuzzywuzzy (Fast)
def merge_similar_questions(qna_list, similarity_threshold=80):
    merged_qna_dict = defaultdict(lambda: {"answers": [], "times_asked": 0})
    for qna in qna_list:
        question = qna["question"]
        answer = qna["answer"]
        times_asked = qna.get("times_asked", 1)
        found_similar_question = False

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
    merged_qna_list = [{"question": key, "answers": value.get(
        "answers"), "times_asked": value["times_asked"]} for key, value in merged_qna_dict.items()]
    return merged_qna_list


def merge_similar_answers_using_nlp(messageArr, similarity_threshold=0.8):
    for x in messageArr:
        x['answers'] = list(set(x.get('answers')))
        merged_answers = []
        for answer in x['answers']:
            found_similar_answer = False
            for index, existing_answer in enumerate(merged_answers):
                similarity = nlp(answer).similarity(nlp(existing_answer))
                if similarity >= similarity_threshold:
                    found_similar_answer = True
                    break
            if not found_similar_answer:
                merged_answers.append(answer)

        x['answers'] = merged_answers
    return messageArr

# merge similar answers using fuzzywuzzy (Fast)


def merge_similar_answers(answer_list, similarity_threshold=80):
    for x in answer_list:
        x['answers'] = list(set(x.get('answers')))
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
