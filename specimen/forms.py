from django.forms import ModelForm

from .models import *

class SampleForm(ModelForm):
	class Meta:
		model = Sample
		fields = ['sample_code', 'sample_name', 'sample_tissue',
			'sample_type', 'collect_location', 'collect_longitude',
			'collect_latitude', 'collect_altitude', 'collect_date',
			'collect_people', 'store_place', 'store_method', 'comment',
			'photos', 'attachments', 'species'
		]
