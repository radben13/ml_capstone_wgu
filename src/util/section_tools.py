import streamlit as st

def init_sections(sections):
    for section in sections:
        if section not in st.session_state:
            st.session_state[section] = False

def toggle_section(section_key: str, sections):
    if st.session_state.get(section_key):
        st.session_state[section_key] = not st.session_state[section_key]
    else:
        st.session_state[section_key] = True
    if st.session_state[section_key]:
        for s in sections:
            if s != section_key and st.session_state.get(s):
                st.session_state[s] = not st.session_state[s]

def create_section_button(section: str, sections: dict):
    l = {}
    g = { 'sections': sections, 'toggle_section': toggle_section }
    exec(f"def toggle_{section}():\n\ttoggle_section('{section}', sections)", g, l)
    listener = l[f'toggle_{section}']
    if not st.session_state[section]:
        st.button(f'View {sections[section]}', on_click=listener)
    else:
        st.button(f'Close {sections[section]}', on_click=listener)
