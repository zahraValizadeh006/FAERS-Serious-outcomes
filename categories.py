"""
categories.py
Loads the FAERS indications file (INDI) and groups each indication
into a disease category using keyword matching.
Output: a DataFrame called indi with a new column category.
"""

import pandas as pd
from pathlib import Path

# Find the indications file automatically in any subfolder
path = next(Path(".").rglob("INDI25Q1.txt"))

# FAERS files are separated by "$", not commas
indi = pd.read_csv(path, sep="$", encoding="latin-1", low_memory=False)

# Keywords for each category.
# Order matters: the first matching category wins.
categories = {
    "Unknown": ["unknown indication"],
    "Cancer": ["cancer", "carcinoma", "myeloma", "lymphoma", "leukaemia", "leukemia", "neoplasm", "tumour", "tumor", "melanoma"],
    "Immunology/Transplant": ["transplant", "graft", "immunosuppress", "immunodeficiency", "angioedema", "urticaria", "hypersensitivity", "bone marrow"],
    "Non-disease use": ["prophylaxis", "premedication", "off label", "ill-defined", "contracept", "vitamin", "foetal", "chemotherapy", "drug therapy"],
    "Blood/Coagulation": ["factor viii", "anticoagul", "haemophilia", "anaemia", "anemia"],
    "Cardiovascular": ["hypertension", "heart", "cardiac", "atrial", "angina", "thrombo", "stroke"],
    "Respiratory": ["asthma", "copd", "pulmonary", "cough", "nasal", "cystic fibrosis", "pneumonia"],
    "Rheumatology": ["arthritis", "arthropathy", "lupus", "ankylosing"],
    "Dermatology": ["dermatitis", "eczema", "psoriasis", "acne"],
    "Gastro": ["crohn", "colitis", "reflux", "gastro", "oesophag", "esophag", "constipation", "diarrh", "nausea", "bowel"],
    "Diabetes/Metabolic": ["diabetes", "weight", "obesity", "cholesterol", "hypothyroid", "osteoporosis"],
    "Neurology": ["migraine", "sclerosis", "parkinson", "epilepsy", "seizure", "alzheimer", "narcolepsy", "cataplexy", "myasthenia", "insomnia"],
    "Pain": ["pain", "neuralgia", "headache"],
    "Psychiatry": ["depression", "schizophrenia", "bipolar", "anxiety", "adhd", "attention deficit"],
    "Infectious": ["hiv", "infection", "hepatitis", "covid"],
}


def get_category(text):
    """Return the first category whose keyword appears in the text."""
    text = str(text).lower()  # lowercase so matching ignores capital letters
    for name, words in categories.items():
        if any(w in text for w in words):
            return name
    return "Other"  # nothing matched


# Apply the function to every indication
indi["category"] = indi["indi_pt"].apply(get_category)