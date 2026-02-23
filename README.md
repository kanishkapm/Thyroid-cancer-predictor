# hyroid Cancer Risk Predictor

A user-friendly Streamlit web application for predicting 5-year survival risk in thyroid cancer patients using explainable AI (SHAP) and machine learning. Designed for doctors, hospital administrators, patients, and researchers.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

### For Clinicians/Doctors
- **Single Patient Assessment**: Enter patient demographics, tumor characteristics, and treatment history
- **Risk Prediction**: Get personalized 5-year survival probability with risk categorization (Low/Intermediate/High)
- **Explainable AI**: SHAP feature importance plots showing why the model made certain predictions
- **Clinical Recommendations**: Evidence-based follow-up strategies based on risk level
- **Report Generation**: Download detailed patient reports in TXT format

### For Hospital Administrators
- **Batch Processing**: Upload CSV/Excel files with multiple patients for bulk risk assessment
- **Summary Statistics**: View risk distribution across patient cohorts
- **Download Results**: Export batch predictions as CSV for further analysis

###  For Patients
- **Simplified Interface**: Easy-to-understand risk estimation without medical jargon
- **Educational Content**: Learn about thyroid cancer and what the numbers mean
- **Next Steps Guidance**: Clear recommendations for follow-up care and support

###  For Researchers
- **Cohort Analysis**: Upload large datasets for statistical analysis
- **Data Exploration**: Descriptive statistics and visualization tools
- **Model Validation**: Framework for testing models on new datasets

##  Demo

The app is currently running in demo mode with simulated predictions. Access it at:
- **Local**: http://localhost:8501


### Sample Screenshots
- Single patient risk assessment with SHAP explanations
- Batch processing results dashboard
- Patient-friendly risk estimation interface

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/kanishkapm/thyroid-cancer-predictor.git
   cd thyroid-cancer-predictor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the app**:
   Open your browser and go to `http://localhost:8501`

##  Usage

### For Clinicians
1. Select " Doctor/Clinician" from the sidebar
2. Fill in patient information:
   - Demographics (age, sex, marital status)
   - Tumor details (size, histology, TNM stage)
   - Treatment history (thyroidectomy, RAI, etc.)
3. Click " PREDICT 5-YEAR RISK"
4. Review results, SHAP explanations, and clinical recommendations
5. Download patient report if needed

### For Hospital Admins
1. Select " Hospital Admin" from the sidebar
2. Upload a CSV file with patient data
3. Click " PREDICT ALL PATIENTS"
4. View batch results and summary statistics
5. Download results as CSV

### For Patients
1. Select " Patient" from the sidebar
2. Answer simple questions about your diagnosis and treatment
3. Click "📊 See My Risk"
4. Read your personalized risk estimate and next steps

### For Researchers
1. Select "📊 Researcher" from the sidebar
2. Upload research cohort data
3. Explore analysis options (risk distribution, feature importance, survival analysis)

## 📊 Data Sources

### Training Data
- **SEER Database**: Surveillance, Epidemiology, and End Results Program
- Historical thyroid cancer patient outcomes
- Features include demographics, tumor characteristics, treatments, and survival data

### Sample Data
- `sample_patients.csv`: 10 sample patient records for testing batch upload
- Columns: age, sex, tumor_size_mm, histology, tnm_stage, thyroidectomy, rai

##  Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .
```

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Disclaimer

**IMPORTANT MEDICAL DISCLAIMER:**

This application is for **educational and research purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.

- All predictions in the current demo version are **simulated** and should not be used for clinical decision-making
- Always consult with qualified healthcare professionals for medical decisions
- Individual patient outcomes may vary significantly based on factors not captured in this model
- The developers and contributors are not liable for any decisions made based on this tool

### For Production Use
- Replace mock models with trained XGBoost models
- Validate on local patient data
- Consult with medical experts before clinical implementation
- Ensure compliance with local healthcare regulations

##  Acknowledgments

- **Data Source**: SEER Program (seer.cancer.gov)
- **Framework**: Streamlit for web app development
- **ML Libraries**: scikit-learn, XGBoost for modeling
- **Explainability**: SHAP for model interpretability

##  Contact

- **GitHub**: [@kanishkapm](https://github.com/kanishkapm)
- **Issues**: [Report bugs or request features](https://github.com/kanishkapm/thyroid-cancer-predictor/issues)

---

**Built with ❤️ for better thyroid cancer care**

