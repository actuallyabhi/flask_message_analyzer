def convert_to_qna_chucks(req_data):
    arr = []
    i = 0
    while i < len(req_data):
        entry = req_data[i]
        output = {}
        if entry["sender_id"] != 1:
            output['question'] = entry["message"]
            i += 1
            if (req_data[i]["chat_id"] == entry["chat_id"] and req_data[i]["sender_id"] == 1):
                output['answer'] = req_data[i]['message']
        i +=1
        arr.append(output)
    return arr

def filter_duplicates(dataArr):
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
    merged_data = [{"question": k, **v} for k, v in unique_questions.items()]

    return merged_data


def get_top_questions_by_times_asked(qna_list, top_n=10):
    qna_list = [item for item in qna_list if item["question"] != "" and item.get("answer") != []]
    return sorted(qna_list, key=lambda x: x["times_asked"], reverse=True)[:top_n]


