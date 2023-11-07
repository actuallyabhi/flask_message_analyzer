
# logic to get top worst questions 
> deps (unanswered or no_answer_exists || downvoted) 
    - so if it is unanswered or no answer exists is bad question and will get -2.5 score
    - if it is downvoted it will get -1 score
    - if it is both it will get -3.5 score
    > the questions will be sorted by score and in case of same score by creation date