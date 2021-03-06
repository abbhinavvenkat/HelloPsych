from django.forms import ModelForm, CharField, \
    Textarea, CheckboxSelectMultiple, \
    MultipleChoiceField, \
    ModelChoiceField, ChoiceField, \
    IntegerField
from prescription.models import generic, brand, \
    prescription
from django.conf import settings
from django.forms.widgets import TextInput

class NumberInput(TextInput):
    input_type = 'number'

class PrescriptionForm(ModelForm):
    '''
         Store the Prescription for every corresponding appointment made.
    '''
    concern = MultipleChoiceField(required=False, \
        widget=CheckboxSelectMultiple, choices=settings.SPECIALIZATION)
    symptoms = CharField(label="Symptoms", \
        widget=Textarea(attrs={'rows': 1}), required=False)
    doctor_comments = CharField(label="Doctor's Notes", \
        widget=Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = prescription
        fields = ['concern', 'symptoms']

    def __init__(self, *args, **kwargs):
        count = kwargs.pop('count')
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        Frequency = (
             ('Daily', 'Daily'),
             ('Twice a Day', 'Twice a Day'),
             ('Weekly', 'Weekly'),
             ('Monthly', 'Monthly'),
        )
        TimePeriods = (
             ('Once', 'Once'),
             ('Twice', 'Twice'),
             ('')
        )

        for i in range(count):
            self.fields['dosage_%s' % i]=ModelChoiceField(label="Generic", \
                  queryset=generic.objects.all().order_by('name'))
            self.fields['brand_%s' % i]=ModelChoiceField(label="Brand", \
                  queryset=brand.objects.all().order_by('name'))
            self.fields['freq_%s' % i]=ChoiceField(label="Frequency", choices=Frequency)
            self.fields['duration_%s' % i]=IntegerField(label="No. of Days(for Medicine)", \
                widget=NumberInput(attrs={'min':1, 'step': 1, 'rows': 1}))
            self.fields['comment_%s' % i]=CharField(label='Comment', \
                  widget=Textarea(attrs={'rows': 1}), required=False, initial='')


            
import django_filters

class PrescriptionFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label='Prescription ID', \
        lookup_type=['exact', 'gt', 'gte', 'lt', 'lte'])
    appointment__id = django_filters.NumberFilter(label='Appointment ID', \
        lookup_type=['exact','gt', 'gte', 'lt', 'lte'])
    appointment__date_booked = django_filters.DateFilter(label='Date Appointment Booked (YYYY-MM-DD)', \
        lookup_type=['exact','gt', 'gte', 'lt', 'lte'])
    patient__username = django_filters.CharFilter(label='Patient Username', \
        lookup_type=['icontains', 'contains', 'exact'])
    class Meta:
        model = prescription
        fields = {
            'patient__username': [],
        }
        order_by = (
            ('dts', 'DateTime'),
            ('id', 'Prescription ID'),
        )

class PrescriptionFilter2(django_filters.FilterSet):
    id = django_filters.NumberFilter(label='Prescription ID', \
        lookup_type=['exact', 'gt', 'gte', 'lt', 'lte'])
    appointment__id = django_filters.NumberFilter(label='Appointment ID', \
        lookup_type=['exact','gt', 'gte', 'lt', 'lte'])
    appointment__date_booked = django_filters.DateFilter(label='Date Appointment Booked (YYYY-MM-DD)', \
        lookup_type=['exact','gt', 'gte', 'lt', 'lte'])
    doc__username = django_filters.CharFilter(label='Doctor Username', \
        lookup_type=['icontains', 'contains', 'exact'])
    doc__first_name = django_filters.CharFilter(label='Doctor First name', \
        lookup_type=['icontains', 'contains', 'exact'])
    doc__last_name = django_filters.CharFilter(label='Doctor Last name', \
        lookup_type=['icontains', 'contains', 'exact'])
    class Meta:
        model = prescription
        fields = {
            'patient__username': [],
        }
        order_by = (
            ('dts', 'DateTime'),
            ('id', 'Prescription ID'),
        )    
