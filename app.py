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
# CONSENT + INSTRUCTIONS PAGE
# ============================================================

if "agreed" not in st.session_state:

    st.session_state.agreed = False

if not st.session_state.agreed:

    st.markdown(
        """
# Annotation Instructions | تعليمات المُقيِّم

## English

Thank you for taking part in this evaluation of Arabic image captioning systems. These instructions explain exactly what you will do. Please read it before starting.

### What you will see

For every image, you will see three Arabic captions, labelled A, B, and C. The captions were produced by three different captioning systems, but you do not know which caption came from which system. The order of A, B, and C is shuffled for each image.

### What you will do

For each image, you will rank the three captions on three things:

1. **Descriptive adequacy:** does the caption correctly describe what is visible in the image (objects, scene, action)?
2. **Affective appropriateness:** does the emotion or sentiment expressed by the caption fit the image's affective content?
3. **Fluency:** is the caption grammatical and natural-sounding Arabic?

For each of these three things, give a rank from 1 (best) to 3 (worst).

Ties are allowed. If two captions are equally good (or equally bad) on a dimension, give them the same rank.

Rank each dimension separately. The same caption can be the best on Language and the worst on Emotion. That is fine and expected.

### Things to keep in mind

- Look at the image first.
- Read all three captions before ranking.
- Keep the three dimensions separate.
- Trust your own reading of the image.
- First impression is the right impression.

### Things to ignore

- Caption length.
- Which system produced which caption.
- Your personal style preferences.

### Frequently asked questions

**What if I cannot decide between two captions?**  
Use a tie.

**What if all three captions are bad?**  
Rank them anyway.

**What if the image's emotion is genuinely unclear?**  
Use whichever reading feels most natural to you.

**How long should I spend on each image?**  
About three to five minutes is typical.

Thank you again for your careful work.

---

<div dir="rtl" style="text-align: right;">


# تعليمات المُقيِّم

شكرا لمشاركتك في تقييم أنظمة توليد الأوصاف العربية للصور. توضح هذه التعليمات بدقة ما هو مطلوب منك. يُرجى قراءتها قبل البدء.

## ما الذي ستراه

في كل صورة، ستظهر لك ثلاثة أوصاف باللغة العربية، مُعلمة بالأحرف A وB وC. أُنتجت هذه الأوصاف بواسطة ثلاثة أنظمة مختلفة لتوليد الأوصاف، لكنك لا تعلم أي وصف يخص أي نظام. ترتيب الأحرف A وB وC يُعاد خلطه عشوائيا في كل صورة.

## ما المطلوب منك

لكل صورة، سترتب الأوصاف الثلاثة وفق ثلاثة معايير:

1. **الملاءمة الوصفية:** هل ينقل الوصف بدقة ما يظهر في الصورة من أشياء ومشاهد وأفعال؟
2. **الملاءمة العاطفية:** هل تتناسب العاطفة أو الشعور الذي يعبّر عنه الوصف مع المحتوى العاطفي للصورة؟
3. **الطلاقة:** هل الوصف مصاغ بعربية سليمة نحويًّا وطبيعية الأسلوب؟

لكل معيار من هذه المعايير الثلاثة، أعطِ رتبة من 1 (الأفضل) إلى 3 (الأسوأ).

التعادل مسموح به. إذا تساوى وصفان في الجودة (أو في الرداءة) على معيار ما، فأعطهما الرتبة نفسها.

رتب كل معيار على حدة. قد يكون الوصف نفسه الأفضل من حيث اللغة والأسوأ من حيث العاطفة، وهذا أمر طبيعي ومتوقع.

## نقاط ينبغي مراعاتها

• انظر إلى الصورة أولا. كوِن انطباعك الخاص حول محتوى الصورة وما تثيره من شعور قبل قراءة الأوصاف.

• اقرأ الأوصاف الثلاثة كاملة قبل الترتيب. هذه عملية مقارنة.

• احرص على استقلال المعايير الثلاثة. لا تدع تميُز الوصف في معيار واحد يدفعك إلى ترتيبه عاليا في المعايير الأخرى.

• ثِق بقراءتك الخاصة للصورة. لا توجد عاطفة "صحيحة" ثابتة لأي صورة، إدراكك الشخصي للصورة هو المرجع.

• الانطباع الأول هو الانطباع الصحيح. لا تعُد إلى الترتيبات السابقة لمراجعتها.

## نقاط ينبغي تجاهلها

• طول الوصف. الوصف القصير ليس بالضرورة أسوأ من الطويل، والعكس صحيح.

• النظام الذي أنتج كل وصف. أنت لا تعلمه، ولا ينبغي محاولة تخمينه.

• تفضيلاتك الأسلوبية الشخصية. رتب ما هو معروض أمامك، لا ما كنت ستكتبه أنت.

## أسئلة شائعة

**ماذا أفعل إذا تعذر علي تمييز الأفضلية بين وصفين؟**  
استخدم التعادل. التعادل جزء من المنهجية.

**ماذا أفعل إذا كانت الأوصاف الثلاثة كلها سيئة؟**  
رتبها على أي حال، الأقل سوءا يحصل على الرتبة 1، والتعادل مسموح إذا تساوى أكثر من وصف في السوء.

**ماذا أفعل إذا كانت عاطفة الصورة غامضة فعلا؟**  
اعتمد على القراءة التي تبدو لك أكثر طبيعية. قد يقرأ المقيمون المختلفون الصورة نفسها بطرق مختلفة، وهذا أمر متوقع.

**كم من الوقت ينبغي أن أمضي على كل صورة؟**  
ما بين ثلاث وخمس دقائق هو المعتاد. إذا وجدت نفسك تستغرق وقتا أطول بكثير، فقدم أفضل حكم لديك وانتقل إلى الصورة التالية.

شكرا مجددا على دقتك في العمل.

</div>
""",
        unsafe_allow_html=True
    )

    agree = st.checkbox(
        "I have read the instructions and agree to participate. | أوافق على المشاركة بعد قراءة التعليمات."
    )

    if agree:

        if st.button("Start Evaluation"):

            st.session_state.agreed = True

            st.rerun()

    st.stop()

# ============================================================
# ANNOTATOR ID
# ============================================================

if "annotator_id" not in st.session_state:

    st.session_state.annotator_id = ""

if st.session_state.annotator_id == "":

    annotator_input = st.text_input(
        "Annotator ID | رقم المقيّم"
    )

    if annotator_input != "":

        results_file_check = (
            f"results_{annotator_input}.csv"
        )

        if os.path.exists(results_file_check):

            st.error(
                "This annotator ID already exists.\n\n"
                "رقم المقيّم مستخدم مسبقاً."
            )

            st.stop()

        else:

            st.session_state.annotator_id = (
                annotator_input
            )

            st.rerun()

    st.stop()

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

    if os.path.exists(results_file):

        with open(results_file, "rb") as file:

            st.download_button(

                label="Download Results CSV",

                data=file,

                file_name=results_file,

                mime="text/csv"
            )

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

    results[f"caption_{label}_system"] = (
        caption_data["system"]
    )

    desc = st.selectbox(

        f"Descriptive Adequacy - Caption {label}",

        ["Select",1,2,3],

        key=f"desc_{st.session_state.current_index}_{label}"
    )

    affect = st.selectbox(

        f"Affective Appropriateness - Caption {label}",

        ["Select",1,2,3],

        key=f"affect_{st.session_state.current_index}_{label}"
    )

    fluency = st.selectbox(

        f"Fluency - Caption {label}",

        ["Select",1,2,3],

        key=f"fluency_{st.session_state.current_index}_{label}"
    )

    results[f"desc_{label}"] = desc

    results[f"affect_{label}"] = affect

    results[f"fluency_{label}"] = fluency

# ============================================================
# NEXT BUTTON
# ============================================================

if st.button("Next Image"):

    missing_fields = []

    for label in labels:

        if st.session_state[
            f"desc_{st.session_state.current_index}_{label}"
        ] == "Select":

            missing_fields.append(label)

        if st.session_state[
            f"affect_{st.session_state.current_index}_{label}"
        ] == "Select":

            missing_fields.append(label)

        if st.session_state[
            f"fluency_{st.session_state.current_index}_{label}"
        ] == "Select":

            missing_fields.append(label)

    if len(missing_fields) > 0:

        st.error(
            "Please complete all fields before continuing."
        )

        st.stop()

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

    st.session_state.current_index += 1

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
