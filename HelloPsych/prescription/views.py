from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from prescription.models import prescription, brand, dosage, generic
from prescription.forms import PrescriptionForm
from login.models import patient, doctor
from django.core.mail import EmailMultiAlternatives 
from django.core.exceptions import ObjectDoesNotExist
from prescription.utils import generate_pdf
from docview.models import request_call
from django.template import RequestContext, Context
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.conf import settings

@csrf_protect
@login_required
def prescribe(request, req_id=1, med_count=1):
    '''
         Prescription Form to be filled/updated by the Doctor
    '''
    try:
        doct = doctor.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponse(" <h1> You are not authorized to \
            view this page. </h1>")
    if not request_call.objects.filter(id=req_id, \
        doc=doct).exists():
        return HttpResponse(" <h1> Error: </h1> <ul> <li> No appointment of \
                the Request Call ID provided was found </li><br /><li>\
                Or you are not authorized to send this prescription. </li> </ul>")
    else:
        med_count = int(med_count)
        r=request_call.objects.get(id=req_id)
        form = PrescriptionForm(request.POST or None, count=med_count, initial = {'doctor_comments': r.doctor_comments})
        if form.is_valid():
            temp_list = request.POST.getlist('concern')
            concern_list = []
            for concerns in temp_list:
                concern_list.append(str(concerns))
            apt = request_call.objects.get(id=req_id)
            if prescription.objects.filter(appointment=apt).exists():
                presc = prescription.objects.filter(
                    appointment=apt,
                ).update(
                    symptoms=form.cleaned_data['symptoms'],
                    doctor_comments=form.cleaned_data['doctor_comments'],
                    concern=concern_list,
                )
                presc = prescription.objects.get(appointment=apt)
                for obj in presc.medicines.all():
                    presc.medicines.remove(obj)
                    dosage.objects.filter(id=obj.id).delete()
                dosage_list = [] 
                for i in range(med_count):
                    med = generic.objects.get(name=form.cleaned_data['dosage_%s'% i])
                    dosobj = dosage.objects.create(generic=med, \
                        frequency=form.cleaned_data['freq_%s'% i],
                        comment=form.cleaned_data['comment_%s' % i], 
                        duration=form.cleaned_data['duration_%s' % i],
                    )
                    dosage_list.append(dosobj)
                presc.medicines.add(*dosage_list) 
                #Adding all the prescription objects together instead of adding them seperately.s 
                presc.save()
                pat_email = getattr(User.objects.get(\
                       username=apt.patient.username), 'email')
                subject = 'Your Prescription has been modified!'
                ctx = {
                    'first_name': apt.patient.first_name,
                    'last_name': apt.patient.last_name,
                    'doc_firstname': doct.first_name,
                    'doc_lastname': doct.last_name,
                    'prescrid': presc.id,
                    'Hostname': settings.HOSTNAME,
                }
                message2 = get_template(\
                       'prescription/presc_email_modify.txt'\
                    ).render(Context(ctx))
                message = get_template(\
                       'prescription/presc_email_modify.html'\
                    ).render(Context(ctx))
                email = EmailMultiAlternatives(subject, message2, \
                       settings.EMAIL_HOST_USER, [pat_email])
                email.attach_alternative(message, "text/html")
                email.send(fail_silently=False)
                return HttpResponseRedirect(reverse('docview:dashboard', \
                       args=(str(request.user.username),)))
            else:
                request_call.objects.filter(id=req_id).update(\
                    prescription_sent=True)
                apt = request_call.objects.get(id=req_id)
                doct = doctor.objects.get(user=apt.doc.user)
                doct.credits += doct.consultation_fee
                doct.save()
                presc = prescription.objects.create(
                    symptoms=form.cleaned_data['symptoms'],
                    doctor_comments=form.cleaned_data['doctor_comments'],
                    doc=doct,
                    patient=apt.patient,
                    appointment=apt,
                    concern=concern_list,
                )
                presc.save();
                dosage_list = []
                for i in range(med_count):
                    med = generic.objects.get(name=form.cleaned_data['dosage_%s'% i])
                    dosobj = dosage(generic=med, \
                        frequency=form.cleaned_data['freq_%s'% i], 
                        comment=form.cleaned_data['comment_%s'% i],
                        duration=form.cleaned_data['duration_%s' % i]
                    )
                    dosobj.save()
                    dosage_list.append(dosobj)
                presc.medicines.add(*dosage_list)
                pat_email = getattr(User.objects.get(\
                    username=apt.patient.username), 'email')
                subject = 'Your Prescription is ready!'
                ctx = {
                    'first_name': apt.patient.first_name,
                    'last_name': apt.patient.last_name,
                    'doc_firstname': doct.first_name,
                    'doc_lastname': doct.last_name,
                    'prescrid': presc.id,
                    'Hostname': settings.HOSTNAME,
                }
                message = get_template('prescription/presc_email_done.html'\
                    ).render(Context(ctx))
                message2 = get_template('prescription/presc_email_done.txt'\
                    ).render(Context(ctx))
                email = EmailMultiAlternatives(subject, message2, \
                    settings.EMAIL_HOST_USER, [pat_email])
                email.attach_alternative(message, "text/html")
                email.send(fail_silently=True)
                presc.save()
                return HttpResponseRedirect(reverse('docview:dashboard', args=(str(request.user.username),)))
    count2 = med_count-1 if med_count>1 else 0
    variables = RequestContext(request, {'form':form, \
        'count': med_count+1, \
        'count2': count2, \
        'usrname': doct.username, \
        'flag': request.user.is_authenticated(), \
        'imdoc': 'True',})
    return render_to_response('prescription/prescribe.html', variables,)

@csrf_protect
@login_required
def prescriptions(request, prescription_id=1):
    '''
        Viewing the Prescription as given by the Doctor
        Note: Can be viewed only by Doctor who prescribed it and by the Patient who it is prescribed to.
    '''
    resp = HttpResponse(content_type='application/pdf')
    title = "Prescription " + str(prescription_id)
    try:
        pat = patient.objects.get(user=request.user)
        flag = 1
    except patient.DoesNotExist:
        try:
            flag = 2
            doct = doctor.objects.get(user=request.user)
        except doctor.DoesNotExist:
            return HttpResponse(" <h1> You are not authorized to \
             view this page. </h1>")
    concerns_list = []
    if flag == 2:
        if not prescription.objects.filter(id=prescription_id, \
        doc=doct).exists():
            return HttpResponse(" <h1> Error: </h1> <ul> <li> \
                No prescription of the provided Prescription ID provided \
                was found </li> <br /><li>Or you are \
                not authorized to view this prescription. </li>")
        else:
            presc = prescription.objects.get(id=prescription_id, doc=doct)
            temp_list = presc.concern.encode('utf8')
            temp_list = temp_list.split(',')
            length = len(temp_list)
            for i in range(0, length):
                temp_list[i] = temp_list[i][1:]
            temp_list[length-1] = temp_list[length-1][:-1]
            for concern in temp_list:
                concern = concern[1:]
                concern = concern[:-1]
                concerns_list.append(concern)
            result = generate_pdf('prescription/prescription.html', context={\
                'presc': presc, 'concern_list': concerns_list, \
                'title': title}, file_object=resp)
            return result
    else:
        if not prescription.objects.filter(id=prescription_id, \
        patient=pat).exists():
            return HttpResponse(" <h1> Error: </h1> <ul> <li> You are not \
                authorized to view this prescription. </li> \
                <li>  Or the Prescription made for you is being generated.\
                Please try again later to view your prescription.</li>")
        else:
            presc = prescription.objects.get(id=prescription_id, patient=pat)
            temp_list = presc.concern.encode('utf8')
            temp_list = temp_list.split(',')
            length = len(temp_list)
            for i in range(0, length):
                temp_list[i] = temp_list[i][1:]
            temp_list[length-1] = temp_list[length-1][:-1]
            for concern in temp_list:
                concern = concern[1:]
                concern = concern[:-1]
                concerns_list.append(concern)
                result = generate_pdf('prescription/prescription.html', \
                    context={'presc': presc, 'concern_list': concerns_list, \
                    'title': title}, file_object=resp)
            return result
