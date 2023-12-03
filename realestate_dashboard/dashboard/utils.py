import pandas as pd

sale_column_mapping = {
    'Županija': 'county',
    'Grad/općina': 'city_or_municipality',
    'Naselje': 'settlement',
    'Tip stana': 'apartment_type',
    'Vlastita šifra objekta': 'custom_object_code',
    'Godina izgradnje': 'year_of_construction',
    'Cijena': 'price',
    'Link': 'link',
    'Datum': 'date',
    'Stambena površina u m2': 'residential_area_sqm',
    'email': 'email',
    'tel ili mobitel': 'phone_or_mobile',
    "€/m²": "price_per_sqm",
    "days_online": "days_online"
}



def sale_dataframe_cleaner(df, date):
    df = df.copy()
    for col in sale_column_mapping.keys():
        if col not in df.columns:
            continue
    
    # Convert columns to appropriate data types
    df["Cijena"] = df["Cijena"].str.replace(r'[^\d,]', '', regex=True).str.replace(',', '.').astype(float)
    if df["Stambena površina u m2"].dtype != 'O':
            df["Stambena površina u m2"] = df["Stambena površina u m2"].astype(str)
    df["Stambena površina u m2"] = df["Stambena površina u m2"].str.replace(",", ".").astype(float)
    
    # Filter out unrealistic values
    df = df[(df["Cijena"] > 10000) & (df["Stambena površina u m2"] > 10) & (df["Stambena površina u m2"] < 10000)]
    
    # Additional transformations
    df["price_per_sqm"] = round(df["Cijena"] / df["Stambena površina u m2"], 2)

    df['Godina izgradnje'] = pd.to_numeric(df['Godina izgradnje'], errors='coerce')  # Convert to numbers, set errors to NaN
    df['Godina izgradnje'].replace(-1, None, inplace=True)  # Replace -1 with None
    df['Godina izgradnje'] = df['Godina izgradnje'].apply(lambda x: int(x) if pd.notnull(x) else None)


    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")
    df['days_online'] = (date - df['Datum'].dt.date).apply(lambda x: x.days)
    
    # Rename columns
    df.rename(columns=sale_column_mapping, inplace=True)
    
    # Check for duplicates
    if df.duplicated().sum():
        print(f"Found {df.duplicated().sum()} duplicate rows. Consider handling them.")
    

    return df



def sale_extract_for_data_entry(df):
    missing_columns = [col for col in sale_column_mapping.values() if col not in df.columns]
    if missing_columns:
        print(f"Missing columns in the dataframe: {missing_columns}")
        print(df)
        return None
    # Make a copy of the filtered dataframe to avoid setting-with-copy warning
    df_filtered = df[list(sale_column_mapping.values())].copy()
    # Replace NaN values in 'year_of_construction' with 1234
    df_filtered['year_of_construction'] = df_filtered['year_of_construction'].fillna(value=1234)
    print("YEAH")
    return df_filtered




rent_column_mapping = {
    'Županija': 'county',
    'Grad/općina': 'city_or_municipality',
    'Naselje': 'settlement',
    'Tip stana': 'apartment_type',
    'Cijena': 'price',
    'Link': 'link',
    'Stambena površina u m2': 'residential_area_sqm',
    'Datum': 'date',
    "€/m²": "price_per_sqm",
    "days_online": "days_online",
    'Godina izgradnje': 'year_of_construction',

}

def rent_dataframe_cleaner(df, date):
    df = df.copy()
    for col in rent_column_mapping.keys():
        if col not in df.columns:
            continue
    
    # Convert columns to appropriate data types
    df["Cijena"] = df["Cijena"].str.replace(r'[^\d,]', '', regex=True).str.replace(',', '.').astype(float)
    if df["Stambena površina u m2"].dtype != 'O':
            df["Stambena površina u m2"] = df["Stambena površina u m2"].astype(str)
    df["Stambena površina u m2"] = df["Stambena površina u m2"].str.replace(",", ".").astype(float)    
    # Filter out unrealistic values
    df = df[(df["Cijena"] > 100) & (df["Cijena"] < 6000) & (df["Stambena površina u m2"] > 10) & (df["Stambena površina u m2"] < 10000)]
    
    # Additional transformations
    df["price_per_sqm"] = round(df["Cijena"] / df["Stambena površina u m2"], 2)
    df['Godina izgradnje'] = pd.to_numeric(df['Godina izgradnje'], errors='coerce')  # Convert to numbers, set errors to NaN
    df['Godina izgradnje'].replace(-1, None, inplace=True)  # Replace -1 with None
    df['Godina izgradnje'] = df['Godina izgradnje'].apply(lambda x: int(x) if pd.notnull(x) else None)

    
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

    df['days_online'] = (date - df['Datum'].dt.date).apply(lambda x: x.days)
    
    # Rename columns
    df.rename(columns=sale_column_mapping, inplace=True)
    
    # Check for duplicates
    if df.duplicated().sum():
        print(f"Found {df.duplicated().sum()} duplicate rows. Consider handling them.")
    
    return df

def rent_extract_for_data_entry(df):
    missing_columns = [col for col in rent_column_mapping.values() if col not in df.columns]
    if missing_columns:
        print(f"Missing columns in the dataframe: {missing_columns}")
        print(df)
        return None
    df_filtered = df[list(rent_column_mapping.values())].copy()

    df_filtered['year_of_construction'] = df_filtered['year_of_construction'].fillna(value=1234)
    print("RENT_YEAH")
    return df_filtered



def extract_for_data_set(df):
    # Reset index to avoid potential reindexing issues
    df = df.reset_index(drop=True)
    
    # Total number of entries
    total_entries = len(df)
    
    # Average values
    average_price = round(df['price'].mean(), 2)
    average_price_per_sqm = round(df['price_per_sqm'].mean(), 2)
    average_size = round(df['residential_area_sqm'].mean(), 2)
    

    # Define the placeholder value
    placeholder_value = 1234

    # Filter out entries where 'year_of_construction' is None or equals the placeholder value
    df_valid_years = df[df['year_of_construction'].notnull() & (df['year_of_construction'] != placeholder_value)]

    # Now calculate the average and mode, ensuring that the DataFrame is not empty
    average_year = round(df_valid_years['year_of_construction'].mean(), 2) if not df_valid_years.empty else None
    mode_year_of_construction = df_valid_years['year_of_construction'].mode().iloc[0] if not df_valid_years['year_of_construction'].mode().empty else None
  
    # Median values
    median_price = round(df['price'].median(), 2)
    median_price_per_sqm = round(df['price_per_sqm'].median(), 2)
    median_size = round(df['residential_area_sqm'].median(), 2)
    median_year = round(df_valid_years['year_of_construction'].astype('float').median(), 2)

    # Standard deviation
    std_price = round(df['price'].std(), 2)
    std_price_per_sqm = round(df['price_per_sqm'].std(), 2)
    std_size = round(df['residential_area_sqm'].std(), 2)


    
    # Highest values
    df = df.reset_index(drop=True)

    highest_price = round(df['price'].max(), 2)
    highest_price_row = df[df['price'] == highest_price].iloc[0]
    highest_price_link = highest_price_row['link']

    highest_price_per_sqm = round(df['price_per_sqm'].max(), 2)
    highest_price_per_sqm_row = df[df['price_per_sqm'] == highest_price_per_sqm].iloc[0]
    highest_price_per_sqm_link = highest_price_per_sqm_row['link']

    # Lowest values
    lowest_price = round(df['price'].min(), 2)
    lowest_price_link = df[df['price'] == lowest_price].reset_index(drop=True)['link'].iloc[0]
    lowest_price_per_sqm = round(df['price_per_sqm'].min(), 2)
    lowest_price_per_sqm_link = df[df['price_per_sqm'] == lowest_price_per_sqm].reset_index(drop=True)['link'].iloc[0]

    # Packaging the results into a dictionary
    statistics = {
        'Total Entries': total_entries,
        'Average Price': average_price,
        'Average Price per Sqm': average_price_per_sqm,
        'Average Size': average_size,
        'Average Year of Construction': average_year,
        'Median Price': median_price,
        'Median Price per Sqm': median_price_per_sqm,
        'Median Size': median_size,
        'Median Year of Construction': median_year,
        'Standard Deviation Price': std_price,
        'Standard Deviation Price per Sqm': std_price_per_sqm,
        'Standard Deviation Size': std_size,
        'Mode Year of Construction': mode_year_of_construction,
        'Highest Price': highest_price,
        'Highest Price Link': highest_price_link,
        'Highest Price per Sqm': highest_price_per_sqm,
        'Highest Price per Sqm Link': highest_price_per_sqm_link,
        'Lowest Price': lowest_price,
        'Lowest Price Link': lowest_price_link,
        'Lowest Price per Sqm': lowest_price_per_sqm,
        'Lowest Price per Sqm Link': lowest_price_per_sqm_link
    }
    
    return statistics