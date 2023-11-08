def convert_to_qna_chucks(req_data):
    arr = []
    for i, entry in enumerate(req_data):
        if entry["sender_id"] != 1:
            output = {
                "question": entry["message"],
                "unanswered": entry["unanswered"],
                "message_id": entry['id'],
                "created_at": entry['created_at'],
            }
            if i + 1 < len(req_data) and req_data[i + 1]["chat_id"] == entry["chat_id"] and req_data[i + 1]["sender_id"] == 1:
                output.update({
                    "answer": req_data[i + 1]["message"],
                    "answer_vote": req_data[i + 1]["vote"],
                    "answer_id": req_data[i + 1]["id"],
                })
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

# get top questions by times asked, sorted in descending order
def get_top_questions_by_times_asked(qna_list, top_n=10):
    qna_list = [item for item in qna_list if item["question"] != "" and item.get("answer") != []]
    return sorted(qna_list, key=lambda x: x["times_asked"], reverse=True)[:top_n]


