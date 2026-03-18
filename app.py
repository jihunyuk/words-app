import streamlit as st
from data import word_data as raw_word_data

APP_TITLE = "Words"
APP_SUBTITLE = "학원 영단어 앱"

APP_VERSION = "0.0.1"
DEVELOPER = "Jihun Yuk"

TOTAL_PAGES = 20


@st.cache_data
def load_word_data():
    return raw_word_data

word_data = load_word_data()


def init_session_state():
    if "show_all_meanings" not in st.session_state:
        st.session_state.show_all_meanings = False
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "page_1"


def get_page_options():
    options = []
    for i in range(1, TOTAL_PAGES + 1):
        page_key = f"page_{i}"
        if page_key in word_data:
            options.append(page_key)
    return options


def format_page_label(page_key: str) -> str:
    page_num = page_key.split("_")[1]
    return f"Page {page_num}"


def render_word_card(page_key: str, number: int, word: str, meaning: str):
    with st.expander(f"**{number}.** {word}", expanded=st.session_state.show_all_meanings):
        search_url = f"https://www.google.com/search?q={word}+발음"
        html_content = f'''
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 12px 16px; 
                    background-color: var(--secondary-background-color); 
                    border-radius: 8px;">
            <div style="margin-right: 12px;">{meaning}</div>
            <a href="{search_url}" target="_blank" style="
                padding: 6px 12px;
                color: white;
                background-color: #424242;
                text-decoration: none;
                border-radius: 6px;
                font-size: 14px;
                white-space: nowrap;
            ">발음 🔊</a>
        </div>
        '''
        st.markdown(html_content, unsafe_allow_html=True)


def render_footer():
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: right; font-size: 12px; color: gray;">
        © 2026 {DEVELOPER} · v{APP_VERSION}
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="📘",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    page_options = get_page_options()

    if not page_options:
        st.error("data.py에서 word_data를 찾을 수 없거나 비어 있습니다.")
        st.stop()

    with st.sidebar:
        st.header("단어장 선택")

        for page_key in page_options:
            page_num = page_key.split("_")[1]
            is_active = st.session_state.selected_page == page_key
            if st.button(
                f"Page {page_num}",
                key=f"select_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.selected_page = page_key
                st.rerun()

        selected_page = st.session_state.selected_page

        st.divider()

        st.header("설정")

        show_all = st.checkbox(
            "전체 뜻 보기",
            value=st.session_state.show_all_meanings,
        )
        st.session_state.show_all_meanings = show_all

    items = list(word_data.get(selected_page, {}).items())

    st.subheader(f"{format_page_label(selected_page)} 단어장")
    st.caption(f"총 {len(items)}개 표시")

    if not items:
        st.warning("표시할 단어가 없습니다.")
        return

    for number, (word, meaning) in items:
        render_word_card(selected_page, number, word, meaning)

    render_footer()


if __name__ == "__main__":
    main()