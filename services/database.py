import streamlit as st
from services.database import add_subject, get_subjects
from services.database import DatabaseAPIError

subject_name = st.text_input("Enter subject name")

if st.button("Add Subject"):
    try:
        subject = add_subject(subject_name)
        st.success(f"Added {subject['name']} successfully!")
        st.rerun()
    except DatabaseAPIError as error:
        st.error(str(error))

try:
    subjects = get_subjects()
    st.write("Your subjects:", subjects)
except DatabaseAPIError as error:
    st.error(str(error))
