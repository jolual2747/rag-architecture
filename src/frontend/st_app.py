import streamlit as st
from utils import (
    clean_prod_workspace, 
    create_vector_database_from_pdf, 
    create_chatbot
)

def start_over_with_new_document():
    st.session_state.text_input = ''
    # delete the vector store from the session state
    del st.session_state.vs
    del st.session_state.bot
    del st.session_state.messages
    # display message to user
    st.info('Please upload new documents to continue after clearing or updating the current ones.')

def clear_text_input():
    st.session_state.text_input = ''

def main() -> None:
    """
    Main of the Streamlit app. 
    """
    st.title("Chat with your documents")
    st.write("Upload your document and start chatting!")

    with st.sidebar:
        st.title("Upload a document to interact with")
        uploaded_file = st.file_uploader("Upload a document", type=["pdf"])
        mode = st.selectbox(label ="Select mode:",options=["Chat with documents", "Chat as a Customer Service Agent"])

        if uploaded_file and st.button("Start chatting!"):
            tmp_route = "./src/frontend/tmp"
            clean_prod_workspace(tmp_route)
            file_name = f"{tmp_route}/{uploaded_file.name}"
            # Guardar el documento en el servidor
            with open(file_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("Document uploaded successfully!")

            st.session_state.vs = create_vector_database_from_pdf(file_name)
            st.session_state.bot = create_chatbot(retriever = st.session_state.vs, mode = mode)
            clean_prod_workspace(tmp_route)
    
    if uploaded_file and 'vs' in st.session_state:
        # user's question text input widget
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input('Ask one or more questions about the content of the uploaded data:', key='text_input')
        if prompt:
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            answer = st.session_state.bot({"question":prompt})["answer"]
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        if st.session_state.text_input:
            st.button('Start again from new context', on_click=start_over_with_new_document, key='new_question_new_context')

        # Display chat messages from history on app rerun
        # for message in st.session_state.messages:
        #     with st.chat_message(message["role"]):
        #         st.markdown(message["content"])

    #     q = st.text_input('Ask one or more questions about the content of the uploaded data:', key='text_input')
    #     if q:
    #         vector_store = st.session_state.vs
    #         answer = st.session_state.bot({"question":q})["answer"]
    #         print(answer)
    #         st.write(answer)

    #     if st.session_state.text_input:
    #         st.button('New question for new context', on_click=start_over_with_new_document, key='new_question_new_context')
    # else:
    #     st.info('Please upload one or more files to continue.')

        # if prompt := st.chat_input("What is up?"):
        #     with st.chat_message("user"):
        #         st.markdown(prompt)

if __name__ == "__main__":
    main()
