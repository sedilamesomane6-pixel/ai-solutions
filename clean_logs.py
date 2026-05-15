import pandas as pd
import numpy as np

print("="*70)
print("DATA CLEANING SCRIPT")
print("="*70)

# Load raw data
print("\nLoading raw data...")
df_raw = pd.read_csv("weblogs_raw_dirty.csv")
print(f"Loaded {len(df_raw):,} records")

# ============================================
# 1. CLEAN TIMESTAMPS
# ============================================
print("\n1. Cleaning timestamps...")
df_raw['timestamp'] = pd.to_datetime(df_raw['timestamp'], errors='coerce')
initial_count = len(df_raw)
df_raw = df_raw.dropna(subset=['timestamp'])
print(f"   Removed {initial_count - len(df_raw):,} records with invalid timestamps")

# ============================================
# 2. CLEAN COUNTRY NAMES
# ============================================
print("\n2. Cleaning country names...")
country_mapping = {
    'south africa': 'South Africa', 'SA': 'South Africa', 'SouthAfrica': 'South Africa',
    'Botswna': 'Botswana', 'Botswanna': 'Botswana',
    'Namib': 'Namibia', 'Zim': 'Zimbabwe', 'Mozambik': 'Mozambique',
    'Zambia!': 'Zambia', 'Angola ': 'Angola', ' eswatini': 'Eswatini'
}
df_raw['country'] = df_raw['country'].replace(country_mapping)
df_raw['country'] = df_raw['country'].str.title()
df_raw.loc[df_raw['country'].isin(['', 'Null', 'Unknown', 'Nan']), 'country'] = 'Other'
print(f"   Standardized {len(country_mapping)} country name variations")

# ============================================
# 3. CLEAN DEPARTMENT NAMES
# ============================================
print("\n3. Cleaning department names...")
df_raw['department'] = df_raw['department'].astype(str).str.strip().str.upper()
df_raw['department'] = df_raw['department'].replace(['', 'NULL', 'H R', 'NAN'], 'OTHER')
print(f"   Standardized department names to uppercase")

# ============================================
# 4. CLEAN HTTP METHODS
# ============================================
print("\n4. Cleaning HTTP methods...")
df_raw['http_method'] = df_raw['http_method'].astype(str).str.strip().str.upper()
df_raw['http_method'] = df_raw['http_method'].replace(['', 'NULL', 'NAN'], 'UNKNOWN')
valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
df_raw.loc[~df_raw['http_method'].isin(valid_methods), 'http_method'] = 'OTHER'

# ============================================
# 5. CLEAN STATUS CODES
# ============================================
print("\n5. Cleaning status codes...")
df_raw['status_code'] = pd.to_numeric(df_raw['status_code'], errors='coerce')
df_raw['status_code'] = df_raw['status_code'].fillna(0).astype(int)
valid_codes = [200, 201, 301, 302, 400, 401, 403, 404, 500, 502, 503]
df_raw.loc[~df_raw['status_code'].isin(valid_codes), 'status_code'] = 0
print(f"   Invalid status codes converted to 0")

# ============================================
# 6. CLEAN LEAD SCORES
# ============================================
print("\n6. Cleaning lead scores...")
df_raw['lead_score'] = pd.to_numeric(df_raw['lead_score'], errors='coerce')
df_raw.loc[(df_raw['lead_score'] < 0) | (df_raw['lead_score'] > 100), 'lead_score'] = 0
df_raw['lead_score'] = df_raw['lead_score'].fillna(0).astype(int)
print(f"   Out-of-range lead scores set to 0")

# ============================================
# 7. CLEAN RESPONSE TIMES
# ============================================
print("\n7. Cleaning response times...")
df_raw['response_time_ms'] = pd.to_numeric(df_raw['response_time_ms'], errors='coerce')
df_raw.loc[df_raw['response_time_ms'] < 0, 'response_time_ms'] = 0
df_raw.loc[df_raw['response_time_ms'] > 5000, 'response_time_ms'] = 5000
df_raw['response_time_ms'] = df_raw['response_time_ms'].fillna(0).astype(int)
print(f"   Negative times set to 0, extreme times capped at 5000ms")

# ============================================
# 8. CLEAN SATISFACTION SCORES
# ============================================
print("\n8. Cleaning satisfaction scores...")
df_raw['satisfaction_score'] = pd.to_numeric(df_raw['satisfaction_score'], errors='coerce')
df_raw.loc[(df_raw['satisfaction_score'] < 1) | (df_raw['satisfaction_score'] > 5), 'satisfaction_score'] = 3
df_raw['satisfaction_score'] = df_raw['satisfaction_score'].fillna(3).astype(int)
print(f"   Invalid scores set to default value of 3")

# ============================================
# 9. CLEAN CONVERSION FLAGS (YES/NO TO BOOLEAN)
# ============================================
print("\n9. Cleaning conversion flags...")
def to_bool(val):
    if pd.isna(val):
        return False
    return str(val).lower() in ['yes', 'true', '1', 'y']

df_raw['conversion_flag'] = df_raw['conversion_flag'].apply(to_bool)
df_raw['ai_assistant_used'] = df_raw['ai_assistant_used'].apply(to_bool)
df_raw['job_applied'] = df_raw['job_applied'].apply(to_bool)
print(f"   Converted yes/no columns to boolean (True/False)")

# ============================================
# 10. CLEAN EMAILS
# ============================================
print("\n10. Cleaning email addresses...")
def is_valid_email(email):
    if pd.isna(email):
        return False
    email_str = str(email)
    return '@' in email_str and '.' in email_str and len(email_str) > 5

df_raw['user_email'] = df_raw['user_email'].astype(str)
df_raw.loc[~df_raw['user_email'].apply(is_valid_email), 'user_email'] = None
print(f"   Invalid emails set to NULL")

# ============================================
# 11. REMOVE DUPLICATES 
# ============================================
print("\n11. Removing duplicates...")
initial_count = len(df_raw)
df_raw = df_raw.drop_duplicates(subset=['log_id', 'timestamp', 'ip_address'])
print(f"   Removed {initial_count - len(df_raw):,} duplicate records")

# ============================================
# 12. REMOVE ROWS WITH CRITICAL MISSING DATA
# ============================================
print("\n12. Removing rows with critical missing data...")
initial_count = len(df_raw)
df_raw = df_raw.dropna(subset=['ip_address', 'url'])
df_raw = df_raw[df_raw['ip_address'] != '']
df_raw = df_raw[df_raw['url'] != '']
print(f"   Removed {initial_count - len(df_raw):,} rows with missing critical data")

# ============================================
# 13. FILL REMAINING NULL VALUES
# ============================================
print("\n13. Filling remaining NULL values...")
df_raw['product_name'] = df_raw['product_name'].fillna('Unknown')
df_raw['browser'] = df_raw['browser'].fillna('Unknown')
df_raw['device_type'] = df_raw['device_type'].fillna('Unknown')
df_raw['campaign_source'] = df_raw['campaign_source'].fillna('organic')
df_raw['client_segment'] = df_raw['client_segment'].fillna('SME')
df_raw['job_type'] = df_raw['job_type'].fillna('None')

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*70)
print("CLEANING COMPLETE")
print("="*70)

print(f"\nOriginal records: {1000000:,}")
print(f"Records after cleaning: {len(df_raw):,}")
print(f"Records removed: {1000000 - len(df_raw):,} ({(1000000 - len(df_raw))/1000000*100:.1f}%)")

print("\nColumn data types after cleaning:")
for col in df_raw.columns:
    print(f"  {col}: {df_raw[col].dtype}")

# Save cleaned data
df_raw.to_csv("weblogs_cleaned.csv", index=False)
print("\nSaved: weblogs_cleaned.csv")

# Also save as Excel for easy viewing
df_raw.to_excel("weblogs_cleaned.xlsx", index=False)
print("Saved: weblogs_cleaned.xlsx")

print("\n" + "="*70)
print("NEXT STEPS")
print("="*70)
print("1. Load weblogs_cleaned.csv into your dashboard")
print("2. Use the cleaned data for analysis and visualizations")
print("3. The data is now ready for the sales analytics dashboard")