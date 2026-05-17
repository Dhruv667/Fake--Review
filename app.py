import streamlit as st
import re

# Initialize session state for the text area
if "review_text" not in st.session_state:
    st.session_state.review_text = ""

def detect_fake_review(review_text):
    score = 0
    max_score = 0
    
    fake_indicators = {
        'extreme_positive': [
            'amazing', 'incredible', 'perfect', 'awesome', 'unbelievable', 'life-changing',
            'mind-blowing', 'spectacular', 'phenomenal', 'miraculous', 'exceptional',
            'extraordinary', 'sublime', 'outstanding', 'magnificent', 'brilliant',
            'excellent', 'wonderful', 'fantastic', 'terrific', 'superb', 'divine',
            'heavenly', 'incredible', 'marvelous', 'splendid', 'gorgeous', 'beautiful',
            'stunning', 'breathtaking', 'remarkable', 'impressive', 'astounding',
            'astonishing', 'shocking', 'stunning', 'dazzling', 'glorious', 'magnificent'
        ],
        'extreme_negative': [
            'worst', 'terrible', 'horrible', 'awful', 'disgusting', 'pathetic',
            'abysmal', 'atrocious', 'dreadful', 'appalling', 'vile', 'repulsive',
            'revolting', 'nauseating', 'sickening', 'heinous', 'deplorable', 'abominable'
        ],
        'urgency': [
            'must buy', 'everyone needs', 'everyone should', 'don\'t miss', 'grab now',
            'hurry', 'rush', 'limited time', 'act fast', 'buy now', 'order now',
            'get yours', 'quick buy', 'immediate', 'urgent', 'asap', 'right now',
            'don\'t wait', 'before it\'s gone', 'while supplies', 'can\'t miss'
        ],
        'generic_praise': [
            'best product', 'best ever', 'best purchase', 'changed my life', 'life altering',
            'game changer', 'game changing', 'ordered 10', 'ordered more', 'bought again',
            'buying again', 'recommend to all', 'tell everyone', 'friends want', 'family wants',
            'exceeded expectations', 'beyond expectations', 'better than expected', 'love it so much',
            'perfect fit', 'perfect size', 'perfect product', 'absolutely love', 'totally love',
            'completely satisfied', ' 100 percent satisfied', 'highly recommend', 'must recommend'
        ],
        'caps_heavy': [
            'AMAZING', 'INCREDIBLE', 'PERFECT', 'BEST', 'LOVE', 'EXCELLENT', 'AWESOME',
            'WOW', 'FANTASTIC', 'GREAT', 'WONDERFUL', 'HIGHLY RECOMMEND', 'BUY NOW'
        ],
        'repetition': [
            '!!!', '??', '...', 'perfect perfect', 'best best', 'amazing amazing',
            'love love', 'great great', 'awesome awesome', 'incredible incredible'
        ],
        'suspicious_patterns': [
            'accelerometer', 'gyroscope', 'magnetometer', 'proximity sensor', 'ambient light',
            'barometer', 'thermometer', 'humidity sensor', 'moisture sensor', 'pressure sensor',
            'purchased for', 'bought for review', 'got this for', 'received this to review',
            'first product', 'first time using', 'never used before', 'brand new user',
            'no downsides', 'no complaints', 'no issues', 'no problems', 'flawless',
            'can\'t find fault', 'nothing bad', 'nothing wrong', 'zero problems', 'zero issues'
        ]
    }
    
    genuine_indicators = [
        'but', 'however', 'although', 'though', 'downside', 'downside is', 'issue',
        'problem', 'problems', 'could be', 'could improve', 'better if', 'wish it had',
        'only complaint', 'complaint is', 'not perfect', 'not ideal', 'improvement',
        'improvements needed', 'needs improvement', 'somewhat', 'kind of', 'sort of',
        'decent', 'okay', 'alright', 'good enough', 'does the job', 'reliable',
        'works well', 'works as expected', 'satisfactory', 'satisfied', 'reasonably',
        'fairly', 'rather', 'pretty good', 'pretty decent', 'not bad', 'average',
        'mediocre', 'mixed', 'pros and cons', 'both good and bad', 'depends',
        'depending on', 'different for', 'might not', 'may not', 'for some',
        'for others', 'some people', 'battery lasted', 'weeks of', 'days of',
        'months of', 'hours of', 'after using', 'after a week', 'after a month',
        'quality is', 'build quality', 'construction', 'material', 'materials',
        'design', 'designed', 'specifically', 'particular', 'particular feature',
        'certain features', 'certain aspects', 'specific', 'details', 'mentioned',
        'noted', 'noticeable', 'noticed', 'observed', 'experience', 'experienced'
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
    
    has_measurements = bool(re.search(r'\d+\s*(days?|weeks?|months?|hours?|times?|years?|times|battery)', review_text))
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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        .main {
            background: transparent;
        }
        .stMetric {
            background-color: rgba(30, 41, 59, 0.8);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .result-card {
            padding: 25px;
            border-radius: 15px;
            margin: 15px 0;
            border-left: 5px solid;
        }
        .fake-card {
            background: rgba(239, 68, 68, 0.1);
            border-left-color: #ef4444;
        }
        .genuine-card {
            background: rgba(34, 197, 94, 0.1);
            border-left-color: #22c55e;
        }
        .uncertain-card {
            background: rgba(245, 158, 11, 0.1);
            border-left-color: #f59e0b;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div style='text-align: center; padding: 30px 0; margin-bottom: 30px;'>
        <h1 style='font-size: 3em; margin: 0; background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>
            🔍 Review Authenticity Checker
        </h1>
        <p style='font-size: 1.1em; color: #94a3b8; margin-top: 10px;'>
            Detect fake reviews with pattern analysis
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Input Section
col_input, col_button = st.columns([5, 1], gap="small")

with col_input:
    review_input = st.text_area(
        "Paste Review to Analyze",
        value=st.session_state.review_text,
        placeholder="Enter the review text here...",
        height=140,
        key="review_input",
        label_visibility="collapsed"
    )
    st.session_state.review_text = review_input

with col_button:
    st.write("")
    st.write("")
    st.write("")
    if st.button("🗑️ Clear", use_container_width=True, help="Clear the text area"):
        st.session_state.review_text = ""
        st.rerun()

st.divider()

# Analysis Section
if review_input and review_input.strip():
    prediction, confidence = detect_fake_review(review_input)
    
    # Main Result Display
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        if prediction == "GENUINE":
            st.markdown("""
                <div style='text-align: center; padding: 20px; background: rgba(34, 197, 94, 0.1); border-radius: 10px; border: 2px solid #22c55e;'>
                    <h2 style='color: #22c55e; margin: 0;'>✅ GENUINE</h2>
                </div>
            """, unsafe_allow_html=True)
        elif prediction == "FAKE":
            st.markdown("""
                <div style='text-align: center; padding: 20px; background: rgba(239, 68, 68, 0.1); border-radius: 10px; border: 2px solid #ef4444;'>
                    <h2 style='color: #ef4444; margin: 0;'>❌ FAKE</h2>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='text-align: center; padding: 20px; background: rgba(245, 158, 11, 0.1); border-radius: 10px; border: 2px solid #f59e0b;'>
                    <h2 style='color: #f59e0b; margin: 0;'>⚠️ UNCERTAIN</h2>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Confidence Score", f"{confidence:.1f}%", delta=None)
    
    with col3:
        authenticity = "High" if prediction == "GENUINE" else "Low"
        st.metric("Authenticity Level", authenticity, delta=None)
    
    # Detailed Analysis Section
    st.markdown("### 📊 Detailed Analysis")
    
    analysis_col1, analysis_col2 = st.columns(2, gap="medium")
    
    with analysis_col1:
        st.markdown("""
            <div style='background: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(148, 163, 184, 0.2);'>
                <h4 style='color: #60a5fa; margin-top: 0;'>📝 Text Characteristics</h4>
        """, unsafe_allow_html=True)
        
        caps_ratio = sum(1 for c in review_input if c.isupper()) / len(review_input) if len(review_input) > 0 else 0
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Capitalization", f"{caps_ratio*100:.1f}%", label_visibility="collapsed")
        with col_b:
            st.metric("Exclamation Marks", f"{review_input.count('!')}", label_visibility="collapsed")
        
        col_c, col_d = st.columns(2)
        with col_c:
            st.metric("Question Marks", f"{review_input.count('?')}", label_visibility="collapsed")
        with col_d:
            st.metric("Word Count", f"{len(review_input.split())}", label_visibility="collapsed")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with analysis_col2:
        st.markdown("""
            <div style='background: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 10px; border: 1px solid rgba(148, 163, 184, 0.2);'>
                <h4 style='color: #60a5fa; margin-top: 0;'>🔤 Language Patterns</h4>
        """, unsafe_allow_html=True)
        
        extreme_words = ['amazing', 'incredible', 'perfect', 'awesome', 'best', 'worst']
        extreme_count = sum(review_input.lower().count(w) for w in extreme_words)
        
        genuine_indicators = ['but', 'however', 'problem', 'issue', 'downside']
        genuine_count = sum(1 for ind in genuine_indicators if ind.lower() in review_input.lower())
        
        has_details = bool(re.search(r'\d+\s*(days?|weeks?|months?)', review_input))
        
        col_e, col_f = st.columns(2)
        with col_e:
            st.metric("Extreme Words", f"{extreme_count}", label_visibility="collapsed")
        with col_f:
            st.metric("Balanced Language", f"{genuine_count}", label_visibility="collapsed")
        
        col_g = st.columns(1)[0]
        with col_g:
            st.metric("Specific Details", "Yes" if has_details else "No", label_visibility="collapsed")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Final Verdict
    if prediction == "FAKE":
        st.markdown("""
            <div class='result-card fake-card'>
                <h3 style='color: #ef4444; margin-top: 0;'>⚠️ Likely Fake Review</h3>
                <p style='color: #cbd5e1; margin-bottom: 0;'>
                    <strong>Red Flags:</strong> Excessive capitalization • Extreme language • Generic phrases • Suspicious urgency
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif prediction == "GENUINE":
        st.markdown("""
            <div class='result-card genuine-card'>
                <h3 style='color: #22c55e; margin-top: 0;'>✅ Likely Genuine Review</h3>
                <p style='color: #cbd5e1; margin-bottom: 0;'>
                    <strong>Indicators:</strong> Balanced language • Specific details • Moderate tone • Natural expression
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='result-card uncertain-card'>
                <h3 style='color: #f59e0b; margin-top: 0;'>❓ Mixed Signals</h3>
                <p style='color: #cbd5e1; margin-bottom: 0;'>
                    This review contains both genuine and suspicious patterns. Manual review may be needed.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Check another review button
    if st.button("📝 Check Another Review", use_container_width=True):
        st.session_state.review_text = ""
        st.rerun()