import streamlit as st
from utils import clean_prod_workspace, create_vector_database_from_pdf, answer_a_question

def start_over_with_new_document():
    st.session_state.text_input = ''
    # delete the vector store from the session state
    del st.session_state.vs
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

        if uploaded_file and st.button("Start chatting!"):
            tmp_route = "./src/frontend/tmp"
            clean_prod_workspace(tmp_route)
            file_name = f"{tmp_route}/{uploaded_file.name}"
            # Guardar el documento en el servidor
            with open(file_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("Document uploaded successfully!")

            st.session_state.vs = create_vector_database_from_pdf(file_name)
            clean_prod_workspace(tmp_route)
    
    if uploaded_file and 'vs' in st.session_state:
        # user's question text input widget
        q = st.text_input('Ask one or more questions about the content of the uploaded data:', key='text_input')
        if q:
            vector_store = st.session_state.vs
            answer = answer_a_question(q, vector_store)["answer"]
            st.write(answer)

        if st.session_state.text_input:
            st.button('New question for new context', on_click=start_over_with_new_document, key='new_question_new_context')
    else:
        st.info('Please upload one or more files to continue.')

        # if prompt := st.chat_input("What is up?"):
        #     with st.chat_message("user"):
        #         st.markdown(prompt)

if __name__ == "__main__":
    main()
