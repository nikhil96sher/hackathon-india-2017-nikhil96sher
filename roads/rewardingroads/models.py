from django.db import models
import uuid

INCIDENT_TYPES = (
	(1, "Under Construction Patch"),
	(2, "Pothole Found"),
	(3, "Accident Site"),
	(4, "Others"),
)

state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

class Operator(models.Model):
	name = models.CharField(max_length=255)
	rating = models.DecimalField(default=3.00,max_digits=3,decimal_places=2)

	def __str__(self):
		return self.name

class Traveller(models.Model):
	unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #Unique ID is of a car, not a person
	name = models.CharField(max_length=255)
	trust = models.DecimalField(default=0.50,max_digits=3,decimal_places=2)
	credits = models.IntegerField(default=0)
	def __str__(self):
		return self.name

#Need to combine some reportings into an information with a relevant trust score algorithm
class Report(models.Model):
	reporting_time = models.DateTimeField(auto_now_add=True)
	reporter = models.ForeignKey('Traveller',related_name='report')
	latitude = models.DecimalField(default=0.0,decimal_places=6,max_digits=10)
	longitude = models.DecimalField(default=0.0,decimal_places=6,max_digits=10)
	incident = models.IntegerField(choices=INCIDENT_TYPES,default=4)
	usability = models.DecimalField(default=0.00,decimal_places=2,max_digits=3)
	information = models.ForeignKey('Information',related_name='report') #This would be deduced.
	def __str__(self):
		return self.reporter.name+"-"+str(self.reporting_time)

class Information(models.Model):
	latitude = models.DecimalField(default=0.0,decimal_places=4,max_digits=10)
	longitude = models.DecimalField(default=0.0,decimal_places=4,max_digits=10)
	incident = models.IntegerField(choices=INCIDENT_TYPES,default=4)
	trust = models.DecimalField(default=0.0,decimal_places=2,max_digits=3)
	road = models.ForeignKey('Road',related_name='information')
	def __str__(self):
		return self.road.name+"-"+str(self.trust)

class Road(models.Model):
	name = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(choices=state_choices,max_length=255)
	penalty = models.IntegerField(default=0) # Penalty to the operator for this road.
	operator = models.ForeignKey('Operator',related_name='road')
	def __str__(self):
		return self.name+", "+self.city+", "+self.state+" : "+self.operator.name