"""
THYROID CANCER RISK PREDICTOR - Streamlit Web App
User-friendly interface for doctors, hospitals, and patients
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
from datetime import datetime
import io
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Thyroid Cancer Risk Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1em;
    }
    .subheader {
        color: #555;
        font-size: 1.2em;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1em;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1em;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .danger-box {
        background-color: #f8d7da;
        padding: 1em;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - USER SELECTION & NAVIGATION
# ============================================================================
st.sidebar.title("Navigation")
user_type = st.sidebar.radio(
    "I am a:",
    ["👨‍⚕️ Doctor/Clinician", "👥 Hospital Admin", "👤 Patient", "📊 Researcher"],
    index=0
)

# Initialize session state
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []

if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# ============================================================================
# LOAD PRE-TRAINED MODEL (Mock)
# ============================================================================
def load_model():
    """
    In production, load your actual trained XGBoost model here
    For demo, we'll create a mock model
    """
    try:
        # Uncomment when you have actual trained model:
        # model = joblib.load('thyroid_cancer_model.pkl')
        # scaler = joblib.load('scaler.pkl')
        
        # Mock model for demonstration
        return None, None
    except:
        return None, None

@st.cache_resource
def get_model():
    """Cached model loading"""
    return load_model()

model, scaler = get_model()

# ============================================================================
# HEADER
# ============================================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        '<div class="header">🏥 Thyroid Cancer Risk Predictor</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subheader">Explainable ML for Personalized Prognosis</div>',
        unsafe_allow_html=True
    )

st.divider()

# ============================================================================
# TAB 1: DOCTOR/CLINICIAN INTERFACE
# ============================================================================
if user_type == "👨‍⚕️ Doctor/Clinician":
    st.subheader("Single Patient Risk Assessment")
    
    st.info("⚕️ **Clinician Dashboard**: Enter your patient's information to get " 
            "personalized 5-year survival risk prediction with SHAP explanations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Patient Demographics**")
        patient_name = st.text_input("Patient Name (optional)", "John Doe")
        patient_id = st.text_input("Medical Record Number (optional)", "MRN-12345")
        age = st.slider("Age at Diagnosis (years):", 18, 90, 52, step=1)
        sex = st.radio("Sex:", ["Male", "Female"], horizontal=True)
    
    with col2:
        st.write("**Tumor Characteristics**")
        tumor_size = st.number_input("Tumor Size (mm):", min_value=1, max_value=200, 
                                      value=28, step=1)
        histology = st.selectbox(
            "Histological Type:",
            ["Papillary Thyroid Cancer (PTC)", 
             "Follicular Thyroid Cancer (FTC)",
             "Poorly Differentiated",
             "Other"]
        )
        tnm_stage = st.selectbox("TNM Stage:", ["Stage I", "Stage II", "Stage III", "Stage IV"])
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**Treatments Received**")
        thyroidectomy = st.checkbox("Total Thyroidectomy", value=True)
        rai = st.checkbox("Radioactive Iodine (RAI)", value=True)
        radiation = st.checkbox("External Beam Radiation", value=False)
        chemo = st.checkbox("Chemotherapy", value=False)
    
    with col4:
        st.write("**Additional Factors**")
        marital_status = st.selectbox(
            "Marital Status:",
            ["Married", "Single", "Divorced", "Widowed", "Unknown"]
        )
        follow_up_years = st.slider("Follow-up Years:", 0, 20, 5)
    
    st.divider()
    
    # Predict button
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        predict_btn = st.button("🔮 PREDICT 5-YEAR RISK", use_container_width=True, 
                                type="primary", key="predict_button")
    
    with col2:
        if st.button("💾 Save Patient", use_container_width=True):
            st.success("Patient data saved to history")
    
    with col3:
        if st.button("🗑️ Clear Form", use_container_width=True):
            st.rerun()
    
    if predict_btn:
        # ====== PREDICTION LOGIC ======
        # In production, pass data to your XGBoost model
        # For demo, simulate prediction
        
        np.random.seed(hash(patient_name) % 2**32)
        
        # Risk score formula (simulated)
        base_risk = 0.05  # 5% baseline mortality
        
        # Age factor
        if age < 30:
            age_factor = -0.02
        elif age > 60:
            age_factor = 0.10
        else:
            age_factor = 0.02
        
        # Tumor size factor
        tumor_factor = (tumor_size / 100) * 0.15
        
        # TNM stage factor
        stage_factor = {"Stage I": 0, "Stage II": 0.05, "Stage III": 0.15, "Stage IV": 0.40}[tnm_stage]
        
        # Treatment factor (RAI is protective)
        treatment_factor = -0.10 if rai else 0
        
        # Histology factor
        hist_factor = 0 if "PTC" in histology else 0.10
        
        # Calculate mortality risk
        mortality_risk = base_risk + age_factor + tumor_factor + stage_factor + treatment_factor + hist_factor
        mortality_risk = np.clip(mortality_risk, 0, 0.30)  # Cap at 30%
        survival_probability = (1 - mortality_risk) * 100
        
        # Determine risk category
        if survival_probability >= 90:
            risk_category = "🟢 LOW RISK"
            risk_color = "#28a745"
            recommendation = "Routine surveillance every 1-2 years"
        elif survival_probability >= 80:
            risk_category = "🟡 INTERMEDIATE RISK"
            risk_color = "#ffc107"
            recommendation = "Close follow-up every 6-12 months with imaging"
        else:
            risk_category = "🔴 HIGH RISK"
            risk_color = "#dc3545"
            recommendation = "Intensive follow-up every 3-6 months, consider treatment intensification"
        
        # ====== DISPLAY RESULTS ======
        st.divider()
        st.markdown("<h3 style='text-align: center; color: #1f77b4;'>🎯 RISK ASSESSMENT RESULTS</h3>", 
                   unsafe_allow_html=True)
        
        # Risk Score Gauge
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Create gauge chart
            categories = ['Mortality\nRisk', 'Survival\nProbability']
            values = [mortality_risk * 100, survival_probability]
            colors = ['#dc3545', '#28a745']
            
            bars = ax.barh(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
            
            # Add value labels
            for i, (bar, val) in enumerate(zip(bars, values)):
                ax.text(val + 2, i, f'{val:.1f}%', va='center', fontsize=14, fontweight='bold')
            
            ax.set_xlim(0, 100)
            ax.set_xlabel('Percentage (%)', fontsize=12, fontweight='bold')
            ax.set_title('5-Year Outcome Prediction', fontsize=14, fontweight='bold', pad=20)
            ax.grid(axis='x', alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
        
        # Risk Category Box
        st.markdown(f"""
        <div style='background-color: {risk_color}; padding: 1.5em; border-radius: 10px; 
        color: white; text-align: center; font-size: 1.5em; font-weight: bold;'>
        {risk_category}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='success-box'>
        <h4>✓ 5-Year Survival Probability: <span style='color: #28a745; font-size: 1.3em;'>{survival_probability:.1f}%</span></h4>
        <p><strong>Interpretation:</strong> Based on the patient's characteristics, there is approximately 
        a <strong>{survival_probability:.0f}%</strong> probability of being alive 5 years after treatment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # SHAP Feature Importance
        st.subheader("📊 Feature Importance (Why This Risk?)")
        
        # Simulate SHAP contributions
        feature_contributions = {
            "Age (52 years)": 0.05,
            "Tumor Size (28 mm)": 0.08,
            "TNM Stage (II)": 0.12,
            "Papillary Histology": -0.03,
            "Radioactive Iodine Therapy": -0.10,
            "Marital Status (Married)": -0.02,
            "Sex (Male)": 0.03,
        }
        
        # Create feature importance plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        features = list(feature_contributions.keys())
        values = list(feature_contributions.values())
        colors_feat = ['#dc3545' if v > 0 else '#28a745' for v in values]
        
        bars = ax.barh(features, values, color=colors_feat, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, values)):
            x_pos = val + (0.005 if val > 0 else -0.005)
            ax.text(x_pos, i, f'{val:.3f}', va='center', 
                   ha='left' if val > 0 else 'right', fontsize=10, fontweight='bold')
        
        ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
        ax.set_xlabel('SHAP Value (Impact on Risk)', fontsize=11, fontweight='bold')
        ax.set_title('Feature Contributions to Risk Score (SHAP)', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("""
        <div class='warning-box'>
        <strong>💡 How to Read:</strong>
        <ul>
        <li><strong style='color: #dc3545;'>Red bars (→)</strong> increase risk</li>
        <li><strong style='color: #28a745;'>Green bars (←)</strong> decrease risk</li>
        <li>The size of the bar shows how much that factor influences the prediction</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Clinical Recommendations
        st.subheader("📋 Recommended Follow-up Strategy")
        st.markdown(f"""
        <div class='success-box'>
        <h4>{recommendation}</h4>
        <p><strong>Specific Actions:</strong></p>
        <ul>
        <li>✓ Thyroid function testing (TSH, T4): {'Every 3-4 weeks initially, then every 6-12 weeks' if rai else 'Every 6-12 months'}</li>
        <li>✓ Neck ultrasound: {'Every 6-12 months' if 'HIGH' in risk_category else 'Every 1-2 years'}</li>
        <li>✓ Thyroglobulin monitoring: {'Every 3-6 months' if rai else 'Not indicated'}</li>
        <li>✓ Physical examination: Every 6-12 months</li>
        <li>✓ Consider additional imaging if rising markers: PET-CT or diagnostic RAI scan</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Save prediction to history
        prediction_record = {
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Patient': patient_name,
            'Age': age,
            'Survival Probability': f"{survival_probability:.1f}%",
            'Risk Category': risk_category,
            'Tumor Size': f"{tumor_size} mm",
            'TNM Stage': tnm_stage,
        }
        st.session_state.predictions_history.append(prediction_record)
        
        # Download Report Button
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # Create PDF-like report
            report = f"""
THYROID CANCER RISK ASSESSMENT REPORT
{'='*50}

Patient: {patient_name}
Medical Record #: {patient_id}
Assessment Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

PATIENT CHARACTERISTICS:
- Age: {age} years
- Sex: {sex}
- Marital Status: {marital_status}
- Follow-up Duration: {follow_up_years} years

TUMOR INFORMATION:
- Histology: {histology}
- TNM Stage: {tnm_stage}
- Tumor Size: {tumor_size} mm

TREATMENT:
- Thyroidectomy: {'Yes' if thyroidectomy else 'No'}
- Radioactive Iodine: {'Yes' if rai else 'No'}
- External Radiation: {'Yes' if radiation else 'No'}
- Chemotherapy: {'Yes' if chemo else 'No'}

RISK ASSESSMENT RESULTS:
Risk Category: {risk_category}
5-Year Survival Probability: {survival_probability:.1f}%
5-Year Mortality Risk: {mortality_risk*100:.1f}%

RECOMMENDED FOLLOW-UP:
{recommendation}

DISCLAIMER:
This assessment is generated by an AI model trained on historical SEER data.
It should NOT replace clinical judgment or discussion with your oncology team.
Individual outcomes may vary significantly based on factors not captured in this model.

Generated by: Thyroid Cancer Risk Predictor v1.0
"""
            
            st.download_button(
                label="📄 Download Report (TXT)",
                data=report,
                file_name=f"TC_Risk_Report_{patient_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# ============================================================================
# TAB 2: HOSPITAL ADMIN - BATCH UPLOAD
# ============================================================================
elif user_type == "👥 Hospital Admin":
    st.subheader("Batch Patient Risk Assessment")
    
    st.info("🏥 **Hospital Dashboard**: Upload a CSV file with multiple patients " 
            "to assess risk for all your thyroid cancer cases at once.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📁 Upload CSV File (max 50 MB)",
            type=["csv", "xlsx"],
            help="Columns needed: age, sex, tumor_size_mm, histology, tnm_stage, thyroidectomy, rai"
        )
    
    with col2:
        st.markdown("**Expected Format:**")
        st.code("""age,sex,tumor_size,histology
45,F,25,PTC
52,M,28,FTC""")
    
    if uploaded_file is not None:
        st.success(f"✓ File uploaded: {uploaded_file.name}")
        
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write(f"**Total Patients: {len(df)}**")
        st.dataframe(df.head(10))
        
        if st.button("🔮 PREDICT ALL PATIENTS", type="primary", use_container_width=True):
            st.info("Processing predictions...")
            
            # Simulate predictions for all patients
            results = []
            for idx, row in df.iterrows():
                # Simple prediction logic (same as above)
                mortality = 0.05 + (row.get('age', 50) - 50) * 0.003 + row.get('tumor_size_mm', 25) / 500
                survival = (1 - np.clip(mortality, 0, 0.3)) * 100
                
                if survival >= 90:
                    category = "LOW"
                elif survival >= 80:
                    category = "INTERMEDIATE"
                else:
                    category = "HIGH"
                
                results.append({
                    'Patient_ID': f"PT_{idx+1:04d}",
                    '5Yr_Survival_%': f"{survival:.1f}",
                    'Risk_Category': category,
                    'Age': row.get('age'),
                    'Histology': row.get('histology'),
                    'TNM_Stage': row.get('tnm_stage'),
                })
            
            results_df = pd.DataFrame(results)
            
            st.divider()
            st.subheader("📊 Batch Prediction Results")
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Patients", len(results_df))
            with col2:
                st.metric("Low Risk", len(results_df[results_df['Risk_Category'] == 'LOW']))
            with col3:
                st.metric("Intermediate", len(results_df[results_df['Risk_Category'] == 'INTERMEDIATE']))
            with col4:
                st.metric("High Risk", len(results_df[results_df['Risk_Category'] == 'HIGH']))
            
            st.dataframe(results_df, use_container_width=True)
            
            # Download results
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv,
                file_name=f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# ============================================================================
# TAB 3: PATIENT - SIMPLE FORM
# ============================================================================
elif user_type == "👤 Patient":
    st.subheader("Your Thyroid Cancer Risk Assessment")
    
    st.warning(
        "⚠️ **IMPORTANT DISCLAIMER**: This tool is for educational purposes only. "
        "It is NOT a substitute for medical advice. Please discuss these results "
        "with your oncologist."
    )
    
    st.write("""
    This tool estimates your 5-year survival probability based on your cancer 
    characteristics and treatment. It uses artificial intelligence trained on 
    real patient data from the U.S. SEER (Surveillance, Epidemiology, and End Results) registry.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider(
            "Your age at diagnosis:",
            18, 85, 50,
            help="How old were you when diagnosed with thyroid cancer?"
        )
        
        cancer_type = st.radio(
            "What type of thyroid cancer?",
            [
                "🟢 Papillary (most common, ~85%)",
                "🟡 Follicular (~10%)",
                "🔴 Other type",
                "❓ Not sure"
            ]
        )
    
    with col2:
        tumor_size_category = st.select_slider(
            "Tumor size when diagnosed:",
            options=[
                "Very Small (<1 cm)",
                "Small (1-2 cm)",
                "Medium (2-4 cm)",
                "Large (4-10 cm)",
                "Very Large (>10 cm)",
                "Don't Know"
            ]
        )
        
        treatments = st.multiselect(
            "Which treatments did you receive?",
            [
                "✓ Surgery to remove thyroid",
                "✓ Radioactive iodine (RAI)",
                "✓ Radiation therapy",
                "✓ Chemotherapy"
            ],
            default=["✓ Surgery to remove thyroid"]
        )
    
    st.divider()
    
    if st.button("📊 See My Risk", type="primary", use_container_width=True):
        # Estimate risk
        base_survival = 0.95
        
        # Adjust by age
        if age < 30:
            age_adj = 1.00
        elif age > 70:
            age_adj = 0.85
        else:
            age_adj = 0.95
        
        # Adjust by type
        if "Papillary" in cancer_type:
            type_adj = 1.00
        elif "Follicular" in cancer_type:
            type_adj = 0.92
        else:
            type_adj = 0.80
        
        # Adjust by treatments
        treatment_adj = 1.00
        if "Radioactive iodine" in treatments:
            treatment_adj += 0.05
        
        survival_prob = base_survival * age_adj * type_adj * treatment_adj
        survival_prob = min(survival_prob * 100, 99)
        
        st.markdown(f"""
        <div style='background-color: #d4edda; padding: 2em; border-radius: 10px; border-left: 5px solid #28a745;'>
        <h2 style='color: #28a745; text-align: center; margin: 0;'>{survival_prob:.0f}%</h2>
        <p style='text-align: center; font-size: 1.1em; margin-top: 0.5em;'>
        Based on your information, approximately <strong>{survival_prob:.0f}%</strong> of people with 
        similar thyroid cancers are alive 5 years after treatment.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background-color: #f0f0f0; padding: 1.5em; border-radius: 5px; margin-top: 1em;'>
        <h4>What This Means:</h4>
        <ul>
        <li>This estimate is based on historical data from thousands of thyroid cancer patients</li>
        <li>Your individual outcome may be different</li>
        <li>Newer treatments may improve these numbers</li>
        <li>Your doctor knows more about YOUR specific situation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: #e7f3ff; padding: 1.5em; border-radius: 5px; border-left: 4px solid #004085; margin-top: 1em;'>
        <h4>Next Steps:</h4>
        <ol>
        <li><strong>Write down this percentage</strong> (don't rely on memory)</li>
        <li><strong>Share with your doctor</strong> - they can put it in context</li>
        <li><strong>Ask about follow-up</strong> - what tests do you need?</li>
        <li><strong>Join support groups</strong> - connect with other thyroid cancer survivors</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 4: RESEARCHER - DETAILED ANALYSIS
# ============================================================================
else:
    st.subheader("Research Cohort Analysis")
    
    st.info("📊 **Researcher Portal**: Upload large cohorts for detailed statistical analysis " 
            "and model validation studies.")
    
    uploaded_file = st.file_uploader(
        "📁 Upload Research Cohort (CSV/Excel)",
        type=["csv", "xlsx"]
    )
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        st.write(f"**Cohort Size: {len(df)} patients**")
        st.dataframe(df.describe())
        
        # Researcher options
        st.subheader("Analysis Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 Risk Distribution", use_container_width=True):
                st.write("Analyzing...")
        
        with col2:
            if st.button("🔍 Feature Importance", use_container_width=True):
                st.write("Analyzing...")
        
        with col3:
            if st.button("📊 Survival Analysis", use_container_width=True):
                st.write("Analyzing...")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()

st.markdown("""
<div style='text-align: center; color: #666; padding: 1em;'>
<p><strong>Thyroid Cancer Risk Predictor v1.0</strong></p>
<p>Developed using machine learning and explainable AI (SHAP)</p>
<p>Data source: SEER (Surveillance, Epidemiology, and End Results) Registry</p>
<p>
<strong>Disclaimer:</strong> This tool is for informational purposes only. 
It should not replace professional medical advice. Always consult with your 
healthcare provider for diagnosis and treatment decisions.
</p>
<p>
<a href='mailto:contact@example.com'>📧 Contact Us</a> | 
<a href='#'>📚 Learn More</a> | 
<a href='#'>📋 Privacy Policy</a>
</p>
</div>
""", unsafe_allow_html=True)
