import streamlit as st
import re

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

def detect_fake_review(review_text):
    text_lower = review_text.lower()
    
    # STRONG FAKE INDICATORS - Multiple matches needed for fake
    strong_fake = [
        'best product ever', 'changed my life', 'unbelievable', 'perfect product',
        'amazing beyond', 'everyone should buy', 'best ever made', 'never seen',
        'magical', 'flawless', 'ultimate product', 'extraordinary', 'unbeatable',
        'works 1000 times', 'five stars not enough', 'masterpiece', 'life changing',
        'absolutely flawless', 'completely outstanding', 'totally perfect', 'far beyond expectations'
    ]
    
    # MODERATE FAKE INDICATORS
    moderate_fake = [
        'amazing', 'incredible', 'perfect', 'awesome', 'spectacular', 'phenomenal',
        'outstanding', 'magnificent', 'brilliant', 'exceptional', 'extraordinary',
        'fantastic', 'wonderful', 'terrific', 'superb', 'divine', 'fabulous',
        'unmatched', 'supreme', 'world-class', 'revolutionary', 'innovative'
    ]
    
    # WEAK FAKE INDICATORS
    weak_fake = [
        'very good', 'excellent', 'great', 'love it', 'highly recommend',
        'best', 'wonderful', 'beautiful', 'stunning'
    ]
    
    # STRONG GENUINE INDICATORS
    strong_genuine = [
        'but', 'however', 'although', 'though', 'downside', 'issue', 'problem',
        'complaint', 'not perfect', 'wish it had', 'could improve', 'better if',
        'pros and cons', 'mixed', 'not ideal', 'needs improvement'
    ]
    
    # MODERATE GENUINE INDICATORS
    moderate_genuine = [
        'good', 'decent', 'okay', 'alright', 'satisfactory', 'reliable',
        'works well', 'fairly', 'pretty good', 'average', 'mediocre',
        'material', 'quality', 'design', 'build', 'packaging', 'delivery',
        'battery', 'performance', 'price', 'value', 'comfortable', 'easy to use'
    ]
    
    # WEAK GENUINE INDICATORS
    weak_genuine = [
        'and', 'the', 'with', 'for', 'after', 'weeks', 'days', 'daily',
        'using', 'use', 'works', 'installation', 'support', 'matched'
    ]
    
    # Count strong fake indicators
    strong_fake_count = 0
    for phrase in strong_fake:
        if phrase in text_lower:
            strong_fake_count += 1
    
    # Count moderate fake indicators
    moderate_fake_count = 0
    for word in moderate_fake:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            moderate_fake_count += 1
    
    # Count weak fake indicators
    weak_fake_count = 0
    for word in weak_fake:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            weak_fake_count += 1
    
    # Count strong genuine indicators
    strong_genuine_count = 0
    for phrase in strong_genuine:
        if phrase in text_lower:
            strong_genuine_count += 1
    
    # Count moderate genuine indicators
    moderate_genuine_count = 0
    for word in moderate_genuine:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            moderate_genuine_count += 1
    
    # Count weak genuine indicators
    weak_genuine_count = 0
    for word in weak_genuine:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            weak_genuine_count += 1
    
    # Calculate fake score
    fake_score = (strong_fake_count * 8) + (moderate_fake_count * 3) + (weak_fake_count * 0.5)
    
    # Calculate genuine score
    genuine_score = (strong_genuine_count * 8) + (moderate_genuine_count * 3) + (weak_genuine_count * 0.5)
    
    # Check capitalization
    caps_count = sum(1 for c in review_text if c.isupper())
    caps_ratio = caps_count / len(review_text) if len(review_text) > 0 else 0
    if caps_ratio > 0.35:
        fake_score += 8
    
    # Check exclamation marks
    exclaim_count = review_text.count('!')
    if exclaim_count > 5:
        fake_score += 8
    elif exclaim_count > 3:
        fake_score += 5
    
    # Check word count
    word_count = len(review_text.split())
    if word_count < 15:
        fake_score += 5
    elif word_count > 300:
        genuine_score += 3
    
    # Check for specific measurements/numbers
    has_measurements = bool(re.search(r'\d+\s*(days?|weeks?|months?|years?|hours?|%)', review_text))
    if has_measurements:
        genuine_score += 6
    
    # Calculate final confidence
    total = fake_score + genuine_score
    if total == 0:
        confidence = 50
        prediction = "UNCERTAIN"
    else:
        fake_percentage = (fake_score / total) * 100
        
        if fake_percentage > 70:
            prediction = "FAKE"
            confidence = fake_percentage
        elif fake_percentage < 30:
            prediction = "GENUINE"
            confidence = 100 - fake_percentage
        else:
            prediction = "UNCERTAIN"
            confidence = 50 + abs(fake_percentage - 50) / 2
    
    # Ensure confidence is between 15 and 90
    confidence = max(15, min(90, confidence))
    
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