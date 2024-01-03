import streamlit as st
from db import fetch_data, school_count
from db.db_schema import School


st.set_page_config(layout="wide")

order = st.session_state.get("ordering")
tmp = fetch_data(st.session_state.get("page") or 0, getattr(School,order) if order else School.id)
st.dataframe(tmp, use_container_width=True, hide_index=True, height=750)
st.slider(
    'Select a range of values',
    0,
    school_count(),
    st.session_state.get("page") or 0,
    1,
    key = "page"
)
st.selectbox("which column order by",["id","name","total_absolvents","faculty","program"], key="ordering")
