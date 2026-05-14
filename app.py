import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Arabic Caption Evaluation",
    layout="centered"
)

# ============================================================
# REDUCE TOP SPACE
# ============================================================

st.markdown(
    """
    <style>
    section.main > div {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# TITLE
# ============================================================

st.title("Arabic Caption Human Evaluation")

# ============================================================
# INSTRUCTIONS
# ============================================================

st.markdown("""
# Evaluation Dimensions | أبعاد التقييم

### English

- **Descriptive adequacy:**  
Does the caption correctly describe what is visible in the image (objects, scene, action)?

- **Affective appropriateness:**  
Does the emotion or sentiment expressed by the caption fit the image's affective content?

- **Fluency:**  
Is the caption grammatical and natural-sounding Arabic?

---

### العربية

- **الملاءمة الوصفية:**  
هل يصف النص ما يظهر في الصورة بشكل صحيح من حيث العناصر والمشهد والأفعال؟

- **الملاءمة العاطفية:**  
هل يتناسب الشعور أو العاطفة التي يعبر عنها الوصف مع المحتوى العاطفي للصورة؟

- **الطلاقة اللغوية:**  
هل الوصف مكتوب بلغة عربية سليمة وطبيعية؟

---

### Ranking Guide | دليل الترتيب

- 1 = Best | الأفضل
- 2 = متوسط
- 3 = Worst | الأضعف

Ties are allowed (e.g., 1, 1, 2 if two captions are equally good).  
يسمح بالتساوي في التقييم (مثال: 1، 1، 2 إذا كان هناك وصفان بنفس الجودة).
""")

# ============================================================
# ANNOTATOR ID
# ============================================================

if "annotator_id" not in st.session_state:

    st.session_state.annotator_id = ""

# ------------------------------------------------------------
# INPUT ONLY IF EMPTY
# ------------------------------------------------------------

if st.session_state.annotator_id == "":

    annotator_input = st.text_input(
        "Annotator ID | رقم المقيّم"
    )

    if annotator_input != "":

        results_file_check = (
            f"results_{annotator_input}.csv"
        )

        # ----------------------------------------------------
        # CHECK DUPLICATE
        # ----------------------------------------------------

        if os.path.exists(results_file_check):

            st.error(
                "This annotator ID already exists. Please use a different ID.\n\n"
                "رقم المقيّم مستخدم مسبقاً. الرجاء استخدام رقم مختلف."
            )

            st.stop()

        else:

            st.session_state.annotator_id = (
                annotator_input
            )

            st.rerun()

    st.stop()

# ------------------------------------------------------------
# USE SAVED ANNOTATOR ID
# ------------------------------------------------------------

annotator_id = (
    st.session_state.annotator_id
)

results_file = (
    f"results_{annotator_id}.csv"
)

st.success(
    f"Annotator ID: {annotator_id}"
)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    "selected_examples_clean.csv"
)

# ============================================================
# SESSION STATE
# ============================================================

if "current_index" not in st.session_state:

    st.session_state.current_index = 0

# ============================================================
# FINISHED
# ============================================================

if st.session_state.current_index >= len(df):

    st.success("تم الانتهاء من التقييم. شكراً لك.")

    st.stop()

# ============================================================
# CURRENT ROW
# ============================================================

row = df.iloc[
    st.session_state.current_index
]

# ============================================================
# IMAGE
# ============================================================

image_path = row["image_path"]

st.image(image_path, width=500)

# ============================================================
# PREPARE CAPTIONS
# ============================================================

captions = [

    {
        "system": "baseline",
        "text": row["baseline"]
    },

    {
        "system": "vad",
        "text": row["vad"]
    },

    {
        "system": "emotion",
        "text": row["emotion"]
    }
]

# ============================================================
# RANDOMIZE ONLY ONCE PER IMAGE
# ============================================================

shuffle_key = f"shuffle_{st.session_state.current_index}"

if shuffle_key not in st.session_state:

    random.shuffle(captions)

    st.session_state[shuffle_key] = captions

captions = st.session_state[shuffle_key]

labels = ["A", "B", "C"]

# ============================================================
# RESULTS STORAGE
# ============================================================

results = {

    "annotator_id":
    annotator_id,

    "painting":
    row["painting"]
}

# ============================================================
# SHOW CAPTIONS
# ============================================================

for label, caption_data in zip(labels, captions):

    st.markdown("---")

    st.subheader(f"Caption {label}")

    st.write(caption_data["text"])

    # --------------------------------------------------------
    # SAVE TRUE SYSTEM MAPPING
    # --------------------------------------------------------

    results[f"caption_{label}_system"] = (
        caption_data["system"]
    )

    # ========================================================
    # DESCRIPTIVE ADEQUACY
    # ========================================================

    desc = st.selectbox(

        f"Descriptive Adequacy | الملاءمة الوصفية - Caption {label}",

        ["Select",1,2,3],

        key=f"desc_{st.session_state.current_index}_{label}"
    )

    # ========================================================
    # AFFECTIVE APPROPRIATENESS
    # ========================================================

    affect = st.selectbox(

        f"Affective Appropriateness | الملاءمة العاطفية - Caption {label}",

        ["Select",1,2,3],

        key=f"affect_{st.session_state.current_index}_{label}"
    )

    # ========================================================
    # FLUENCY
    # ========================================================

    fluency = st.selectbox(

        f"Fluency | الطلاقة اللغوية - Caption {label}",

        ["Select",1,2,3],

        key=f"fluency_{st.session_state.current_index}_{label}"
    )

    # --------------------------------------------------------
    # SAVE SCORES
    # --------------------------------------------------------

    results[f"desc_{label}"] = desc

    results[f"affect_{label}"] = affect

    results[f"fluency_{label}"] = fluency

# ============================================================
# NEXT BUTTON
# ============================================================

if st.button("Next Image"):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    missing_fields = []

    for label in labels:

        if st.session_state[
            f"desc_{st.session_state.current_index}_{label}"
        ] == "Select":

            missing_fields.append(
                f"Descriptive - {label}"
            )

        if st.session_state[
            f"affect_{st.session_state.current_index}_{label}"
        ] == "Select":

            missing_fields.append(
                f"Affective - {label}"
            )

        if st.session_state[
            f"fluency_{st.session_state.current_index}_{label}"
        ] == "Select":

            missing_fields.append(
                f"Fluency - {label}"
            )

    # --------------------------------------------------------
    # STOP IF MISSING
    # --------------------------------------------------------

    if len(missing_fields) > 0:

        st.error(
            "Please complete all dropdown fields before continuing.\n\n"
            "الرجاء تعبئة جميع الحقول قبل المتابعة."
        )

        st.stop()

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    results_df = pd.DataFrame([results])

    file_exists = os.path.isfile(
        results_file
    )

    results_df.to_csv(

        results_file,

        mode="a",

        header=not file_exists,

        index=False
    )

    # --------------------------------------------------------
    # NEXT IMAGE
    # --------------------------------------------------------

    st.session_state.current_index += 1

    # --------------------------------------------------------
    # SCROLL TO TOP
    # --------------------------------------------------------

    components.html(
        """
        <script>
            window.parent.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        </script>
        """,
        height=0
    )

    st.rerun()

# ============================================================
# DOWNLOAD RESULTS
# ============================================================

if os.path.exists(results_file):

    with open(results_file, "rb") as file:

        st.download_button(

            label="Download Results CSV",

            data=file,

            file_name=results_file,

            mime="text/csv"
        )
