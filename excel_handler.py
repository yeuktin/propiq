import pandas as pd
import io

REQUIRED_COLUMNS = ["property_name","location","price","rental_income","expenses"]
OPTIONAL_COLUMNS = ["property_type","size_sqft","bedrooms","year_built","notes"]

def load_excel(file):
    try:
        raw = file.read()
        filename = getattr(file, "name", "").lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(raw))
        elif filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(raw), engine="xlrd")
        else:
            df = pd.read_excel(io.BytesIO(raw), engine="openpyxl")
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
        return df
    except Exception as e:
        raise ValueError(f"Could not read file: {e}")

def validate_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return len(missing) == 0, missing

def clean_data(df):
    df = df.dropna(subset=REQUIRED_COLUMNS, how="all")
    for col in ["price","rental_income","expenses"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = "Not provided"
        else:
            df[col] = df[col].fillna("Not provided")
    return df.reset_index(drop=True)

def get_properties(file):
    try:
        df = load_excel(file)
    except ValueError as e:
        return [], [str(e)]
    is_valid, missing = validate_columns(df)
    if not is_valid:
        return [], [f"Missing required columns: {missing}"]
    df = clean_data(df)
    if len(df) == 0:
        return [], ["No valid property rows found."]
    return df.to_dict(orient="records"), []

def get_sample_data():
    import pandas as pd
    return pd.DataFrame([
        {"property_name":"King West Condo","location":"Toronto, ON","price":780000,"rental_income":3200,"expenses":950,"property_type":"Condo","size_sqft":620,"bedrooms":1,"year_built":2018,"notes":"Steps to TTC, high demand"},
        {"property_name":"Plateau Duplex","location":"Montreal, QC","price":620000,"rental_income":3800,"expenses":700,"property_type":"Duplex","size_sqft":1400,"bedrooms":3,"year_built":2005,"notes":"Strong rental market"},
        {"property_name":"Beltline Townhouse","location":"Calgary, AB","price":520000,"rental_income":2600,"expenses":550,"property_type":"Townhouse","size_sqft":1100,"bedrooms":2,"year_built":2012,"notes":"No provincial income tax"},
        {"property_name":"Kitsilano 2BR","location":"Vancouver, BC","price":1100000,"rental_income":3800,"expenses":1200,"property_type":"Condo","size_sqft":780,"bedrooms":2,"year_built":2016,"notes":"Near beach, high appreciation"},
        {"property_name":"Centretown Flat","location":"Ottawa, ON","price":480000,"rental_income":2200,"expenses":600,"property_type":"Condo","size_sqft":650,"bedrooms":1,"year_built":2014,"notes":"Near Parliament Hill"},
        {"property_name":"Westmount Triplex","location":"Montreal, QC","price":890000,"rental_income":5400,"expenses":1100,"property_type":"Triplex","size_sqft":2200,"bedrooms":5,"year_built":1998,"notes":"Prestigious area, stable tenants"},
        {"property_name":"Oliver District Condo","location":"Edmonton, AB","price":310000,"rental_income":1800,"expenses":420,"property_type":"Condo","size_sqft":590,"bedrooms":1,"year_built":2017,"notes":"Walkable, near river valley"},
        {"property_name":"Leslieville Semi","location":"Toronto, ON","price":950000,"rental_income":3600,"expenses":980,"property_type":"Semi-Detached","size_sqft":1050,"bedrooms":3,"year_built":2002,"notes":"Gentrifying area, strong upside"},
        {"property_name":"Mission Bungalow","location":"Calgary, AB","price":640000,"rental_income":2800,"expenses":600,"property_type":"Detached","size_sqft":1200,"bedrooms":3,"year_built":1978,"notes":"Renovated, inner city lot"},
        {"property_name":"Corktown Loft","location":"Hamilton, ON","price":420000,"rental_income":2100,"expenses":500,"property_type":"Loft","size_sqft":720,"bedrooms":1,"year_built":2010,"notes":"Art district, growing market"},
        {"property_name":"Roncesvalles House","location":"Toronto, ON","price":1250000,"rental_income":4200,"expenses":1100,"property_type":"Detached","size_sqft":1400,"bedrooms":4,"year_built":1935,"notes":"Prime neighbourhood, land value"},
        {"property_name":"Marda Loop Condo","location":"Calgary, AB","price":390000,"rental_income":2000,"expenses":480,"property_type":"Condo","size_sqft":640,"bedrooms":2,"year_built":2019,"notes":"Popular walkable area"},
        {"property_name":"Griffintown Studio","location":"Montreal, QC","price":340000,"rental_income":1900,"expenses":420,"property_type":"Studio","size_sqft":420,"bedrooms":0,"year_built":2020,"notes":"New development, high rental demand"},
        {"property_name":"Glebe Townhouse","location":"Ottawa, ON","price":720000,"rental_income":3100,"expenses":750,"property_type":"Townhouse","size_sqft":1100,"bedrooms":3,"year_built":2008,"notes":"Family area, near canal"},
        {"property_name":"South Granville Suite","location":"Vancouver, BC","price":880000,"rental_income":3200,"expenses":950,"property_type":"Condo","size_sqft":700,"bedrooms":2,"year_built":2015,"notes":"Luxury area, stable income"},
        {"property_name":"North End Duplex","location":"Halifax, NS","price":380000,"rental_income":2800,"expenses":550,"property_type":"Duplex","size_sqft":1300,"bedrooms":3,"year_built":1990,"notes":"Up and coming market, affordable"},
        {"property_name":"Varsity Condo","location":"Calgary, AB","price":420000,"rental_income":2100,"expenses":490,"property_type":"Condo","size_sqft":710,"bedrooms":2,"year_built":2011,"notes":"Near U of C, reliable student tenants"},
        {"property_name":"Distillery Loft","location":"Toronto, ON","price":680000,"rental_income":2900,"expenses":820,"property_type":"Loft","size_sqft":680,"bedrooms":1,"year_built":2006,"notes":"Tourist area, Airbnb potential"},
        {"property_name":"St Boniface Bungalow","location":"Winnipeg, MB","price":295000,"rental_income":1700,"expenses":380,"property_type":"Detached","size_sqft":1050,"bedrooms":3,"year_built":1965,"notes":"Affordable market, steady cash flow"},
        {"property_name":"Fairview Apartment","location":"Vancouver, BC","price":760000,"rental_income":2900,"expenses":880,"property_type":"Condo","size_sqft":660,"bedrooms":2,"year_built":2013,"notes":"Central location, strong yield"},
    ])
