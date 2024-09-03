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
			'photos', 'attachments', 'species', 'status'
		]

class SpecimenForm(forms.ModelForm):
	photos = forms.JSONField(widget=forms.MultipleHiddenInput, required=False)
	attachments = forms.JSONField(widget=forms.MultipleHiddenInput, required=False)

	class Meta:
		model = Specimen
		fields = ['specimen_code', 'specimen_name', 'specimen_gender',
			'collect_location', 'collect_longitude', 'collect_latitude',
			'collect_altitude', 'collect_date', 'collect_people',
			'store_place', 'store_method', 'status', 'comment',
			'photos', 'attachments', 'species'
		]

class SpeciesForm(forms.ModelForm):
	class Meta:
		model = Species
		fields = ['kingdom_en', 'kingdom_cn', 'phylum_en', 'phylum_cn',
			'class_en', 'class_cn', 'order_en', 'order_cn', 'family_en',
			'family_cn', 'genus_en', 'genus_cn', 'species_en', 'species_cn'
		]

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'last_name', 'first_name']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['major', 'resume', 'phone', 'title', 'degree',
			'position', 'status', 'identity'
		]

