import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["OPENAI_KEY"]

# def clear_cache():
#     st.session_state['customer_conv'] = []
#     # print(st.session_state)
#     # st.experimental_rerun()
#
#
# st.button("Restart",on_click=clear_cache)

def generate_response(messages):
    print('customer_conv---------------\n',messages,'\n-------------')

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
        {"role": "system",
         "content": "You are an assistant acting as customer in a sale simulation while the user is trying to sell you a pen"},
        {"role": "user",
         "content": "Act as a customer while i'm trying to sell you a pen, start by asking if I sell any pens"}
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


if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.input
    st.session_state.input = ''

# user_input = get_text()
# user_input = st.text_input('You:',key='input')

st.text_input('You:', key='input', on_change=submit)

if st.session_state.user_input:
    st.session_state.customer_conv.append({"role": "user", "content": st.session_state.user_input})
    response = generate_response(st.session_state.customer_conv)
    st.session_state.customer_conv.append(response)

    # store the output
    # st.session_state.past.append(user_input)
    # st.session_state.generated.append(output)

if st.session_state['customer_conv']:
    # for i in range(len(st.session_state['generated']) - 1, -1, -1):
    #     message(st.session_state["generated"][i], key=str(i))
    #     message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    message("""Hello, I'll act as a potential customer interested in buying a pen while you try to sell it to me. 
You have 3 interaction to convince me, then I'll give you a feedback on how well you performed""",
            key="000")

    for i, text in enumerate(st.session_state['customer_conv'][2:]):
        if text['role'] == 'user':
            message(text['content'], is_user=True,  key=str(i) + text['role'])
        else:
            message(text['content'], key=str(i) + text['role'])

    if len(st.session_state['customer_conv']) >= 9:
        st.session_state.customer_conv.append({"role": "system", "content": "You are an experienced sales coach"})

        # st.session_state.customer_conv.append(
        #     {"role": "user", "content": "can you provide me feedbacks and suggestion on how to improve as a seller based on the previous convrsation?"}
        # )
        # feedback = generate_response(st.session_state.customer_conv)
        # message(feedback['content'], key="feedback" + feedback['role'])
        # st.session_state.customer_conv.append(feedback)

        # st.session_state.customer_conv.append(
        #     {"role": "user", "content": """provide feedback on how effectively did I tried to sell the pen, then on a new line give me float score between 0 and 10 in the format of: Score:[float]"""}
        # )

        st.session_state.customer_conv.append(
            {"role": "user",
             "content": """Provide a feedback on how effective I have been trying to sell you a pen, penalizing me if I changed subject, rambled or have been unhelpful.
        Then on a new line give me an int score between 0 and 10 on how effective I have been trying to sell you a pen, strictly in the format of:
        Score: [int]"""}
        )
        score = generate_response(st.session_state.customer_conv)
        message(score['content'], key="score" + score['role'])




