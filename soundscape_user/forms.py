from django import forms

class SoundFileUploadForm(forms.Form):
    sound_file = forms.FileField()
    sound_descriptor = forms.CharField(max_length=255)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
