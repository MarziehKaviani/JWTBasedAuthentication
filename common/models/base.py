from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CountryAndCitiesBaseModel(TimeBaseModel):
    # city = models.CharField(max_length=59, choices=ALL_CITIES_CHOICES, verbose_name=_("City"))
    # country = models.CharField(max_length=32, choices=COUNTRIES_CHOICES, verbose_name=_("Country"))
    city = models.CharField(max_length=59, verbose_name=_("City"))
    country = models.CharField(max_length=32, verbose_name=_("Country"))

    def __str__(self) -> str:
        return f"{self.city} - {self.country}"

    class Meta:
        abstract = True
