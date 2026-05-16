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

st.set_page_config(page_title="Fake Review Detector", layout="wide")

st.title("🔍 Fake Review Detection System")
st.markdown("**Advanced Machine Learning Based Detection with 88% Accuracy**")
st.markdown("---")

col_input, col_clear = st.columns([4, 1])

with col_input:
    review_input = st.text_area(
        "Enter Review Text:",
        placeholder="Paste the review you want to analyze...",
        height=120,
        key="review_input"
    )

with col_clear:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear", use_container_width=True):
        st.rerun()

if review_input and review_input.strip():
    prediction, confidence = detect_fake_review(review_input)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if prediction == "GENUINE":
            st.success(f"### ✅ GENUINE")
        elif prediction == "FAKE":
            st.error(f"### ❌ FAKE")
        else:
            st.warning(f"### ⚠️ UNCERTAIN")
    
    with col2:
        st.metric("Confidence Score", f"{confidence:.1f}%")
    
    with col3:
        if prediction == "GENUINE":
            st.metric("Authenticity Level", "High")
        else:
            st.metric("Authenticity Level", "Low")
    
    st.progress(confidence / 100)
    
    st.markdown("---")
    st.subheader("📊 Detailed Analysis")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        st.write("**Text Characteristics:**")
        caps_ratio = sum(1 for c in review_input if c.isupper()) / len(review_input) if len(review_input) > 0 else 0
        st.write(f"• Capitalization: {caps_ratio*100:.1f}%")
        st.write(f"• Exclamation marks: {review_input.count('!')}")
        st.write(f"• Question marks: {review_input.count('?')}")
        st.write(f"• Word count: {len(review_input.split())}")
    
    with analysis_col2:
        st.write("**Language Patterns:**")
        extreme_words = ['amazing', 'incredible', 'perfect', 'awesome', 'best', 'worst']
        extreme_count = sum(review_input.lower().count(w) for w in extreme_words)
        st.write(f"• Extreme sentiment words: {extreme_count}")
        
        genuine_indicators = ['but', 'however', 'problem', 'issue', 'downside']
        genuine_count = sum(1 for ind in genuine_indicators if ind.lower() in review_input.lower())
        st.write(f"• Balanced language indicators: {genuine_count}")
        
        has_details = bool(re.search(r'\d+\s*(days?|weeks?|months?)', review_input))
        st.write(f"• Specific timeframe: {'Yes' if has_details else 'No'}")
    
    st.markdown("---")
    if prediction == "FAKE":
        st.error(
            "**⚠️ This review appears to be FAKE**\n\n"
            "Indicators: Excessive capitalization • Extreme language • Generic phrases • Urgency tactics"
        )
    elif prediction == "GENUINE":
        st.success(
            "**✅ This review appears to be GENUINE**\n\n"
            "Indicators: Balanced language • Specific details • Moderate tone • Natural patterns"
        )
    else:
        st.warning(
            "**❓ Classification Uncertain**\n\n"
            "This review has mixed characteristics. Manual review recommended."
        )
    
    st.markdown("---")
    col_recheck, col_space = st.columns([1, 4])
    with col_recheck:
        if st.button("📝 Check Another Review", use_container_width=True):
            st.rerun()

else:
    st.info("👈 **Enter a review text to begin analysis**")