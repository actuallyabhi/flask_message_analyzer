import os
from flask import Flask, request
from dotenv import load_dotenv

# modules
from helpers.formatters import convert_to_qna_chucks, filter_duplicates, get_top_questions_by_times_asked
from helpers.optimizers import merge_similar_questions_using_nlp, merge_similar_questions,merge_similar_answers, merge_similar_answers_using_nlp
from helpers.aggregators import get_satisfaction_scores


app = Flask(__name__)

@app.route('/get_top_questions', methods=['POST'])
def get_top_questions():
    # Get the request body
    req_data = request.get_json()

    # Process the request body
    qna_arr = convert_to_qna_chucks(req_data['messages'])

    # Filter duplicates
    unique_messages = filter_duplicates(qna_arr)

    # marge similar questions
    merged_messages = merge_similar_questions(unique_messages)

    # Get top questions by times asked
    top_messages = get_top_questions_by_times_asked(merged_messages, 10)
    
    # merge similar answers
    final_messages = merge_similar_answers_using_nlp(top_messages)

    # aggregate answers with satisfaction scores
    aggregated_data = get_satisfaction_scores(final_messages)


    return aggregated_data

if __name__ == '__main__':
    load_dotenv()
    # check for OPEN_AI_API_KEY
    if not os.environ.get('OPEN_AI_KEY'):
        print('OPENAI_API_KEY not found in .env file')
        exit(1)
    app.run(debug=True)
