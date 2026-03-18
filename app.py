import streamlit as st
from data import word_data

APP_TITLE = "Words"
APP_SUBTITLE = "학원 영단어 앱"

APP_VERSION = "0.0.1"
DEVELOPER = "Jihun Yuk"

TOTAL_PAGES = 20


def init_session_state():
    if "show_all_meanings" not in st.session_state:
        st.session_state.show_all_meanings = False
    if "revealed_words" not in st.session_state:
        st.session_state.revealed_words = set()
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "page_1"


def toggle_word(word_id: str):
    if word_id in st.session_state.revealed_words:
        st.session_state.revealed_words.remove(word_id)
    else:
        st.session_state.revealed_words.add(word_id)


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
    word_id = f"{page_key}_{number}"
    is_revealed = (
        st.session_state.show_all_meanings
        or word_id in st.session_state.revealed_words
    )

    with st.container(border=True):
        st.markdown(f"### {number}. {word}")

        label = meaning if is_revealed else "뜻 보기"
        if st.button(label, key=f"btn_{word_id}", use_container_width=True, type="secondary" if not is_revealed else "primary"):
            toggle_word(word_id)
            st.rerun()


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
        st.header("설정")

        show_all = st.checkbox(
            "전체 뜻 보기",
            value=st.session_state.show_all_meanings,
        )
        st.session_state.show_all_meanings = show_all

        if st.button("현재 페이지 펼친 뜻 초기화", use_container_width=True):
            prefix = f"{st.session_state.selected_page}_"
            st.session_state.revealed_words = {
                x for x in st.session_state.revealed_words if not x.startswith(prefix)
            }
            st.rerun()

    # Page selection grid in main area
    st.markdown("### 단어장 선택")
    for i in range(0, len(page_options), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(page_options):
                page_key = page_options[i + j]
                page_num = page_key.split("_")[1]
                is_active = st.session_state.selected_page == page_key
                if cols[j].button(
                    f"Page {page_num}",
                    key=f"select_{page_key}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state.selected_page = page_key
                    st.rerun()

    selected_page = st.session_state.selected_page
    st.divider()

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