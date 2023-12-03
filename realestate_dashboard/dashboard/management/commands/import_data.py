from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from dashboard.models import City, SaleDataset, SaleDataEntry, RentDataset, RentDataEntry
import os
import pandas as pd
import random
from datetime import datetime
from dashboard.utils import *
from django.conf import settings


class Command(BaseCommand):
    help = 'Import data from Excel files into the PostgreSQL database'

    def add_arguments(self, parser):
        # Optional argument to override paths
        parser.add_argument(
            '--path',
            nargs='+',
            help='Specify a custom path or paths to Excel files'
        )


    def handle(self, *args, **options):
        # Define the paths
        paths = settings.EXCEL_FILES_PATHS
        
        # Collect all the Excel files from the provided directories
        all_excel_files = []
        for path in paths:
            if os.path.isdir(path):
                for filename in os.listdir(path):
                    if filename.endswith('.xlsx') or filename.endswith('.xls'):
                        all_excel_files.append(os.path.join(path, filename))
            else:
                self.stdout.write(self.style.ERROR(f'{path} is not a valid directory'))

        # Process each Excel file
        for file_path in all_excel_files:
            self.stdout.write(self.style.SUCCESS(f'Processing file {file_path}'))
            try:
                with transaction.atomic():
                    self.process_file(file_path)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing file {file_path}: {e}'))

    def process_file(self, file_path):
        filename = os.path.basename(file_path)
        city_name, data_type, _, date_str = filename.replace('.xlsx', '').replace('.xls', '').split('_')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        city = city_name.capitalize()

        # Extract time for date
        calendar_year = date_obj.year
        calendar_month = date_obj.month
        calendar_week = date_obj.isocalendar().week

        # Create or get city instance
        city_instance, created = City.objects.get_or_create(name=city)

        #HERE I NEED THE CODE THAT IS CHECKING IF THE DATA IS ALLREADY THERE


        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        total_raw = len(df)

        if "SALE" in filename:
            df_clean = sale_dataframe_cleaner(df, date_obj)
            df_for_dataentry = sale_extract_for_data_entry(df_clean)
            statistics = extract_for_data_set(df_for_dataentry)
            self.create_sale_entries(city_instance, df_for_dataentry, statistics, total_raw, calendar_year, calendar_month, calendar_week)

        elif "RENT" in filename:
            df_clean = rent_dataframe_cleaner(df, date_obj)
            df_for_dataentry = rent_extract_for_data_entry(df_clean)
            statistics = extract_for_data_set(df_for_dataentry)

            self.create_rent_entries(city_instance, df_for_dataentry, statistics, total_raw, calendar_year, calendar_month, calendar_week)


    def create_sale_entries(self, city_instance, df_for_dataentry, statistics, total_raw, calendar_year, calendar_month, calendar_week):
        # Create a dataset instance, now including the calendar time data
        dataset_instance = self.create_dataset_instance(
            SaleDataset,
            city_instance,
            statistics,
            total_raw,
            calendar_year,
            calendar_month,
            calendar_week
        )

        # Iterate over cleaned data entries and create SaleDataEntry instances
        for _, entry in df_for_dataentry.iterrows():
            SaleDataEntry.objects.create(
                dataset=dataset_instance,
                **entry.to_dict()
            )

    def create_rent_entries(self, city_instance, df_for_dataentry, statistics, total_raw, calendar_year, calendar_month, calendar_week):
        # Create a dataset instance, now including the calendar time data
        dataset_instance = self.create_dataset_instance(
            RentDataset,
            city_instance,
            statistics,
            total_raw,
            calendar_year,
            calendar_month,
            calendar_week
        )

        # Iterate over cleaned data entries and create RentDataEntry instances
        for _, entry in df_for_dataentry.iterrows():
            RentDataEntry.objects.create(
                dataset=dataset_instance,
                **entry.to_dict()
            )

    def create_dataset_instance(self, model, city_instance, statistics, total_raw,calendar_year, calendar_month, calendar_week):
        # Here you can add additional logic to check if the dataset already exists
        # based on the city and date or any other criteria
        return model.objects.create(
            city=city_instance,
            calendar_year=calendar_year,       # Add this line
            calendar_month=calendar_month,     # Add this line
            calendar_week=calendar_week,       # Add this line
            total_clean_entries=statistics['Total Entries'],
            total_raw=total_raw, 
            average_price = statistics['Average Price'],
            average_price_per_sqm = statistics['Average Price per Sqm'],
            average_size = statistics['Average Size'],
            average_year_of_construction = statistics['Average Year of Construction'],
            median_price = statistics['Median Price'],
            median_price_per_sqm = statistics['Median Price per Sqm'],
            median_size = statistics['Median Size'],
            median_year_of_construction = statistics['Median Year of Construction'],
            std_dev_price = statistics['Standard Deviation Price'],
            std_dev_price_per_sqm = statistics['Standard Deviation Price per Sqm'],
            std_dev_size = statistics['Standard Deviation Size'],
            mode_year_of_construction = statistics['Mode Year of Construction'],
            highest_price = statistics['Highest Price'],
            highest_price_link = statistics['Highest Price Link'],
            highest_price_per_sqm = statistics['Highest Price per Sqm'],
            highest_price_per_sqm_link = statistics['Highest Price per Sqm Link'],
            lowest_price = statistics['Lowest Price'],
            lowest_price_link = statistics['Lowest Price Link'],
            lowest_price_per_sqm = statistics['Lowest Price per Sqm'],
            lowest_price_per_sqm_link = statistics['Lowest Price per Sqm Link'],

            # Add other fields from statistics as needed, e.g., average_price=statistics['Average Price']
            # You may need to adjust field names to match your model fields
        )

