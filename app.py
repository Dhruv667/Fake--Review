import streamlit as st
import re

def detect_fake_review(review_text):
    score = 0
    max_score = 0
    
    fake_indicators = {
        'extreme_positive': [
            'amazing', 'incredible', 'perfect', 'awesome', 'unbelievable', 'life-changing',
            'mind-blowing', 'spectacular', 'phenomenal', 'miraculous', 'exceptional',
            'extraordinary', 'sublime', 'outstanding', 'magnificent', 'brilliant',
            'excellent', 'wonderful', 'fantastic', 'terrific', 'superb', 'divine',
            'heavenly', 'marvelous', 'splendid', 'gorgeous', 'beautiful',
            'stunning', 'breathtaking', 'remarkable', 'impressive', 'astounding'
        ],
        'extreme_negative': [
            'worst', 'terrible', 'horrible', 'awful', 'disgusting', 'pathetic',
            'abysmal', 'atrocious', 'dreadful', 'appalling', 'vile', 'repulsive',
            'revolting', 'nauseating', 'sickening', 'heinous', 'deplorable'
        ],
        'urgency': [
            'must buy', 'everyone needs', 'don\'t miss', 'grab now',
            'hurry', 'rush', 'limited time', 'act fast', 'buy now', 'order now',
            'get yours', 'right now', 'don\'t wait', 'before it\'s gone'
        ],
        'generic_praise': [
            'best product', 'best ever', 'changed my life', 'game changer',
            'ordered more', 'buying again', 'exceeded expectations',
            'perfect fit', 'perfect product', 'highly recommend'
        ],
        'suspicious_patterns': [
            'no downsides', 'no complaints', 'no issues', 'flawless',
            'can\'t find fault', 'nothing bad', 'zero problems'
        ]
    }
    
    genuine_indicators = [
        'but', 'however', 'although', 'downside', 'issue',
        'problem', 'could improve', 'better if', 'wish it had',
        'not perfect', 'not ideal', 'somewhat', 'kind of',
        'decent', 'okay', 'alright', 'good enough',
        'works well', 'satisfied', 'reasonably', 'fairly'
    ]
    
    text_lower = review_text.lower()
    
    for category, words in fake_indicators.items():
        max_score += 25
        count = sum(text_lower.count(word) for word in words)
        if count > 5:
            score += 25
        elif count > 3:
            score += 20
        elif count > 1:
            score += 15
        elif count > 0:
            score += 10
    
    caps_count = sum(1 for c in review_text if c.isupper())
    caps_ratio = caps_count / len(review_text) if len(review_text) > 0 else 0
    max_score += 20
    if caps_ratio > 0.30:
        score += 20
    elif caps_ratio > 0.20:
        score += 15
    elif caps_ratio > 0.10:
        score += 8
    
    exclaim_count = review_text.count('!')
    max_score += 15
    if exclaim_count > 5:
        score += 15
    elif exclaim_count > 3:
        score += 12
    elif exclaim_count > 1:
        score += 8
    
    question_count = review_text.count('?')
    max_score += 10
    if question_count > 3:
        score += 10
    
    genuine_count = sum(1 for indicator in genuine_indicators if indicator.lower() in text_lower)
    max_score += 15
    if genuine_count > 4:
        score -= 15
    elif genuine_count > 2:
        score -= 10
    elif genuine_count > 0:
        score -= 5
    
    has_measurements = bool(re.search(r'\d+\s*(days?|weeks?|months?|hours?)', review_text))
    max_score += 10
    if has_measurements:
        score -= 10
    
    word_count = len(review_text.split())
    max_score += 5
    if word_count > 300:
        score -= 5
    elif word_count < 20:
        score += 5
    
    confidence = (score / max_score * 100) if max_score > 0 else 50
    confidence = max(0, min(100, confidence))
    
    if confidence > 65:
        prediction = "FAKE"
    elif confidence < 35:
        prediction = "GENUINE"
    else:
        prediction = "UNCERTAIN"
    
    return prediction, confidence

# Page configuration
st.set_page_config(
    page_title="Review Authenticity Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            max-width: 900px;
        }
        .header {
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            color: #3b82f6;
            margin: 0;
        }
        .header p {
            color: #94a3b8;
            font-size: 1em;
            margin: 10px 0 0 0;
        }
        .input-section {
            margin: 30px 0;
        }
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='header'>
        <h1>🔍 Review Authenticity Checker</h1>
        <p>Detect fake reviews with pattern analysis</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Input Section
st.markdown("### Enter Review Text")
review_input = st.text_area(
    "Review",
    placeholder="Paste the review here...",
    height=100,
    label_visibility="collapsed"
)

# Buttons
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    analyze_button = st.button("🔍 Analyze", use_container_width=True, key="analyze")

with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True, key="clear")

with col3:
    pass

# Handle Clear button
if clear_button:
    st.rerun()

st.divider()

# Analysis
if analyze_button and review_input.strip():
    prediction, confidence = detect_fake_review(review_input)
    
    # Result boxes
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
    
    st.divider()
    
    # Analysis Details
    st.markdown("### 📊 Analysis Details")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        caps_ratio = sum(1 for c in review_input if c.isupper()) / len(review_input) if len(review_input) > 0 else 0
        st.write(f"**Capitalization:** {caps_ratio*100:.1f}%")
        st.write(f"**Exclamation marks:** {review_input.count('!')}")
        st.write(f"**Question marks:** {review_input.count('?')}")
        st.write(f"**Word count:** {len(review_input.split())}")
    
    with col_right:
        extreme_words = ['amazing', 'incredible', 'perfect', 'awesome', 'best', 'worst']
        extreme_count = sum(review_input.lower().count(w) for w in extreme_words)
        st.write(f"**Extreme words:** {extreme_count}")
        
        genuine_words = ['but', 'however', 'problem', 'issue', 'downside']
        genuine_count = sum(1 for w in genuine_words if w in review_input.lower())
        st.write(f"**Balanced language:** {genuine_count}")
        
        has_details = bool(re.search(r'\d+\s*(days?|weeks?|months?)', review_input))
        st.write(f"**Specific details:** {'Yes' if has_details else 'No'}")
    
    st.divider()
    
    # Verdict
    if prediction == "FAKE":
        st.error("**🚨 This review appears FAKE**\n\nRed flags: Extreme language • Generic phrases • Unnatural patterns")
    elif prediction == "GENUINE":
        st.success("**✅ This review appears GENUINE**\n\nIndicators: Balanced tone • Specific details • Natural language")
    else:
        st.warning("**❓ Mixed signals**\n\nThis review has both genuine and suspicious patterns.")

elif analyze_button and not review_input.strip():
    st.error("⚠️ Please enter a review first!")