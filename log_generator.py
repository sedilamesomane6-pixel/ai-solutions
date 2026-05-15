import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import string

print("="*70)
print("🌍 WEB SERVER LOG GENERATOR WITH DIRTY DATA")
print("="*70)

# Initialize
fake = Faker()
np.random.seed(42)
random.seed(42)

# Configuration
num_records = 1000000  # 1 Million records
start_date = datetime(2026, 1, 1, 0, 0, 0)
end_date = datetime(2026, 4, 30, 23, 59, 59)

print(f"\n📊 Generating {num_records:,} log records...")
print("⏰ This will take approximately 2-3 minutes...\n")

# ============================================
# DATA DEFINITIONS
# ============================================

# Countries (Southern Africa focus + some dirty data)
countries_clean = [
    "South Africa", "Botswana", "Namibia", "Zimbabwe", 
    "Mozambique", "Zambia", "Angola", "Eswatini", "Lesotho"
]

# Dirty entries to add (misspellings, different cases, abbreviations)
countries_dirty = [
    "south africa", "SA", "Botswna", "Namib", "Zim",
    "Mozambik", "Zambia!", "Angola ", " eswatini", "LESOTHO",
    "Unknown", "NULL", "", " ", "SouthAfrica", "Botswanna"
]

# Combine clean and dirty
countries = countries_clean + countries_dirty

# Regions
regions = ["Southern Africa", "East Africa", "West Africa", "North Africa", "Central Africa", "Unknown", ""]

# Departments
departments_clean = ["HR", "IT", "Sales", "Operations", "Executive", "Marketing", "Finance", "Legal"]
departments_dirty = ["hr", "It", "SALES", " ops ", "EXEC", "marketing", "Fin", "", "NULL", "H R"]
departments = departments_clean + departments_dirty

# HTTP Methods
http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "get", "Post", "GET ", " POST", "", "NULL"]

# Status Codes (including invalid ones for dirty data)
status_codes_valid = [200, 201, 301, 302, 400, 401, 403, 404, 500, 502, 503]
status_codes_invalid = [999, -1, 0, "200", "404", None, "", "error", "OK", "NOT FOUND"]
status_codes = status_codes_valid + status_codes_invalid

# Request Categories
request_categories = ["product", "event", "demo", "assistant", "job", "support", "pricing", "PRODUCT", "Demo", "", "NULL"]

# Product Names
products = [
    "Cyber Assistant", "Prototype Service", "AI Analytics", "Cloud Security", 
    "Data Visualizer", "AutoResponder", "SmartDashboard",
    "Cyber", "AI", "unknown", "", "NULL", None
]

# Action Types
actions = ["browse", "request_demo", "enquire", "schedule", "download", "click", "BROWSE", "Request", "", "NULL"]

# Campaign Sources
campaign_sources = [
    "google_ads", "linkedin_ads", "organic", "direct", "referral", "email_campaign",
    "Facebook", "Twitter", "newsletter", "", "NULL", "unknown"
]

# Client Segments
client_segments = ["SME", "Financial Institution", "Government", "Enterprise", "Startup", "Sme", "GOV", "", "NULL"]

# Browsers (dirty and clean)
browsers = [
    "Chrome", "Firefox", "Safari", "Edge", "Mobile Safari", "Opera",
    "chrome", "CHROME", "firefox ", " safari", "", "NULL", "Unknown Browser"
]

# Device Types
devices = ["Desktop", "Mobile", "Tablet", "desktop", "MOBILE", "", "NULL"]

# ============================================
# HELPER FUNCTIONS FOR DIRTY DATA
# ============================================

def generate_dirty_ip():
    """Generate IP addresses, some invalid"""
    if random.random() < 0.05:  # 5% dirty IPs
        choices = ["256.256.256.256", "999.999.999.999", "invalid", "", "NULL", "0.0.0.0"]
        return random.choice(choices)
    return fake.ipv4()

def generate_dirty_timestamp():
    """Generate timestamps, some with invalid format"""
    if random.random() < 0.03:  # 3% dirty timestamps
        choices = ["invalid-date", "2026-13-01", "", "NULL", "yesterday", "01/01/26"]
        return random.choice(choices)
    return fake.date_time_between(start_date=start_date, end_date=end_date)

def generate_dirty_email():
    """Generate emails, some invalid"""
    if random.random() < 0.04:  # 4% dirty emails
        choices = ["invalidemail", "no-at-sign", "", "NULL", "user@", "@domain.com"]
        return random.choice(choices)
    return fake.email()

def generate_dirty_lead_score():
    """Generate lead scores, some out of range"""
    if random.random() < 0.03:  # 3% dirty lead scores
        return random.choice([-10, 150, 200, 999, -5, "high", "low", None, "", "NULL"])
    return random.randint(0, 100)

def generate_dirty_response_time():
    """Generate response times, some negative or extremely high"""
    if random.random() < 0.04:  # 4% dirty response times
        return random.choice([-100, -1, 10000, 50000, "slow", None, "", "NULL"])
    return random.randint(50, 2000)

# ============================================
# DATA GENERATION LOOP
# ============================================

data = []
batch_size = 50000

for i in range(num_records):
    if i % 100000 == 0 and i > 0:
        print(f"   Generated {i:,} records... ({i/num_records*100:.0f}%)")
    
    # Generate record with dirty data intentionally
    record = {
        # 1. Unique identifier
        "log_id": i + 1,
        
        # 2. Timestamp (some dirty)
        "timestamp": generate_dirty_timestamp(),
        
        # 3. IP Address (some invalid)
        "ip_address": generate_dirty_ip(),
        
        # 4. Country (mix of clean and dirty)
        "country": random.choice(countries),
        
        # 5. Region
        "region": random.choice(regions),
        
        # 6. Department (mix of clean and dirty)
        "department": random.choice(departments),
        
        # 7. HTTP Method (some dirty)
        "http_method": random.choice(http_methods),
        
        # 8. URL / Resource
        "url": fake.uri_path() if random.random() > 0.05 else random.choice(["", "invalid-url", "NULL"]),
        
        # 9. Status Code (some invalid)
        "status_code": random.choice(status_codes),
        
        # 10. Request Category
        "request_category": random.choice(request_categories),
        
        # 11. Product Name
        "product_name": random.choice(products),
        
        # 12. Action Type
        "action_type": random.choice(actions),
        
        # 13. Campaign Source
        "campaign_source": random.choice(campaign_sources),
        
        # 14. Client Segment
        "client_segment": random.choice(client_segments),
        
        # 15. Lead Score (0-100, some dirty)
        "lead_score": generate_dirty_lead_score(),
        
        # 16. Conversion Flag (yes/no, some dirty)
        "conversion_flag": random.choice(["yes", "no", "true", "false", "1", "0", "Y", "N", "", "NULL", "maybe"]),
        
        # 17. User Email (some invalid)
        "user_email": generate_dirty_email(),
        
        # 18. Browser
        "browser": random.choice(browsers),
        
        # 19. Device Type
        "device_type": random.choice(devices),
        
        # 20. Response Time (ms) (some negative or extremely high)
        "response_time_ms": generate_dirty_response_time(),
        
        # 21. Session ID (some missing)
        "session_id": fake.uuid4() if random.random() > 0.02 else random.choice(["", "NULL", "invalid-session"]),
        
        # 22. User Satisfaction Score (1-5, some out of range)
        "satisfaction_score": random.choice([1, 2, 3, 4, 5, 0, 6, "high", "low", None, ""]),
        
        # 23. AI Assistant Used (yes/no, some dirty)
        "ai_assistant_used": random.choice(["yes", "no", "true", "false", "1", "0", "Y", "N", "", "NULL"]),
        
        # 24. Job Applied Flag
        "job_applied": random.choice(["yes", "no", "true", "false", "1", "0", "", "NULL"]),
        
        # 25. Job Type (if applicable)
        "job_type": random.choice([
            "Software Engineer", "Data Scientist", "Product Manager", "", "NULL", 
            "Developer", "Analyst", "unknown", None
        ])
    }
    
    data.append(record)

# ============================================
# CREATE DATAFRAME
# ============================================

print("\n📊 Creating DataFrame...")
df = pd.DataFrame(data)

# ============================================
# EXPORT RAW DIRTY DATA
# ============================================

print("💾 Saving raw dirty data...")
df.to_csv("weblogs_raw_dirty.csv", index=False)
print(f"   ✅ Saved: weblogs_raw_dirty.csv ({len(df):,} records)")

# ============================================
# DATA CLEANING SCRIPT (To be run separately)
# ============================================

cleaning_script = """
# ============================================
# DATA CLEANING SCRIPT
# Run this after loading the raw data
# ============================================

import pandas as pd
import numpy as np

print("🧹 Starting Data Cleaning Process...")

# Load raw data
df_raw = pd.read_csv("weblogs_raw_dirty.csv")
print(f"Loaded {len(df_raw):,} records")

# 1. Clean timestamps
df_raw['timestamp'] = pd.to_datetime(df_raw['timestamp'], errors='coerce')
df_raw = df_raw.dropna(subset=['timestamp'])

# 2. Clean country names (standardize to title case)
country_mapping = {
    'south africa': 'South Africa', 'SA': 'South Africa', 'SouthAfrica': 'South Africa',
    'Botswna': 'Botswana', 'Botswanna': 'Botswana',
    'Namib': 'Namibia', 'Zim': 'Zimbabwe', 'Mozambik': 'Mozambique',
    'Zambia!': 'Zambia', 'Angola ': 'Angola', ' eswatini': 'Eswatini'
}
df_raw['country_clean'] = df_raw['country'].replace(country_mapping)
df_raw['country_clean'] = df_raw['country_clean'].str.title()
df_raw.loc[df_raw['country_clean'].isin(['', 'Null', 'Unknown']), 'country_clean'] = 'Other'

# 3. Clean department names
df_raw['department'] = df_raw['department'].str.strip().str.upper()
df_raw['department'] = df_raw['department'].replace(['', 'NULL', 'H R'], 'OTHER')

# 4. Clean status codes (convert to numeric, invalid become 0)
df_raw['status_code'] = pd.to_numeric(df_raw['status_code'], errors='coerce').fillna(0).astype(int)

# 5. Clean lead scores (out of range become 0)
df_raw['lead_score'] = pd.to_numeric(df_raw['lead_score'], errors='coerce')
df_raw.loc[(df_raw['lead_score'] < 0) | (df_raw['lead_score'] > 100), 'lead_score'] = 0
df_raw['lead_score'] = df_raw['lead_score'].fillna(0).astype(int)

# 6. Clean response times (negative become 0, extreme capped)
df_raw['response_time_ms'] = pd.to_numeric(df_raw['response_time_ms'], errors='coerce')
df_raw.loc[df_raw['response_time_ms'] < 0, 'response_time_ms'] = 0
df_raw.loc[df_raw['response_time_ms'] > 5000, 'response_time_ms'] = 5000
df_raw['response_time_ms'] = df_raw['response_time_ms'].fillna(0).astype(int)

# 7. Clean satisfaction scores
df_raw['satisfaction_score'] = pd.to_numeric(df_raw['satisfaction_score'], errors='coerce')
df_raw.loc[(df_raw['satisfaction_score'] < 1) | (df_raw['satisfaction_score'] > 5), 'satisfaction_score'] = 3
df_raw['satisfaction_score'] = df_raw['satisfaction_score'].fillna(3).astype(int)

# 8. Convert yes/no columns to boolean
def to_bool(val):
    if pd.isna(val):
        return False
    return str(val).lower() in ['yes', 'true', '1', 'y']

df_raw['conversion_flag'] = df_raw['conversion_flag'].apply(to_bool)
df_raw['ai_assistant_used'] = df_raw['ai_assistant_used'].apply(to_bool)
df_raw['job_applied'] = df_raw['job_applied'].apply(to_bool)

# 9. Remove duplicates
df_clean = df_raw.drop_duplicates(subset=['log_id', 'timestamp', 'ip_address'])

# 10. Remove rows with missing critical data
df_clean = df_clean.dropna(subset=['ip_address', 'url'])
df_clean = df_clean[df_clean['ip_address'] != '']

print(f"✅ Cleaning complete!")
print(f"   Records after cleaning: {len(df_clean):,}")
print(f"   Records removed: {len(df_raw) - len(df_clean):,} ({((len(df_raw)-len(df_clean))/len(df_raw)*100):.1f}%)")

# Save cleaned data
df_clean.to_csv("weblogs_cleaned.csv", index=False)
print("💾 Saved: weblogs_cleaned.csv")
"""

print("\n" + "="*70)
print("✅ RAW DATA GENERATION COMPLETE!")
print("="*70)
print(f"\n📁 Files created:")
print(f"   1. weblogs_raw_dirty.csv - {num_records:,} RAW records with dirty data")
print(f"\n📝 Next Steps:")
print(f"   1. Run the cleaning script above to clean the data")
print(f"   2. Or copy the cleaning script to a new file called clean_logs.py")
print(f"   3. Run: python clean_logs.py")
print(f"\n🔍 Dirty data included:")
print(f"   - Misspelled country names (Botswna, Namib, Zim)")
print(f"   - Inconsistent case (south africa, SALES)")
print(f"   - Invalid status codes (999, -1, 'OK')")
print(f"   - Out-of-range lead scores (-10, 150, 999)")
print(f"   - Negative response times (-100, -1)")
print(f"   - Missing values (NULL, empty strings)")
print(f"   - Duplicate records")
print(f"   - Invalid email formats")
print(f"   - Out-of-range satisfaction scores (0, 6, 'high')")

# Save cleaning script to file
with open("clean_logs.py", "w") as f:
    f.write(cleaning_script)

print(f"\n💾 Cleaning script saved as: clean_logs.py")
print("\n🚀 Run the cleaning script: python clean_logs.py")