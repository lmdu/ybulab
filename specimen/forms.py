from django import forms

from .models import *

class SampleForm(forms.ModelForm):
	photos = forms.JSONField(widget=forms.MultipleHiddenInput, required=False)
	attachments = forms.JSONField(widget=forms.MultipleHiddenInput, required=False)

	class Meta:
		model = Sample
		fields = ['sample_code', 'sample_name', 'sample_tissue',
			'sample_type', 'collect_location', 'collect_longitude',
			'collect_latitude', 'collect_altitude', 'collect_date',
			'collect_people', 'store_place', 'store_method', 'comment',
			'photos', 'attachments', 'species'
		]
