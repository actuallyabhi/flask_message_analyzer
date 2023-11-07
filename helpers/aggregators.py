import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from openai._exceptions import OpenAIError, AuthenticationError, RateLimitError

# data = [{
# 			"answers": [
# 				"The cost of IVF can vary depending on several factors, including the location of the clinic, the reputation and success rates of the clinic, any additional procedures or tests required, medications used during treatment, and whether any fertility preservation techniques are needed. Each clinic may have its own pricing structure. It's best to consult with your specific clinic for a detailed breakdown of costs.",
# 				"The factors that determine the cost of IVF include:\n1. Geographic location: The cost can vary depending on the country and city where you receive treatment.\n2. Clinic reputation and expertise: More renowned clinics may charge higher fees.\n3. Treatment protocol: Different protocols have different costs, such as standard IVF or advanced techniques like ICSI or PGS\/PGD.\n4. Medications: The type and dosage of medications needed for ovarian stimulation can significantly impact the cost.\n5. Additional procedures: If additional procedures like embryo freezing, embryo transfer, or genetic testing are required, they will add to the overall cost.\n\nFor more information, you can visit this article - [Factors Affecting Cost of IVF](https:\/\/www.drmalpani.com\/knowledge-center\/articles\/factors-affecting-cost-of-ivf)"
# 			],
# 			"question": "What is the Cost for IVF?",
# 			"times_asked": 4
# 		},
# 		{
# 			"answers": [
# 				"When choosing an IVF clinic, consider factors like success rates, doctor-patient communication, treatment options offered, cost and convenience, clinic reputation and reviews. It's important to find a clinic that aligns with your needs and values.",
# 				"When choosing an IVF clinic, consider factors such as:\n1. Success rates: Look for clinics with high success rates.\n2. Expertise and experience of the doctors: Choose a clinic with experienced fertility specialists.\n3. Services offered: Ensure the clinic offers comprehensive services and treatment options.\n4. Patient reviews and testimonials: Read about other patients' experiences at the clinic.\n5. Cost and affordability: Consider the cost of treatment and any additional expenses.\n6. Location and convenience: Choose a clinic that is easily accessible to you.\n7. Personal connection with the doctor: Consult with different doctors to find one who understands your needs.\n\nFor more information, visit [Choosing an IVF Clinic](https:\/\/www.drmalpani.com\/knowledge-center\/articles\/choosing-an-ivf-clinic)."
# 			],
# 			"question": "How to choose the right clinic?",
# 			"times_asked": 2
# 		},
# 		{
# 			"answers": [
# 				"Hello! How can I assist you today?"
# 			],
# 			"question": "Hi",
# 			"times_asked": 2
# 		}]
def get_satisfaction_scores(topQuestionAnswers):
    aggregated_data = []
    client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))
    for d in topQuestionAnswers:
        question = d['question']
        answers = d['answers']
        times_asked = d['times_asked']
        try: 
            response = client.chat.completions.create(
                        model="gpt-3.5-turbo-0613",
                        messages=[{
                            'role': 'system',
                            'content': """You will be provided with a question and array of answers. Please rate the answer on a scale of 1 to 5, with 1 being the lowest and 5 being the highest. The basis of your rating should be how well the answer addresses the question and how satisfied you are with the answer.
                            Output format should be in JSON. AS:{ question: "", answers: [
                                    {
                                    answer: "",
                                    satisfaction_score:  int
                                }]
                            },
                            """
                            },
                            {
                            'role': 'user',
                            'content': f"Q: {question}\nA: {answers}\nSatisfaction score:"
                            }
                        ],
                        temperature=0.8,
                        max_tokens=1000,
                    
                    )
            # convert response to json
            formatted_response = json.loads(response.choices[0].message.content)

            # add times_asked to formatted_response
            formatted_response['times_asked'] = times_asked

            aggregated_data.append(formatted_response)
          # handle multiple exceptions at once
        except (OpenAIError, AuthenticationError, RateLimitError) as e:
            print(e)
            return {
                'status_code': 500,
                'error': 'Something went wrong. Please try again later.'
            }
        except Exception as e:
            print(e)
            formatted_response = {
                'question': question,
                'answers': answers,
                'times_asked': times_asked,
            }         
            aggregated_data.append(formatted_response)
    return aggregated_data



# demo code
# load_dotenv()
# print(get_satisfaction_scores(data))