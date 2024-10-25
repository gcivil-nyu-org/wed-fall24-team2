from django import forms

class SoundFileUploadForm(forms.Form):
    username = forms.CharField(max_length=255)
    sound_file = forms.FileField()
    sound_descriptor = forms.CharField(max_length=255)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
