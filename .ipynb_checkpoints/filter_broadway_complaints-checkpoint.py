import pandas as pd

# Load the original dataset
df = pd.read_csv('Pedestrian_Ramp_Complaints_20250708.csv')

print('🔍 Filtering Broadway complaints...')
print('Original dataset:', len(df), 'rows')

# Filter for Broadway in Street_Name1 or Street_Name2
broadway_complaints = df[
    (df['Street_Name1'].str.contains('BROADWAY', case=False, na=False)) |
    (df['Street_Name2'].str.contains('BROADWAY', case=False, na=False))
].copy()

print('Broadway complaints found:', len(broadway_complaints), 'rows')

# Show which columns contain Broadway
print('\nBroadway mentions by column:')
print('- Street_Name1 = BROADWAY:', len(df[df['Street_Name1'] == 'BROADWAY']))
print('- Street_Name2 = BROADWAY:', len(df[df['Street_Name2'] == 'BROADWAY']))

# Check for any other Broadway variations
broadway_street1_variations = df[df['Street_Name1'].str.contains('BROADWAY', case=False, na=False)]['Street_Name1'].unique()
broadway_street2_variations = df[df['Street_Name2'].str.contains('BROADWAY', case=False, na=False)]['Street_Name2'].unique()

print('\nStreet_Name1 Broadway variations found:')
for variation in broadway_street1_variations:
    count = len(df[df['Street_Name1'] == variation])
    print(f'  {variation}: {count} complaints')

if len(broadway_street2_variations) > 0:
    print('\nStreet_Name2 Broadway variations found:')
    for variation in broadway_street2_variations:
        count = len(df[df['Street_Name2'] == variation])
        print(f'  {variation}: {count} complaints')

# Save to new CSV file
output_filename = 'Broadway_Ramp_Complaints.csv'
broadway_complaints.to_csv(output_filename, index=False)

print(f'\n✅ Broadway complaints saved to: {output_filename}')
print(f'File contains {len(broadway_complaints)} rows and {len(broadway_complaints.columns)} columns')

# Show summary of Broadway data
print('\n📊 BROADWAY COMPLAINTS SUMMARY:')
print('='*50)

# Borough breakdown
print('\nBroadway complaints by borough:')
borough_counts = broadway_complaints['Borough'].value_counts()
for borough, count in borough_counts.items():
    pct = (count / len(broadway_complaints)) * 100
    print(f'  {borough}: {count} ({pct:.1f}%)')

# Date range
if 'Complaint_Date' in broadway_complaints.columns:
    broadway_complaints['Complaint_Date_parsed'] = pd.to_datetime(broadway_complaints['Complaint_Date'], errors='coerce')
    valid_dates = broadway_complaints['Complaint_Date_parsed'].dropna()
    if len(valid_dates) > 0:
        print(f'\nDate range: {valid_dates.min()} to {valid_dates.max()}')
        
        # Yearly breakdown
        yearly_counts = valid_dates.dt.year.value_counts().sort_index()
        print('\nBroadway complaints by year:')
        for year, count in yearly_counts.items():
            print(f'  {year}: {count} complaints')

# Sample records
print(f'\n📋 Sample Broadway Records:')
print('='*30)
for i in range(min(3, len(broadway_complaints))):
    record = broadway_complaints.iloc[i]
    print(f'\nRecord {i+1}:')
    print(f'  Street 1: {record["Street_Name1"]}')
    print(f'  Street 2: {record["Street_Name2"]}')
    print(f'  Borough: {record["Borough"]}')
    print(f'  Complaint Date: {record["Complaint_Date"]}')
    print(f'  Complaint ID: {record["Complaint_ID"]}')

print(f'\n🎯 Successfully created Broadway-only dataset!') 