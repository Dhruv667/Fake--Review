import streamlit as st
import re

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

def detect_fake_review(review_text):
    score = 0
    max_score = 100
    
    fake_keywords = {
        'extreme_positive': [
            'amazing', 'incredible', 'perfect', 'awesome', 'unbelievable', 'life-changing',
            'mind-blowing', 'spectacular', 'phenomenal', 'miraculous', 'exceptional',
            'extraordinary', 'outstanding', 'magnificent', 'brilliant', 'excellent',
            'wonderful', 'fantastic', 'terrific', 'superb', 'divine', 'heavenly',
            'marvelous', 'splendid', 'gorgeous', 'beautiful', 'stunning', 'breathtaking',
            'remarkable', 'impressive', 'astounding', 'astonishing', 'fabulous',
            'delightful', 'exquisite', 'tremendous', 'unmatched', 'supreme'
        ],
        'extreme_negative': [
            'worst', 'terrible', 'horrible', 'awful', 'disgusting', 'pathetic',
            'abysmal', 'atrocious', 'dreadful', 'appalling', 'vile', 'repulsive',
            'revolting', 'nauseating', 'sickening', 'heinous', 'deplorable',
            'abominable', 'hideous', 'monstrous', 'detestable', 'ghastly',
            'horrendous', 'nightmarish', 'disastrous', 'catastrophic'
        ],
        'urgency': [
            'must buy', 'everyone needs', 'don\'t miss', 'grab now', 'hurry',
            'rush', 'limited time', 'act fast', 'buy now', 'order now', 'get yours',
            'right now', 'don\'t wait', 'before it\'s gone', 'while supplies',
            'can\'t miss', 'asap', 'immediate', 'urgent', 'limited stock'
        ],
        'generic_praise': [
            'best product', 'best ever', 'changed my life', 'game changer', 'exceeded expectations',
            'beyond expectations', 'perfect fit', 'perfect product', 'highly recommend',
            'all my friends', 'everyone should buy', 'spread the word', 'amazing value',
            'steal of a deal', 'unbeatable price', 'can\'t believe the price'
        ],
        'marketing_speak': [
            'revolutionary', 'innovative', 'cutting edge', 'state of the art',
            'breakthrough', 'one of a kind', 'life-transforming', 'world-class',
            'premium quality', 'luxury', 'game-changing'
        ]
    }
    
    genuine_keywords = [
        'but', 'however', 'although', 'though', 'downside', 'issue', 'problem',
        'could improve', 'better if', 'wish it had', 'complaint', 'not perfect',
        'not ideal', 'somewhat', 'kind of', 'sort of', 'decent', 'okay', 'alright',
        'good enough', 'reliable', 'works well', 'works as expected', 'satisfactory',
        'fairly', 'rather', 'pretty good', 'not bad', 'average', 'mediocre', 'mixed',
        'pros and cons', 'depends', 'might not', 'may not', 'for some', 'after using',
        'after a week', 'after a month', 'quality is', 'build quality', 'material',
        'construction', 'design', 'specific', 'details', 'experience', 'personally',
        'in my opinion', 'in my experience', 'actually', 'took a while', 'learning curve'
    ]
    
    text_lower = review_text.lower()
    
    fake_count = 0
    for category, words in fake_keywords.items():
        for word in words:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                fake_count += 1
    
    genuine_count = 0
    for word in genuine_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            genuine_count += 1
    
    score += fake_count * 3
    score -= genuine_count * 4
    
    caps_count = sum(1 for c in review_text if c.isupper())
    caps_ratio = caps_count / len(review_text) if len(review_text) > 0 else 0
    if caps_ratio > 0.30:
        score += 15
    elif caps_ratio > 0.20:
        score += 10
    elif caps_ratio > 0.10:
        score += 5
    
    exclaim_count = review_text.count('!')
    if exclaim_count > 5:
        score += 12
    elif exclaim_count > 3:
        score += 8
    elif exclaim_count == 1:
        score += 0
    
    word_count = len(review_text.split())
    if word_count < 15:
        score += 10
    elif word_count < 30:
        score += 5
    elif word_count > 400:
        score += 3
    
    has_measurements = bool(re.search(r'\d+\s*(days?|weeks?|months?|years?|hours?|%)', review_text))
    if has_measurements:
        score -= 8
    
    confidence = max(0, min(100, score))
    
    if confidence > 65:
        prediction = "FAKE"
    elif confidence < 35:
        prediction = "GENUINE"
    else:
        prediction = "UNCERTAIN"
    
    return prediction, confidence

st.set_page_config(page_title="Review Authenticity Checker", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <div style='text-align: center; padding: 20px 0; margin-bottom: 30px;'>
        <h1 style='font-size: 2.5em; color: #3b82f6; margin: 0;'>🔍 Review Authenticity Checker</h1>
        <p style='color: #94a3b8; font-size: 1em; margin: 10px 0 0 0;'>Detect fake reviews with pattern analysis</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("### Enter Review Text")
review_input = st.text_area("Review", value=st.session_state.review_text, placeholder="Paste the review here...", height=100, label_visibility="collapsed")
st.session_state.review_text = review_input

col1, col2 = st.columns(2)
with col1:
    analyze_button = st.button("🔍 Analyze", use_container_width=True, key="analyze")
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True, key="clear")

if clear_button:
    st.session_state.review_text = ""
    st.rerun()

st.divider()

if analyze_button and review_input.strip():
    prediction, confidence = detect_fake_review(review_input)
    
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        if prediction == "GENUINE":
            st.success("✅ GENUINE")
        elif prediction == "FAKE":
            st.error("❌ FAKE")
        else:
            st.warning("⚠️ UNCERTAIN")
    with col2:
        st.metric("Confidence", f"{confidence:.0f}%")
    with col3:
        level = "High" if prediction == "GENUINE" else "Low"
        st.metric("Authenticity", level)
    
    st.progress(confidence / 100)
    
    st.divider()
    st.markdown("### 📊 Analysis Details")
    col_left, col_right = st.columns(2)
    with col_left:
        caps_ratio = sum(1 for c in review_input if c.isupper()) / len(review_input) if len(review_input) > 0 else 0
        st.write(f"**Capitalization:** {caps_ratio*100:.1f}%")
        st.write(f"**Exclamation marks:** {review_input.count('!')}")
        st.write(f"**Question marks:** {review_input.count('?')}")
        st.write(f"**Word count:** {len(review_input.split())}")
    with col_right:
        extreme_words = ['amazing', 'incredible', 'perfect', 'awesome', 'best', 'worst', 'terrible', 'horrible']
        extreme_count = sum(1 for w in extreme_words if re.search(r'\b' + w + r'\b', review_input.lower()))
        st.write(f"**Extreme words found:** {extreme_count}")
        genuine_words = ['but', 'however', 'problem', 'issue', 'downside', 'complaint', 'not perfect']
        genuine_count = sum(1 for w in genuine_words if re.search(r'\b' + w + r'\b', review_input.lower()))
        st.write(f"**Balanced language indicators:** {genuine_count}")
        has_details = bool(re.search(r'\d+\s*(days?|weeks?|months?|hours?|%)', review_input))
        st.write(f"**Specific timeframe/details:** {'Yes' if has_details else 'No'}")
    st.divider()
    if prediction == "FAKE":
        st.error("**🚨 This review appears FAKE**\n\nRed flags: Extreme language • Generic phrases • Unnatural patterns")
    elif prediction == "GENUINE":
        st.success("**✅ This review appears GENUINE**\n\nIndicators: Balanced tone • Specific details • Natural language")
    else:
        st.warning("**❓ Mixed signals**\n\nThis review has both genuine and suspicious patterns.")
elif analyze_button and not review_input.strip():
    st.error("⚠️ Please enter a review first!")