def convert_to_qna_chucks(req_data):
    arr = []
    i = 0
    while i < len(req_data):
        entry = req_data[i]
        output = {}
        if entry["sender_id"] != 1:
            output['question'] = entry["message"]
            output['unanswered'] = entry["unanswered"]
            output['message_id'] = entry['id']
            i += 1
            if (req_data[i]["chat_id"] == entry["chat_id"] and req_data[i]["sender_id"] == 1):
                output['answer'] = req_data[i]['message']
                output['answer_vote'] = req_data[i]['vote']
                output['answer_id'] = req_data[i]['id']
        i +=1
        arr.append(output)
    return arr


def merge_duplicates(dataArr):
    unique_questions = {}
    for item in dataArr:
        question = item.get("question", "")
        answer = item.get("answer")

        if question not in unique_questions:
            unique_questions[question] = {
                "answer": [answer] if answer is not None and answer != "" else [],
                "times_asked": 1
            }
        else:
            if answer is not None and answer != "":
                unique_questions[question]["answer"].append(answer)
            unique_questions[question]["times_asked"] += 1

    # Convert the dictionary values back to a list
    return [{"question": k, **v} for k, v in unique_questions.items()]


# def merge_duplicate_questions_with_answer_data(dataArr):
#     unique_questions = {}
#     for item in dataArr:
#         question = item.get("question", "")
#         answer = item.get("answer")
#         vote = item.get("answer_vote")

#         if question not in unique_questions:
#             unique_questions[question] = {
#                 "answer": [{"answer": answer, "vote": vote}] if answer is not None and answer != "" else [],
#                 "unanswered": item.get("unanswered", False),
#                 "times_asked": 1
#             }
#         else:
#             if answer is not None and answer != "":
#                 unique_questions[question]["answer"].append({
#                     "answer": answer,
#                     "vote": vote
#                 })
#             unique_questions[question]["times_asked"] += 1

#     # Convert the dictionary values back to a list
#     merged_data = [{"question": k, **v} for k, v in unique_questions.items()]

#     return merged_data

# get top questions by times asked, sorted in descending order
def get_top_questions_by_times_asked(qna_list, top_n=10):
    qna_list = [item for item in qna_list if item["question"] != "" and item.get("answer") != []]
    return sorted(qna_list, key=lambda x: x["times_asked"], reverse=True)[:top_n]


