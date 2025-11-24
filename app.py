import streamlit as st
import os
import glob
from io import BytesIO

from auth import init_db, register_user, validate_user
from utils import extract_pdf_text, export_docx, export_pdf, export_ppt
from nlp import (
    summarize_text,
    section_wise_summaries,
    create_question_bank,
    create_written_answer_questions,
    create_ppt_outline,
    generate_group_assignments,
)

# ============= SETUP =============

st.set_page_config(page_title="EDUSAGE - AI Academic Assistant", layout="centered")

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: rgba(255,255,255,0.60) !important;
    backdrop-filter: blur(8px); /* optional */
}
</style>
""", unsafe_allow_html=True)

EDUSAGE_LOGO = "https://image2url.com/images/1763825773250-0afd41d5-3ff1-4df3-93d6-ffe830917499.png"
SIDEBAR_USER_LOGO ="https://image2url.com/images/1763825442048-d6224662-c0f0-4db6-aa5f-8c39baf6e524.png"
local_css("styles.css")

LOGIN_BG = "https://i.pinimg.com/originals/95/fc/9d/95fc9d6faecd2ecc13b1179ae07b3755.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{LOGIN_BG}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "generated" not in st.session_state:
    st.session_state.generated = {
        "notes": None,
        "ppt": None,
        "questions_mcq": None,
        "questions_written": None,
        "sections": None,
        "assignments": None,
    }
if "modal_content" not in st.session_state:
    st.session_state.modal_content = None
if "modal_title" not in st.session_state:
    st.session_state.modal_title = ""
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

def save_user_file(filename: str, content) -> str:
    user_dir = f"user_files/{st.session_state.username}"
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, filename)
    if isinstance(content, BytesIO):
        with open(path, "wb") as f:
            f.write(content.getvalue())
    else:
        if isinstance(content, (bytes, bytearray)):
            with open(path, "wb") as f:
                f.write(content)
        else:
            try:
                data = content.read()
                with open(path, "wb") as f:
                    f.write(data)
            except Exception:
                with open(path, "wb") as f:
                    f.write(str(content).encode("utf-8"))
    return path

def list_user_files():
    user_dir = f"user_files/{st.session_state.username}"
    os.makedirs(user_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(user_dir, "*")))
    return files

def show_preview_modal(title: str, content: str):
    st.session_state.modal_title = title
    st.session_state.modal_content = content
    st.session_state.show_modal = True
    st.rerun()

def login_register_ui():
    st.markdown(f'<img src="{EDUSAGE_LOGO}" width="300" style="display:block;margin:auto;margin-bottom:20px"/>', unsafe_allow_html=True)
    tabs = st.tabs(["Sign In", "Create account"])
    with tabs[0]:
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
        if st.button("Sign In", key="login_btn"):
            username = validate_user(email, password)
            if username:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")
    with tabs[1]:
        username_input = st.text_input("Full Name", key="reg_username", placeholder="John Doe")
        email_reg = st.text_input("Email", key="register_email", placeholder="you@example.com")
        password_reg = st.text_input("Password", type="password", key="register_pass", placeholder="Choose a password")
        if st.button("Create account", key="register_btn"):
            success = register_user(email_reg, password_reg, username_input)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.rerun()
            else:
                st.error("❌ Email already exists.")
    st.stop()

if not st.session_state.logged_in:
    login_register_ui()

with st.sidebar:
    st.image(SIDEBAR_USER_LOGO, width=100)
    st.markdown(f"## {st.session_state.username or 'User'}")
    st.markdown("---")
    st.markdown("### 📂 Previous Files")

    user_files_dir = f"user_files/{st.session_state.username}"
    os.makedirs(user_files_dir, exist_ok=True)
    user_files = sorted(os.listdir(user_files_dir))

    if not user_files:
        st.info("No Files Yet.")
    else:
        for file in user_files:
            file_path = os.path.join(user_files_dir, file)
            with st.expander(f"📄 {file}", expanded=False):
                try:
                    if file.lower().endswith((".txt", ".md", ".py", ".csv")):
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        st.text_area("Preview", content, height=150, disabled=True)
                except Exception:
                    st.warning("Could not load file content.")

                with open(file_path, "rb") as f:
                    st.download_button("⬇️ Download", f, file_name=file, key=f"download_{file}")

                new_name = st.text_input("Rename file", value=file, key=f"rename_{file}")
                if st.button("Save New Name", key=f"save_rename_{file}"):
                    new_path = os.path.join(user_files_dir, new_name)
                    if os.path.exists(new_path):
                        st.warning("A file with that name already exists!")
                    else:
                        os.rename(file_path, new_path)
                        st.success("Renamed!")
                        st.rerun()

                if st.button("Delete", key=f"delete_{file}"):
                    os.remove(file_path)
                    st.success("File deleted!")
                    st.rerun()

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown(f'<img src="{EDUSAGE_LOGO}" width="270" style="display:block;margin:auto;margin-bottom:20px"/>', unsafe_allow_html=True)
st.markdown(
    """
    <p style="text-align:center;color:#F08080;font-size:14px;font-family:'Open Sans',sans-serif;">Get clean notes, structured PPTs, question banks and section summaries — all from your uploaded PDF.</p>
    """, unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
pdf_text = None

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_pdf_text(uploaded_file)
    st.success("PDF extracted successfully!")

if pdf_text:
    st.markdown("""
    <div style='text-align:center; font-size:1.4rem; font-family:Montserrat, sans-serif; color:#d8572a; margin-bottom:15px; margin-top:10px; letter-spacing:1px;'>
    ✨ Choose Your Magic Academic Tool Below ✨
    </div>
    """, unsafe_allow_html=True)

    # Summary Notes
    st.markdown('<hr style="height:1px;border:none;color:#bbb;background-color:#bbb;" />', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    cols = st.columns([8, 2])
    with cols[0]:
        st.subheader("📄 Summary Notes")
    with cols[1]:
        if not st.session_state.generated.get("notes"):
            if st.button("Generate", key="gen_notes"):
                with st.spinner("Generating summary notes..."):
                    notes = summarize_text(pdf_text)
                    st.session_state.generated["notes"] = notes
                    try:
                        save_user_file("notes.docx", export_docx(notes))
                    except Exception:
                        pass
                    st.success("Notes generated.")
                    st.rerun()
        else:
            if st.button("🔍 Preview", key="preview_notes_btn"):
                show_preview_modal("📄 Summary Notes Preview", st.session_state.generated["notes"])
    notes = st.session_state.generated.get("notes")
    if notes:
        for f in list_user_files():
            if f.endswith("notes.docx"):
                with open(f, "rb") as fh:
                    st.download_button("Download DOCX", fh, file_name="notes.docx")
                break
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr style="height:1px;border:none;color:#bbb;background-color:#bbb;" />', unsafe_allow_html=True)

    # Presentation Slides
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    cols = st.columns([8, 2])
    with cols[0]:
        st.subheader("📅 Presentation Slides")
    with cols[1]:
        if not st.session_state.generated.get("ppt"):
            if st.button("Generate", key="gen_ppt"):
                with st.spinner("Generating PPT outline..."):
                    ppt_text = create_ppt_outline(pdf_text)
                    st.session_state.generated["ppt"] = ppt_text
                    try:
                        save_user_file("slides.pptx", export_ppt(ppt_text))
                    except Exception:
                        pass
                    st.success("PPT outline generated.")
                    st.rerun()
        else:
            if st.button("🔍 Preview", key="preview_ppt_btn"):
                show_preview_modal("📅 PPT Outline Preview", st.session_state.generated["ppt"])
    ppt_text = st.session_state.generated.get("ppt")
    if ppt_text:
        for f in list_user_files():
            if f.endswith("slides.pptx"):
                with open(f, "rb") as fh:
                    st.download_button("Download PPTX", fh, file_name="slides.pptx")
                break
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr style="height:1px;border:none;color:#bbb;background-color:#bbb;" />', unsafe_allow_html=True)

    # Research Summary
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    cols = st.columns([8, 2])
    with cols[0]:
        st.subheader("📚 Research Summary")
    with cols[1]:
        if not st.session_state.generated.get("sections"):
            if st.button("Generate", key="gen_sec"):
                with st.spinner("Generating section summaries..."):
                    sec_text = section_wise_summaries(pdf_text)
                    st.session_state.generated["sections"] = sec_text
                    try:
                        save_user_file("section_summaries.pdf", export_pdf(sec_text))
                    except Exception:
                        pass
                    st.success("Section summaries generated.")
                    st.rerun()
        else:
            if st.button("🔍 Preview", key="preview_sections_btn"):
                show_preview_modal("📚 Research Summary Preview", st.session_state.generated["sections"])
    sec_text = st.session_state.generated.get("sections")
    if sec_text:
        for f in list_user_files():
            if f.endswith("section_summaries.pdf"):
                with open(f, "rb") as fh:
                    st.download_button("Download PDF", fh, file_name="section_summaries.pdf")
                break
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr style="height:1px;border:none;color:#bbb;background-color:#bbb;" />', unsafe_allow_html=True)

    # Question Bank
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    cols = st.columns([8, 2])
    with cols[0]:
        st.subheader("🧾 Question Bank")
        qtype = st.radio("Type", ["MCQs", "Written"], key="qtype_radio")
        key_name = "questions_mcq" if qtype == "MCQs" else "questions_written"
    with cols[1]:
        if not st.session_state.generated.get(key_name):
            if st.button("Generate", key="gen_questions"):
                with st.spinner("Generating questions..."):
                    if qtype == "MCQs":
                        qtext = create_question_bank(pdf_text)
                    else:
                        qtext = create_written_answer_questions(pdf_text)
                    st.session_state.generated[key_name] = qtext
                    fname = "questions.docx" if qtype == "MCQs" else "written_answer_questions.docx"
                    try:
                        save_user_file(fname, export_docx(qtext))
                        if qtype == "Written":
                            save_user_file("written_answer_questions.pdf", export_pdf(qtext))
                    except Exception:
                        pass
                    st.success("Questions generated.")
                    st.rerun()
        else:
            if st.button("🔍 Preview", key="preview_questions_btn"):
                show_preview_modal(f"🧾 {qtype} Preview", st.session_state.generated[key_name])
    qtext = st.session_state.generated.get(key_name)
    if qtext:
        for f in list_user_files():
            if qtype == "MCQs" and f.endswith("questions.docx"):
                with open(f, "rb") as fh:
                    st.download_button("Download MCQs (DOCX)", fh, file_name="questions.docx")
                break
            if qtype == "Written" and f.endswith("written_answer_questions.docx"):
                with open(f, "rb") as fh:
                    st.download_button("Download Written (DOCX)", fh, file_name="written_answer_questions.docx")
                break
        if qtype == "Written":
            pdfs = [x for x in list_user_files() if x.endswith("written_answer_questions.pdf")]
            if pdfs:
                with open(pdfs[0], "rb") as pf:
                    st.download_button("Download Written (PDF)", pf, file_name="written_answer_questions.pdf")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr style="height:1px;border:none;color:#bbb;background-color:#bbb;" />', unsafe_allow_html=True)

    # Assignment Generator
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    cols = st.columns([8, 2])
    with cols[0]:
        st.subheader("📝 Assignment Generator")
    with cols[1]:
        if not st.session_state.generated.get("assignments"):
            if st.button("Generate", key="gen_assignments"):
                with st.spinner("Creating assignments..."):
                    assignments = generate_group_assignments(pdf_text)
                    st.session_state.generated["assignments"] = assignments
                    try:
                        save_user_file("assignments_all_groups.docx", export_docx(assignments))
                        save_user_file("assignments_all_groups.pdf", export_pdf(assignments))
                    except Exception:
                        pass
                    st.success("Assignments ready.")
                    st.rerun()
        else:
            if st.button("🔍 Preview", key="preview_assignments_btn"):
                show_preview_modal("📝 Assignment Generator Preview", st.session_state.generated["assignments"])
    ass_text = st.session_state.generated.get("assignments")
    if ass_text:
        for f in list_user_files():
            if f.endswith("assignments_all_groups.docx"):
                with open(f, "rb") as fh:
                    st.download_button("Download DOCX", fh, file_name="assignments_all_groups.docx")
                break
        pdfs = [x for x in list_user_files() if x.endswith("assignments_all_groups.pdf")]
        if pdfs:
            with open(pdfs[0], "rb") as pf:
                st.download_button("Download PDF", pf, file_name="assignments_all_groups.pdf")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<hr style="height:1px;border:none;color:#bbb;background-color:#bbb;" />', unsafe_allow_html=True)

    # MODAL POPUP (same as before)
    if st.session_state.get("show_modal") and st.session_state.get("modal_content"):
        with st.form(f"modal_form_{st.session_state.modal_title}"):
            st.markdown(f"""
            <h4 style="font-family:'Montserrat',sans-serif; color:#e53935; font-size:1.6rem; margin-bottom:10px;">
                {st.session_state.get('modal_title', '')}
            </h4>
            <div style="font-family:'Open Sans',sans-serif; font-size:1rem; color:#444; margin-bottom:18px;">
                {st.session_state.get('modal_content', '')}
            </div>
            """, unsafe_allow_html=True)
            submitted = st.form_submit_button("✕ Close")
            if submitted:
                st.session_state["show_modal"] = False
                st.session_state["modal_content"] = None
                st.session_state["modal_title"] = ""
                st.rerun()
else:
    st.info("📄 Upload a PDF to enable the generator.")
