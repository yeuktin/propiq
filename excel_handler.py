import pandas as pd
from typing import Union
import io

REQUIRED_COLUMNS = [
    "property_name",
    "location",
    "price",
    "rental_income",
    "expenses",
]

OPTIONAL_COLUMNS = [
    "property_type",
    "size_sqft",
    "bedrooms",
    "year_built",
    "notes",
]

def load_excel(file: Union[str, io.BytesIO]) -> pd.DataFrame:
    """Load Excel or CSV file and return a DataFrame."""
    try:
        if isinstance(file, str):
            if file.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, engine="openpyxl")
        else:
            df = pd.read_excel(file, engine="openpyxl")

        # Clean column names — lowercase, strip spaces
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
        return df

    except Exception as e:
        raise ValueError(f"Could not read file: {e}")


def validate_columns(df: pd.DataFrame) -> tuple[bool, list]:
    """Check required columns exist. Returns (is_valid, missing_columns)."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return len(missing) == 0, missing


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove empty rows, fix data types, fill missing optionals."""
    # Drop rows where all required fields are empty
    df = df.dropna(subset=REQUIRED_COLUMNS, how="all")

    # Convert numeric columns
    for col in ["price", "rental_income", "expenses"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill optional columns with sensible defaults
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = "Not provided"
        else:
            df[col] = df[col].fillna("Not provided")

    return df.reset_index(drop=True)


def get_properties(file) -> tuple[list[dict], list[str]]:
    """
    Main function — takes uploaded file, returns list of property dicts.
    Returns: (properties, errors)
    """
    errors = []

    try:
        df = load_excel(file)
    except ValueError as e:
        return [], [str(e)]

    is_valid, missing = validate_columns(df)
    if not is_valid:
        return [], [f"Missing required columns: {missing}. Please check your Excel file."]

    df = clean_data(df)

    if len(df) == 0:
        return [], ["No valid property rows found in the file."]

    properties = df.to_dict(orient="records")
    return properties, errors


def get_sample_data() -> pd.DataFrame:
    """Returns sample data so users can see the expected format."""
    return pd.DataFrame([
        {
            "property_name": "Orchard Heights",
            "location": "Orchard, Singapore",
            "price": 1500000,
            "rental_income": 4500,
            "expenses": 800,
            "property_type": "Condo",
            "size_sqft": 850,
            "bedrooms": 2,
            "year_built": 2015,
            "notes": "Near MRT"
        },
        {
            "property_name": "Wan Chai Flat",
            "location": "Wan Chai, Hong Kong",
            "price": 8000000,
            "rental_income": 22000,
            "expenses": 3000,
            "property_type": "Apartment",
            "size_sqft": 600,
            "bedrooms": 1,
            "year_built": 2008,
            "notes": "City view"
        },
        {
            "property_name": "JB Terrace House",
            "location": "Johor Bahru, Malaysia",
            "price": 450000,
            "rental_income": 1800,
            "expenses": 300,
            "property_type": "Landed",
            "size_sqft": 1800,
            "bedrooms": 3,
            "year_built": 2019,
            "notes": "Near customs"
        },
    ])