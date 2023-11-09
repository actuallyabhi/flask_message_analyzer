import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Helper functions
from helpers.formatters import convert_to_qna_chucks, get_top_questions_by_times_asked
from helpers.optimizers import merge_similar_questions_using_fuzzy, merge_similar_answers_using_nlp, merge_similar_questions_using_nlp
from helpers.aggregators import get_satisfaction_scores, get_top_negative_score_questions

app = Flask(__name__)

@app.route('/get_top_questions', methods=['POST'])
def get_top_questions():
    req_data = request.get_json()

    ## Formatting the data to be optimized
    qna_list = convert_to_qna_chucks(req_data['messages'])
    merged_messages = merge_similar_questions_using_fuzzy(qna_list) # Fastest
    # merged_messages = merge_similar_questions_using_nlp(qna_list) # more accurate

    ## Optimizing the data
    top_messages = get_top_questions_by_times_asked(merged_messages, 10)
    final_messages = merge_similar_answers_using_nlp(top_messages)

    ## Aggregating the data
    aggregated_data = get_satisfaction_scores(final_messages)

    return jsonify(aggregated_data)

@app.route('/get_worst_or_unanswered_questions', methods=['POST'])
def get_worst_or_unanswered_questions():
    ## Get the request body
    req_data = request.get_json()

    ## Formatting the data to be aggregated
    qna_list = convert_to_qna_chucks(req_data['messages'])

    ## Aggregating the data
    aggregated_data = get_top_negative_score_questions(qna_list, 10)
    
    return jsonify(aggregated_data)

if __name__ == '__main__':
    load_dotenv()

    if not os.environ.get('OPEN_AI_KEY'):
        print('OPENAI_API_KEY not found in .env file')
        exit(1)

    app.run(debug=True)

