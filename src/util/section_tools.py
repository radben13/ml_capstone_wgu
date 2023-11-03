import streamlit as st


def init_sections(sections):
    for section in sections:
        if section not in st.session_state:
            st.session_state[section] = False

def toggle_section(section_key: str):
    if section_key in st.session_state:
        st.session_state[section_key] = not st.session_state[section_key]
    else:
        st.session_state[section_key] = True

def create_section_button(section: str, sections: dict):
    l = {}
    exec(f"def toggle_{section}():\n\ttoggle_section('{section}')", None, l)
    listener = l[f'toggle_{section}']
    if not st.session_state[section]:
        st.button(f'View {sections[section]}', on_click=listener)
    else:
        st.button(f'Close {sections[section]}', on_click=listener)