from django.db import models
from django.utils.dateformat import DateFormat
from django.contrib.auth.models import User


class Car(models.Model):
    user = models.ForeignKey(User)
    label = models.CharField(max_length=250)
    date_purchased = models.DateField()
    initial_cost = models.PositiveIntegerField(default=0)
    initial_mileage = models.PositiveIntegerField(default=0)
    mileage = models.PositiveIntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        if self.mileage == 0:
            self.mileage = self.initial_mileage
        super(Car, self).save(*args, **kwargs)

    def get_total_maintenance_cost(self):
        entries = Entry.objects.filter(car=self)
        total = 0
        for entry in entries:
            if entry.cost_of_parts:
                total += entry.cost_of_parts
            if entry.cost_of_service:
                total += entry.cost_of_service
        return total

    def get_total_parts_cost(self):
        entries = Entry.objects.filter(car=self)
        total = 0
        for entry in entries:
            if entry.cost_of_parts:
                total += entry.cost_of_parts
        return total

    def get_total_service_cost(self):
        entries = Entry.objects.filter(car=self)
        total = 0
        for entry in entries:
            if entry.cost_of_service:
                total += entry.cost_of_service
        return total

    def get_total_car_cost(self):
        entries = Entry.objects.filter(car=self)
        total = 0
        for entry in entries:
            if entry.cost_of_parts:
                total += entry.cost_of_parts
            if entry.cost_of_service:
                total += entry.cost_of_service
        if self.initial_cost:
            total += self.initial_cost
        return total


class Entry(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField()
    car = models.ForeignKey('Car', related_name='car')
    mileage = models.PositiveIntegerField(blank=True, null=True, default=0)
    service_type = models.CharField(max_length=250, blank=True, null=True, default="")
    service_location = models.CharField(max_length=250, blank=True, null=True, default="")
    contact_name = models.CharField(max_length=250, blank=True, null=True, default='')
    contact_number = models.CharField(max_length=15, blank=True, default='')
    cost_of_parts = models.IntegerField(blank=True, null=True, default=0)
    cost_of_service = models.IntegerField(blank=True, null=True, default=0)
    comments = models.TextField(blank=True, null=True, default="")

    def __unicode__(self):
        df = DateFormat(self.date)

        label = self.service_type or ""
        return str(df.format("d M y")) + "- " + str(self.car) + ": " + label

    def __repr__(self):
        df = DateFormat(self.date)

        label = self.service_type or ""
        return str(df.format("d M y")) + "- " + str(self.car) + ": " + label

    def get_total_cost(self):
        return self.cost_of_parts + self.cost_of_service