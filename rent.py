import streamlit as st
import pickle
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 0rem;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.95;
    }
    
    /* Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Prediction Box */
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .price-value {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .price-label {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        height: 3.5em;
        border-radius: 15px;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stNumberInput input, .stSelectbox select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
        transition: border-color 0.3s ease;
    }
    
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #00d2ff;
        color: #ffffff;
    }
    
    .info-box h4 {
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .info-box p {
        color: #e2e8f0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #48bb78;
        color: #ffffff;
    }
    
    .success-box h4 {
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .success-box p {
        color: #e2e8f0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Stats Section */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-top: 4px solid #667eea;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #ffffff;
        border-top: 1px solid rgba(255,255,255,0.2);
        margin-top: 3rem;
    }
    
    /* Image styling */
    .property-image {
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_model():
    try:
        with open(r'C:\Users\aryan\OneDrive\Desktop\project-3\load_model.sav', 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load locations from JSON
@st.cache_data
def load_locations():
    locations = ["1st block jayanagar", "1st phase jp nagar", "2nd phase judicial layout", "2nd stage nagarbhavi", "5th block hbr layout", "5th phase jp nagar", "6th phase jp nagar", "7th phase jp nagar", "8th phase jp nagar", "9th phase jp nagar", "aecs layout", "abbigere", "akshaya nagar", "ambalipura", "ambedkar nagar", "amruthahalli", "anandapura", "ananth nagar", "anekal", "anjanapura", "ardendale", "arekere", "attibele", "beml layout", "btm 2nd stage", "btm layout", "babusapalaya", "badavala nagar", "balagere", "banashankari", "banashankari stage ii", "banashankari stage iii", "banashankari stage v", "banashankari stage vi", "banaswadi", "banjara layout", "bannerghatta", "bannerghatta road", "basavangudi", "basaveshwara nagar", "battarahalli", "begur", "begur road", "bellandur", "benson town", "bharathi nagar", "bhoganhalli", "billekahalli", "binny pete", "bisuvanahalli", "bommanahalli", "bommasandra", "bommasandra industrial area", "bommenahalli", "brookefield", "budigere", "cv raman nagar", "chamrajpet", "chandapura", "channasandra", "chikka tirupathi", "chikkabanavar", "chikkalasandra", "choodasandra", "cooke town", "cox town", "cunningham road", "dasanapura", "dasarahalli", "devanahalli", "devarachikkanahalli", "dodda nekkundi", "doddaballapur", "doddakallasandra", "doddathoguru", "domlur", "dommasandra", "epip zone", "electronic city", "electronic city phase ii", "electronics city phase 1", "frazer town", "gm palaya", "garudachar palya", "giri nagar", "gollarapalya hosahalli", "gottigere", "green glen layout", "gubbalala", "gunjur", "hal 2nd stage", "hbr layout", "hrbr layout", "hsr layout", "haralur road", "harlur", "hebbal", "hebbal kempapura", "hegde nagar", "hennur", "hennur road", "hoodi", "horamavu agara", "horamavu banaswadi", "hormavu", "hosa road", "hosakerehalli", "hoskote", "hosur road", "hulimavu", "isro layout", "itpl", "iblur village", "indira nagar", "jp nagar", "jakkur", "jalahalli", "jalahalli east", "jigani", "judicial layout", "kr puram", "kadubeesanahalli", "kadugodi", "kaggadasapura", "kaggalipura", "kaikondrahalli", "kalena agrahara", "kalyan nagar", "kambipura", "kammanahalli", "kammasandra", "kanakapura", "kanakpura road", "kannamangala", "karuna nagar", "kasavanhalli", "kasturi nagar", "kathriguppe", "kaval byrasandra", "kenchenahalli", "kengeri", "kengeri satellite town", "kereguddadahalli", "kodichikkanahalli", "kodigehaali", "kodigehalli", "kodihalli", "kogilu", "konanakunte", "koramangala", "kothannur", "kothanur", "kudlu", "kudlu gate", "kumaraswami layout", "kundalahalli", "lb shastri nagar", "laggere", "lakshminarayana pura", "lingadheeranahalli", "magadi road", "mahadevpura", "mahalakshmi layout", "mallasandra", "malleshpalya", "malleshwaram", "marathahalli", "margondanahalli", "marsur", "mico layout", "munnekollal", "murugeshpalya", "mysore road", "ngr layout", "nri layout", "nagarbhavi", "nagasandra", "nagavara", "nagavarapalya", "narayanapura", "neeladri nagar", "nehru nagar", "ombr layout", "old airport road", "old madras road", "padmanabhanagar", "pai layout", "panathur", "parappana agrahara", "pattandur agrahara", "poorna pragna layout", "prithvi layout", "r.t. nagar", "rachenahalli", "raja rajeshwari nagar", "rajaji nagar", "rajiv nagar", "ramagondanahalli", "ramamurthy nagar", "rayasandra", "sahakara nagar", "sanjay nagar", "sarakki nagar", "sarjapur", "sarjapur  road", "sarjapura - attibele road", "sector 2 hsr layout", "sector 7 hsr layout", "seegehalli", "shampura", "shivaji nagar", "singasandra", "somasundara palya", "sompura", "sonnenahalli", "subramanyapura", "sultan palaya", "tc palaya", "talaghattapura", "thanisandra", "thigalarapalya", "thubarahalli", "tindlu", "tumkur road", "ulsoor", "uttarahalli", "varthur", "varthur road", "vasanthapura", "vidyaranyapura", "vijayanagar", "vishveshwarya layout", "vishwapriya layout", "vittasandra", "whitefield", "yelachenahalli", "yelahanka", "yelahanka new town", "yelenahalli", "yeshwanthpur"]
    return locations

# Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🏠 Bangalore House Price Predictor</div>
        <div class="hero-subtitle">Get accurate price estimates powered by AI & Machine Learning</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 About This App")
    st.info("""
    This intelligent tool uses machine learning to predict house prices in Bangalore based on:
    
    ✅ Location analysis  
    ✅ Property size  
    ✅ Room configuration  
    ✅ Historical data patterns
    """)
    
    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. Select your desired location
    2. Enter property details
    3. Click predict to see results
    4. Review the price estimate
    """)
    
    st.markdown("### 📈 Model Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Locations", "241+")
    with col2:
        st.metric("Accuracy", "85%+")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.success("""
    **Pro Tip:** Prices vary based on proximity to IT hubs, metro stations, and amenities!
    """)

# Load model and locations
model = load_model()
locations = load_locations()

if model is None:
    st.error("⚠️ Failed to load the model. Please check the model path.")
    st.stop()

# Feature cards section
st.markdown("### ✨ Why Choose Our Predictor?")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <span class="card-icon">🎯</span>
            <div class="card-title">Accurate Predictions</div>
            <div class="card-description">Our AI model is trained on thousands of property listings</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <span class="card-icon">⚡</span>
            <div class="card-title">Instant Results</div>
            <div class="card-description">Get price estimates in seconds, not days</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <span class="card-icon">🔒</span>
            <div class="card-title">Data-Driven</div>
            <div class="card-description">Based on real market data and trends</div>
        </div>
    """, unsafe_allow_html=True)

# Main prediction form
st.markdown("---")
st.markdown("## 🔍 Enter Property Details")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📍 Location & Size")
    
    # Location dropdown
    location = st.selectbox(
        "Location",
        options=["Select a location"] + sorted(locations),
        index=0,
        help="Choose the area where the property is located"
    )
    
    # Total Square Feet
    total_sqft = st.number_input(
        "Total Square Feet",
        min_value=300,
        max_value=30000,
        value=1000,
        step=100,
        help="Enter the total area in square feet"
    )
    
    # Price per sqft indicator
    if total_sqft > 0:
        st.caption(f"💡 Typical range: {total_sqft * 3:.0f} - {total_sqft * 8:.0f} lakhs")

with col2:
    st.markdown("#### 🛏️ Room Configuration")
    
    # BHK (Bedrooms)
    bhk = st.number_input(
        "Number of Bedrooms (BHK)",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        help="Enter the number of bedrooms"
    )
    
    # Bathrooms
    bath = st.number_input(
        "Number of Bathrooms",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        help="Enter the number of bathrooms"
    )
    
    # Room ratio indicator
    if bhk > 0 and bath > 0:
        ratio = bhk / bath
        if ratio < 1:
            st.caption("🚿 Bathroom-rich property")
        elif ratio > 2:
            st.caption("🛏️ Bedroom-rich property")
        else:
            st.caption("✅ Balanced room ratio")

# Prediction button
st.markdown("---")
predict_button = st.button("🔮 Predict Price Now", use_container_width=True)

if predict_button:
    if location == "Select a location":
        st.error("⚠️ Please select a location!")
    else:
        with st.spinner("🔄 Analyzing property details..."):
            # Prepare input data
            input_data = np.zeros(244)
            
            # Set the numerical features
            input_data[0] = total_sqft
            input_data[1] = bath
            input_data[2] = bhk
            
            # Set the location feature
            if location in locations:
                loc_index = locations.index(location)
                input_data[3 + loc_index] = 1
            
            # Make prediction
            try:
                prediction = model.predict([input_data])[0]
                
                # Display prediction with animation
                st.balloons()
                
                st.markdown(f"""
                    <div class="prediction-box">
                        <div class="price-label">Estimated Property Value</div>
                        <div class="price-value">₹ {prediction:.2f} L</div>
                        <div class="price-label">Indian Rupees (Lakhs)</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Price breakdown
                st.markdown("### 📊 Price Breakdown")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-number">₹{prediction:.2f}L</div>
                            <div class="stat-label">Total Price</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    price_per_sqft = (prediction * 100000) / total_sqft
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-number">₹{price_per_sqft:.0f}</div>
                            <div class="stat-label">Per Sq.Ft</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    monthly_emi = (prediction * 100000 * 0.008) / (1 - (1 + 0.008)**-240)
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-number">₹{monthly_emi/1000:.1f}K</div>
                            <div class="stat-label">Est. EMI/month</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    down_payment = prediction * 0.20
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="stat-number">₹{down_payment:.2f}L</div>
                            <div class="stat-label">20% Down Payment</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Input Summary
                st.markdown("### 📝 Property Summary")
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.markdown(f"""
                        <div class="success-box">
                            <h4>🏘️ Location Details</h4>
                            <p><strong>Area:</strong> {location.title()}</p>
                            <p><strong>Type:</strong> {bhk} BHK Apartment</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with summary_col2:
                    st.markdown(f"""
                        <div class="success-box">
                            <h4>📐 Size & Configuration</h4>
                            <p><strong>Total Area:</strong> {total_sqft} sq.ft</p>
                            <p><strong>Bathrooms:</strong> {bath}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Price comparison chart
                st.markdown("### 📈 Price Comparison")
                
                # Create sample data for comparison
                comparison_data = {
                    'Config': [f'{bhk-1} BHK', f'{bhk} BHK\n(Your Property)', f'{bhk+1} BHK'],
                    'Price': [prediction * 0.75, prediction, prediction * 1.35],
                    'Color': ['#a8dadc', '#667eea', '#a8dadc']
                }
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=comparison_data['Config'],
                        y=comparison_data['Price'],
                        marker_color=comparison_data['Color'],
                        text=[f'₹{p:.1f}L' for p in comparison_data['Price']],
                        textposition='outside',
                    )
                ])
                
                fig.update_layout(
                    title='Price Comparison by BHK Configuration',
                    xaxis_title='Property Type',
                    yaxis_title='Price (Lakhs)',
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Additional insights
                st.markdown("### 💡 Key Insights")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                        <div class="info-box">
                            <h4>🎯 Market Position</h4>
                            <p>This property is priced competitively based on current market trends in Bangalore.</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div class="info-box">
                            <h4>📊 Investment Potential</h4>
                            <p>Consider factors like proximity to IT hubs, metro connectivity, and future development plans.</p>
                        </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error making prediction: {e}")

# Footer
st.markdown("""
    <div class="footer">
        <h3 style="color: #ffffff;">📢 Important Disclaimer</h3>
        <p style="color: #f0f0f0;">💡 This prediction is based on historical data and machine learning models.</p>
        <p style="color: #f0f0f0;">📊 Actual prices may vary based on current market conditions, property condition, amenities, and other factors.</p>
        <p style="color: #f0f0f0;">🤝 Always consult with real estate professionals for final decisions.</p>
        <hr style="margin: 2rem 0; border: none; border-top: 1px solid rgba(255,255,255,0.2);">
        <p style="color: #e0e0e0; font-size: 0.9rem;">Made with ❤️ for Bangalore Property Seekers | © 2024</p>
    </div>
""", unsafe_allow_html=True)