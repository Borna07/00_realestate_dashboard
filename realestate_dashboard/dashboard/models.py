from django.db import models

# City Model
class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    size = models.FloatField(help_text="Size of the city in square kilometers.")
    web_link_sale = models.URLField(blank=True, null=True)
    web_link_rent = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# Sale Dataset Model
class SaleDataset(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    total_clean_entries = models.PositiveIntegerField()
    total_raw = models.PositiveIntegerField()
    calendar_week = models.PositiveIntegerField()
    calendar_month = models.PositiveIntegerField()
    calendar_year = models.PositiveIntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    average_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    average_size = models.FloatField()
    average_year_of_construction = models.PositiveIntegerField(null=True)
    median_price = models.DecimalField(max_digits=10, decimal_places=2)
    median_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    median_size = models.FloatField()
    median_year_of_construction = models.PositiveIntegerField()
    std_dev_price = models.DecimalField(max_digits=10, decimal_places=2)
    std_dev_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    std_dev_size = models.FloatField()
    mode_year_of_construction = models.PositiveIntegerField()
    highest_price = models.DecimalField(max_digits=10, decimal_places=2)
    highest_price_link = models.URLField(blank=True, null=True)
    highest_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    highest_price_per_sqm_link = models.URLField(blank=True, null=True)
    lowest_price = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price_link = models.URLField(blank=True, null=True)
    lowest_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price_per_sqm_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.city.name}_SALE_DATASET_KW{self.calendar_week}_{self.calendar_year}"



# Sale DataEntry Model
class SaleDataEntry(models.Model):
    dataset = models.ForeignKey(SaleDataset, on_delete=models.CASCADE, related_name="sale_data_entries")
    county = models.CharField(max_length=255)
    city_or_municipality = models.CharField(max_length=255)
    settlement = models.CharField(max_length=255, blank=True, null=True)
    # number_of_rooms = models.PositiveIntegerField()
    # number_of_apartment_floors = models.PositiveIntegerField()
    apartment_type = models.CharField(max_length=255)
    custom_object_code = models.CharField(max_length=255)
    year_of_construction = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()
    date = models.DateField()
    residential_area_sqm = models.FloatField()
    email = models.EmailField(blank=True, null=True)
    phone_or_mobile = models.CharField(max_length=20, blank=True, null=True)
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    days_online = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.dataset.city.name}_SALE_DATAENTRY_KW{self.dataset.calendar_week}_{self.dataset.calendar_year}"


# Rent Dataset Model
class RentDataset(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    total_clean_entries = models.PositiveIntegerField()
    total_raw = models.PositiveIntegerField()
    calendar_week = models.PositiveIntegerField()
    calendar_month = models.PositiveIntegerField()
    calendar_year = models.PositiveIntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    average_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    average_size = models.FloatField()
    average_year_of_construction = models.PositiveIntegerField(null=True)
    median_price = models.DecimalField(max_digits=10, decimal_places=2)
    median_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    median_size = models.FloatField()
    median_year_of_construction = models.PositiveIntegerField()
    std_dev_price = models.DecimalField(max_digits=10, decimal_places=2)
    std_dev_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    std_dev_size = models.FloatField()
    mode_year_of_construction = models.PositiveIntegerField()
    highest_price = models.DecimalField(max_digits=10, decimal_places=2)
    highest_price_link = models.URLField(blank=True, null=True)
    highest_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    highest_price_per_sqm_link = models.URLField(blank=True, null=True)
    lowest_price = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price_link = models.URLField(blank=True, null=True)
    lowest_price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price_per_sqm_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.city.name}_RENT_DATASET_KW{self.calendar_week}_{self.calendar_year}"



# Rent DataEntry Model
class RentDataEntry(models.Model):
    dataset = models.ForeignKey(RentDataset, on_delete=models.CASCADE, related_name="rent_data_entries")
    county = models.CharField(max_length=255)
    city_or_municipality = models.CharField(max_length=255)
    settlement = models.CharField(max_length=255, blank=True, null=True)
    # number_of_rooms = models.PositiveIntegerField()
    # number_of_apartment_floors = models.PositiveIntegerField()
    year_of_construction = models.PositiveIntegerField(null=True, blank=True)
    apartment_type = models.CharField(max_length=255)
    custom_object_code = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()
    date = models.DateField()
    residential_area_sqm = models.FloatField()
    email = models.EmailField(blank=True, null=True)
    phone_or_mobile = models.CharField(max_length=20, blank=True, null=True)
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    days_online = models.PositiveIntegerField()
    #rijeka_RENT_RAW_2022-12-02
    def __str__(self):
        return f"{self.dataset.city.name}_RENT_DATAENTRY_KW{self.dataset.calendar_week}_{self.dataset.calendar_year}"