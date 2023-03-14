import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["OPENAI_KEY"]


def generate_response(messages):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = 1.0 # 0.0 - 2.0
    )
    # print(response.choices[0].message)
    return response.choices[0].message


# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


st.title("Sales Coach Trainer")

if 'customer_conv' not in st.session_state:
    st.session_state['customer_conv'] = [
        {"role": "system", "content": "You are a chat bot acting like a customer interested in buying a pen"},
        # {"role": "user", "content": "How can I help you today?"},
    ]
    response = generate_response(st.session_state.customer_conv)
    st.session_state.customer_conv.append(response)

# if 'trainer_conv' not in st.session_state:
#     st.session_state['trainer_conv'] = [
#         {"role": "system", "content": "You are an expert sales coach"},
#         {"role": "user", "content":
#             "Consider this conversation"},
#     ]
#     response = generate_response(st.session_state.customer_conv)
#     st.session_state.customer_conv.append(response)

# user_input = get_text()
user_input = st.text_input('You:',key='input')

if user_input:
    st.session_state.customer_conv.append({"role": "user", "content": user_input})
    print('customer_conv---------------\n',st.session_state.customer_conv,'\n-------------')
    response = generate_response(st.session_state.customer_conv)
    st.session_state.customer_conv.append(response)

    # store the output
    # st.session_state.past.append(user_input)
    # st.session_state.generated.append(output)

if st.session_state['customer_conv']:
    # for i in range(len(st.session_state['generated']) - 1, -1, -1):
    #     message(st.session_state["generated"][i], key=str(i))
    #     message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    message("Hi, I'm a potential customer interested in buying a pen, try to sell it to me in 3 interactiion and then you'll have feedbackss on how well you performed",
            key="000")

    for i, text in enumerate(st.session_state['customer_conv'][2:]):
        if text['role'] == 'user':
            message(text['content'], is_user=True,  key=str(i) + text['role'])
        else:
            print('text:', text)
            message(text['content'], key=str(i) + text['role'])

    if len(st.session_state['customer_conv']) >= 9:
        st.session_state.customer_conv.append({"role": "system", "content": "You are an experienced sales coach"})

        # st.session_state.customer_conv.append(
        #     {"role": "user", "content": "can you provide me feedbacks and suggestion on how to improve as a seller based on the previous convrsation?"}
        # )
        # feedback = generate_response(st.session_state.customer_conv)
        # message(feedback['content'], key="feedback" + feedback['role'])
        # st.session_state.customer_conv.append(feedback)

        st.session_state.customer_conv.append(
            {"role": "user", "content": "provide me a score between 0 and 2 also based on the previous convrsation?"}
        )
        score = generate_response(st.session_state.customer_conv)
        message(score['content'], key="score" + score['role'])




