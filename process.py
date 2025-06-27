import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def issue_to_date(issue):
    """
    Convert an issue number to a date.
    
    Parameters:
    issue (int): The issue number, where issue 1 corresponds to 01/01/1990
                 and each subsequent issue is 3 months later.
    
    Returns:
    str: A date string in MM/DD/YYYY format
    """
    if issue < 1:
        raise ValueError("Issue number must be 1 or greater")
    
    # Start date: January 1, 1990
    start_year = 1990
    start_month = 1
    start_day = 1
    
    # Calculate how many years and months to add
    months_to_add = (issue - 1) * 3
    years_to_add = months_to_add // 12
    remaining_months = months_to_add % 12
    
    # Calculate the new year and month
    new_year = start_year + years_to_add
    new_month = start_month + remaining_months
    
    # Adjust if month exceeds 12
    if new_month > 12:
        new_year += 1
        new_month -= 12
    
    # Format the date as MM/DD/YYYY
    return f"{new_month:02d}/{start_day:02d}/{new_year}"


country_code_map = {
    "Afghanistan": "AF",
    "Albania": "AL",
    "Algeria": "DZ",
    "Angola": "AO",
    "Argentina": "AR",
    "Armenia": "AM",
    "Aruba": "AW",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Belarus": "BY",
    "Belgium": "BE",
    "Bolivia (Plurinational State of)": "BO",
    "Bosnia and Herzegovina": "BA",
    "Brazil": "BR",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Cabo Verde": "CV",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Chile": "CL",
    "China": "CN",
    "China, Hong Kong SAR": "HK",
    "China, Macao SAR": "MO",
    "China, Taiwan Province of China": "TW",
    "Colombia": "CO",
    "Congo": "CG",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cuba": "CU",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "Côte d'Ivoire": "CI",
    "Dem. People's Rep. of Korea": "KP",
    "Dem. Rep. of the Congo": "CD",
    "Denmark": "DK",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Greece": "GR",
    "Guam": "GU",
    "Guatemala": "GT",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Honduras": "HN",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran (Islamic Republic of)": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Malaysia": "MY",
    "Malta": "MT",
    "Mexico": "MX",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Morocco": "MA",
    "Myanmar": "MM",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Nigeria": "NG",
    "North Macedonia": "MK",
    "Northern Mariana Islands": "MP",
    "Norway": "NO",
    "Pakistan": "PK",
    "Panama": "PA",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Puerto Rico": "PR",
    "Qatar": "QA",
    "Republic of Korea": "KR",
    "Republic of Moldova": "MD",
    "Romania": "RO",
    "Russian Federation": "RU",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Spain": "ES",
    "Sudan": "SD",
    "Suriname": "SR",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syrian Arab Republic": "SY",
    "Tajikistan": "TJ",
    "Thailand": "TH",
    "Togo": "TG",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkmenistan": "TM",
    "Türkiye": "TR",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "United Kingdom": "UK",  # Note: ISO standard is actually "GB", but using "UK" to match your list
    "United States of America": "US",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Venezuela (Bolivarian Republic of)": "VE",
    "Viet Nam": "VN",
    "South Africa": "ZA",
    "Zambia": "ZM",
    "Zimbabwe": "ZW"
}

if __name__ == "__main__":
    # df = pd.read_csv("merged_fighter_data.csv")
    # pop_df = pd.read_csv("pop_data.csv")
    # pop_df["flag"] = pop_df["Location"].map(country_code_map)
    # df = df.merge(pop_df, on="flag", how="left")
    # df.to_csv("processed_fighter_data.csv", index=False)
    df = pd.read_csv("processed_fighter_data.csv")
    df = df.drop_duplicates(subset=["flag", "Location"])

    # Optional: Display the unique countries and their codes
    df[["flag", "Location", "name"]].to_csv("country_codes.csv", index=False)

