import streamlit as st
from utils import clean_prod_workspace, create_vector_database_from_pdf, answer_a_question

def main() -> None:
    """
    Main of the Streamlit app. 
    """
    st.title("Chat with your documents")
    st.write("Upload your document and start chatting!")

    with st.sidebar:
        st.title("Upload a document to interact with")
        uploaded_file = st.file_uploader("Upload a document", type=["pdf"])

        if uploaded_file is not None:
            tmp_route = "./src/frontend/tmp"
            clean_prod_workspace(tmp_route)
            file_name = f"{tmp_route}/{uploaded_file.name}"
            # Guardar el documento en el servidor
            with open(file_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("Document uploaded successfully!")

            retriever = create_vector_database_from_pdf(file_name)
    
    if uploaded_file is not None:
        # user's question text input widget
        q = st.text_input('Ask one or more questions about the content of the uploaded data:', key='text_input')
        if q:
            answer = answer_a_question(q, retriever)
            st.text_area('LLM Answer: ', value=answer, height=200)

if __name__ == "__main__":
    main()
