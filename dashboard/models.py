from django.db import models

# Create your models here.
class CityInfos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    cityname = models.CharField(db_column='CityName', max_length=255)  # Field name made lowercase.
    temperature = models.CharField(db_column='Temperature', max_length=255)  # Field name made lowercase.
    humidity = models.CharField(db_column='Humidity', max_length=255)  # Field name made lowercase.
    c_date = models.DateTimeField(db_column='C_date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'city_infos'
