from django import forms
#from django.contrib.auth.models import User
#from django.utils.translation import ugettext_lazy as _

class SlotForm(forms.Form):
    weekday = (
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
    )
    day = forms.ChoiceField(label="Day", choices=weekday)
    start_time = forms.TimeField(widget=forms.TimeInput(), \
        label="Start Time(hh:mm:ss format 24-hour)")
    end_time = forms.TimeField(widget=forms.TimeInput(), \
        label="End Time(hh:mm:ss format 24-hour)")

class DocProfileForm(forms.Form):
    description = forms.CharField(label="About Yourself", \
    widget=forms.Textarea, required=False)
    current_job = forms.CharField(label="Current Job", widget=forms.Textarea)
    location = forms.CharField(label="Current Location")
    address = forms.CharField(label="Address", widget=forms.Textarea)
    phone_no = forms.IntegerField(label="Phone Number")
    prev_exp = forms.CharField(label="Previous Work Experience", \
    widget=forms.Textarea, required=False)
    projects = forms.CharField(label="Projects/Publications", \
    widget=forms.Textarea, required=False)
    memberships = forms.CharField(label="Memberships", \
    widget=forms.Textarea, required=False)
    ug_degree = forms.CharField(label="UG degree")
    ug_college = forms.CharField(label="College/Institution")
    ug_council = forms.CharField(label="Approving Council")
    ug_year = forms.IntegerField(label="Year Of Completion")
    ug_regno = forms.IntegerField(label="Registration Number")
    pg_degree = forms.CharField(label="PG degree")
    pg_college = forms.CharField(label="Institution")
    pg_regno = forms.IntegerField(label="Registration Number")
    pg_council = forms.CharField(label="Approving Council")
    pg_year = forms.IntegerField(label="Year of Graduation")
    others = forms.CharField(label="Other Qualifications", \
    widget=forms.Textarea, required=False)
    consultation_fee = forms.IntegerField(label="Consultation Fee")
