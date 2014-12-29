from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from login.models import patient, doctor
from docview.models import request_call, \
    specializations, timeslot, reschedule_request
from django.contrib.auth.decorators import login_required
from docview.forms import DocProfileForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from prescription.models import prescription
import re

def convert(time):
    '''
         Appointment Reschedule Logic
    '''
    temp = time
    searchM = re.search( r':\d+', temp)
    x = temp.split(" ")
    if searchM is None:
        hours = x[0]
        mins = "00"
        ampm = x[1]
    else:        
        searchH = re.search( r'\d+', temp)
        hours = searchH.group()
        mins = searchM.group()
        mins = mins[1:3]
        ampm = re.search( r'\w\.\w\.', temp)
        ampm = ampm.group()
    hours = int(hours)
    mins = int(mins)
    if ampm == "p.m.":
        if hours < 12:
            hours = hours + 12
    if ampm == "a.m.":
        if hours == 12:
            hours = hours - 12
    Shour = str(hours)
    Smin = str(mins)
    if hours < 10:
        Shour = "0" + Shour
    if mins < 10: 
        Smin = "0" + Smin
    final_time = Shour + ':' + Smin    
    return final_time

@login_required
def dashboard(request, doc):
    '''
        Doctor Dashboard
    '''
    if doc == request.user.username:
        doct = doctor.objects.get(username=doc)
        calls_not_done = request_call.objects.filter(\
            doc=doct, callpending=True, sent=True)
        call_not_done = []
        calls_not_returned=request_call.objects.filter(doc=doct, \
            acknowledged=False, sent=True, callpending=True)
        for appointment in calls_not_done:
            call_not_done.append(appointment)
        prescription_pending = request_call.objects.filter(\
            doc=doct, acknowledged=True, sent=True, \
            calldone=True, callinprogress=False, \
        prescription_sent=False)
        presc_pending = []
        for i in prescription_pending:
            presc_pending.append(i)
        #reschedule logic
        schedule_request=reschedule_request.objects.filter(requested_to=request.user)
        date_b='a'  
        req_date='a'
        date_b_d='a'
        date_b_m='m'
        date_b_y='m'
        st_time = 'm'
        en_time = 'm'
        if request.method == 'GET':
            if 'accept' in request.GET:
                reqPatient = patient.objects.get(username=request.GET['requestFrom'])
                reqDoc = doctor.objects.get(username=request.GET['requestedTo'])
                reqDate = request.GET['requestDate']
                reqStartTime = request.GET['requestStartTime']
                reqEndTime = request.GET['requestEndTime']
                if request_call.objects.filter(id=request.GET['requestID']).exists():
                    request_call.objects.get(id=request.GET['requestID']).delete()
                date_b = str(reqDate)
                date_b_m = date_b[0:3]
                date_b_d = date_b[5:7]
                date_b_y = date_b[9:13]
                convert_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03',\
                          'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', \
                          'Aug':'08', 'Sep':'09', 'Oct': '10', 'Nov':'11', \
                          'Dec': '12'}
                date_b_m = convert_dict[date_b_m]
                req_date = date_b_y + '-' + date_b_m + '-' + date_b_d
                st_time = str(reqStartTime)
                st_time = convert(st_time)
                en_time = str(reqEndTime)
                en_time = convert(en_time)
                call=request_call(id=request.GET['requestID'], \
                     patient=reqPatient, doc=reqDoc, date_booked=req_date, \
                     start_tim=st_time, end_tim=en_time, sent=True)
                call.save()
                reschedule_request.objects.filter(id=request.GET['requestID']).delete()
                variables = RequestContext(request, {'flag':request.user.is_authenticated(), 'doc':doct, 'urgents':call_not_done,'left_calls':calls_not_returned,'lname': doct.last_name,'pending': presc_pending,'imdoc':'True','schedule_request':schedule_request,'usrname': doct.username, 'fname': doct.first_name, 'user': request.user,'date_b':date_b,'req_date':req_date,'date_b_d':date_b_d, 'st_time':st_time,'en_time':en_time})
                return render_to_response('docview/dash.html', variables)
            elif 'reject' in request.GET:
                reschedule_request.objects.filter(id=request.GET['requestID']).delete()
                return render_to_response('docview/dash.html',RequestContext(request, {'flag':request.user.is_authenticated(), 'doc':doct, 'urgents':call_not_done,'lname': doct.last_name,'left_calls':calls_not_returned,'pending': presc_pending,'imdoc':'True','schedule_request':schedule_request,'usrname': doct.username, 'fname': doct.first_name, 'user': request.user,'date_b':date_b,'req_date':req_date,'date_b_d':date_b_d, 'st_time':st_time,'en_time':en_time}))

            #end reschedule logic.
        return render_to_response('docview/dash.html', \
            RequestContext(request, {'doc':doct, 'urgents':call_not_done, \
            'pending': presc_pending, 'user': request.user, \
            'usrname': doct.username, 'fname': doct.first_name, \
            'lname': doct.last_name, 'left_calls':calls_not_returned, \
            'pic': doct.propic, \
            'flag': request.user.is_authenticated(), \
            'imdoc':'True','schedule_request':schedule_request, \
            'date_b':date_b,'req_date':req_date,'date_b_d':date_b_d,'st_time':st_time,'en_time':en_time}))
    else:
        return HttpResponse(" You are not authorised to see this page :)")

def get(request):
    if not request.is_ajax():
        return  HttpResponse(" Not an AJAX request ")
    if request.method == 'GET':
        doct = doctor.objects.get(user=request.user.id)
        req = request_call.objects.filter(doc=doct.id)
        ans = ""
        for i in req:
            if i.sent is False:
                requ = request_call.objects.get(id=i.id)
                requ.sent = True
                requ.save()
                ans += str(i.patient.first_name) + '&' + \
                 str(i.patient.last_name) + '&' + str(i.id) + \
                 '&' + str(i.start_tim) + ','
        special = specializations.objects.filter(doc=doct)
        ans += "|"
        exp = []
        for i in special:
            exp.append(i.expertise)
        return HttpResponse(ans)
    return HttpResponse('ACTIVatr')

@csrf_protect
@login_required
def specialization(request):
    '''
        Edit Specializations of Doctor
    '''
    doct = doctor.objects.get(user=request.user)
    exclude_list = [elem.expertise for elem in \
    specializations.objects.filter(doc=doct)]
    from django.conf import settings
    specialization_list = settings.SPECIALIZATION_LIST
    specs = [i for i in specialization_list if i not in exclude_list]
    if request.method == 'POST':
        if 'add' in request.POST and request.POST.get('expertise') is not None:
            if not specializations.objects.filter(doc=doct, \
                expertise=request.POST.get('expertise')).exists():
                sobj = specializations.objects.create(
                        doc=doct,
                        expertise=request.POST.get('expertise', False)
                        )
                sobj.save()
                specs = [i for i in specs if i not in request.POST['expertise']]
                specs.sort()
        elif 'del' in request.POST:
            for i in request.POST.getlist('specs'):
                specializations.objects.filter(doc=doct, expertise=i).delete()
                if i not in specs:
                    specs.append(i)
                specs.sort()
    existing = specializations.objects.filter(doc=doct)
    variables = RequestContext(request, \
        {'flag':request.user.is_authenticated(), 'docid':doct.id, \
        'usrname':doct.username, 'existing':existing, \
        'specs':specs, 'imdoc':'True'}
    )
    return render_to_response('docview/expertise.html', variables,)

@csrf_protect
def profile(request, doc):
    '''
        Profile Page of Doctor as viewable by 
        patients / unregistered users.
    '''
    if not doctor.objects.filter(username=doc).exists():
        return HttpResponse("We have no doctor with that username . Please check again")
    doct=doctor.objects.get(username=doc)
    receiver = User.objects.get(username=doc)
    slots=timeslot.objects.filter(doc=doct,enabled=True)
    special=specializations.objects.filter(doc=doct)
    req_exists=False

    try:
        pat = patient.objects.get(user=request.user)
        req = request_call.objects.filter(doc=doct, \
            patient=pat, acknowledged=False)
        req_exists = True if len(req) > 0 else False
    except (patient.DoesNotExist, request_call.DoesNotExist):
        req_exists = False

    patient_exists = patient.objects.filter(\
        user=request.user.id).exists()
    if request.method == 'POST':
        subject = request.POST['subject']
        text_message = request.POST['message']
        sender = request.user
        from messageapp.models import message
        msg = message(sender=sender, \
            text_message=text_message, subject=subject, \
            receiver=receiver)
        msg.save()
    return render_to_response( 'docview/profile.html', RequestContext(request,\
            {'user':request.user, 'doct':doct, \
            'usrname':doct.username, 'flagp':patient_exists, \
            'flag':request.user.is_authenticated(), 'rflag':req_exists, \
            'imdoc':not patient_exists, 'slots':slots, 'special':special}))

def calendar(request, doc_id):
    '''
        Get the Calendar of the Doctor
        based on the Doctor Id provided.
    '''
    doct = doctor.objects.get(id=doc_id)
    timeslots = timeslot.objects.filter(doc=doct, enabled=True)
    slotdays = ""
    for i in timeslots:
        slotdays = slotdays + i.day + ", " 

    pat = patient.objects.get(user=request.user)
    req = request_call.objects.filter(doc=doct)
    return render_to_response('theme.html', {'slots':timeslots, \
        'req':req, 'flag':request.user.is_authenticated(), 'doc':doc_id,'slotdays':slotdays, \
        'pat':pat}, context_instance=RequestContext(request))

@csrf_protect
@login_required
def slot(request):
    '''
        Edit TimeSlots of the Doctor
    '''
    from docview.forms import SlotForm
    formslot = SlotForm(request.POST or None)
    doct=doctor.objects.get(user=request.user)
    if 'save' in request.POST:
        if formslot.is_valid():
            slotday = formslot.cleaned_data['day']
            start = formslot.cleaned_data['start_time']
            end = formslot.cleaned_data['end_time']
            flag = True
            if start > end:
                flag = False
            doct = doctor.objects.get(user=request.user)
            for tim in timeslot.objects.filter(doc=doct):
                if tim.day == slotday:
                    if tim.start_time == start and tim.end_time == end:
                        flag = False #Incase Same Query was passed again.
                        timeslot.objects.filter(\
                            doc=doct, \
                            day=slotday, start_time=start, \
                            end_time=end).update(enabled=True)
                    elif start > tim.start_time \
                        and tim.end_time > end: #In between
                        flag = False
                    elif tim.start_time < end and start < tim.start_time \
                        and end < tim.end_time:
                        flag = False
                    elif tim.start_time < start and tim.end_time > end:
                        flag = False
                    elif start < tim.start_time and start < tim.end_time \
                        and tim.end_time < end:
                        flag = False
            if flag:
                time = timeslot.objects.create(
                    doc=doct,
                    day=slotday,
                    start_time=start,
                    end_time=end,
                    enabled=True
                )
                time.save()
    elif 'save_slot' in request.POST:
        timeslots = timeslot.objects.filter(\
            doc=doctor.objects.get(user=request.user))
        for doc_slot in timeslots:
            if str(doc_slot.id) in request.POST:
                doc_slot.enabled = True
            else:
                doc_slot.enabled = False
            doc_slot.save()
        formslot = SlotForm(None)

    existing = timeslot.objects.filter(doc=doct)
    variables = RequestContext(request, {'form': formslot, \
        'usrname': doct.username, \
        'flag': request.user.is_authenticated(), 'existing': existing, \
        'imdoc': 'True'})
    return render_to_response('docview/slot.html', variables,)

@csrf_protect
@login_required
def profile_create(request):
    '''
        Profile Creation after taking basic user info.
        Also Doctor Object Creation.
    '''
    if request.method=='POST':
        fm = DocProfileForm(request.POST,request.FILES)
        if fm.is_valid():
            user_obj=User.objects.get(id=request.user.id)
            doc=doctor.objects.create(
                user=request.user,
                username=request.user.username,
                first_name=user_obj.first_name,
                last_name=user_obj.last_name,
                description=fm.cleaned_data['description'],
                current_job=fm.cleaned_data['current_job'],
                location=fm.cleaned_data['location'],
                address=fm.cleaned_data['address'],
                phone_no=fm.cleaned_data['phone_no'],
                prev_exp=fm.cleaned_data['prev_exp'],
                projects=fm.cleaned_data['projects'],
                memberships=fm.cleaned_data['memberships'],
                ug_degree=fm.cleaned_data['ug_degree'],
                ug_college=fm.cleaned_data['ug_college'],
                ug_council=fm.cleaned_data['ug_council'],
                ug_year=fm.cleaned_data['ug_year'],
                ug_regno=fm.cleaned_data['ug_regno'],
                pg_degree=fm.cleaned_data['pg_degree'],
                pg_college=fm.cleaned_data['pg_college'],
                pg_regno=fm.cleaned_data['pg_regno'],
                pg_council=fm.cleaned_data['pg_council'],
                pg_year=fm.cleaned_data['pg_year'],
                consultation_fee=fm.cleaned_data['consultation_fee'],
                others=fm.cleaned_data['others'],
            )
            doc.save()
            from login.models import UserProfile
            doc_verify=UserProfile.objects.get(user=request.user)
            if doc_verify.verified:
                return HttpResponseRedirect(reverse('docview:dashboard', \
                    args=(str(request.user.username),)))
            else:
                return HttpResponseRedirect(reverse('login:not_verified'))
    else:
        fm=DocProfileForm(None)
    variables = RequestContext(request, {'form': fm, \
        'flag':request.user.is_authenticated(), 'imdoc':'True', \
        'usrname':request.user.username})
    return render_to_response('registration/docprof.html', variables)

@csrf_protect
@login_required
def profile_update(request):
    '''
        Updation of Profile after the Doctor 
        Account is created.
    '''
    ins=doctor.objects.get(user=request.user)
    if request.method == 'POST':
        fm = DocProfileForm(request.POST, request.FILES)
        if fm.is_valid():
            ins.address=fm.cleaned_data['address']
            ins.phone_no=fm.cleaned_data['phone_no']
            ins.location=fm.cleaned_data['location']
            ins.others=fm.cleaned_data['others']
            ins.current_job=fm.cleaned_data['current_job']
            ins.projects=fm.cleaned_data['projects']
            ins.description=fm.cleaned_data['description']
            ins.prev_exp=fm.cleaned_data['prev_exp']
            ins.memberships=fm.cleaned_data['memberships']
            ins.ug_degree=fm.cleaned_data['ug_degree']
            ins.ug_council=fm.cleaned_data['ug_council']
            ins.ug_college=fm.cleaned_data['ug_college']
            ins.ug_year=fm.cleaned_data['ug_year']
            ins.ug_regno=fm.cleaned_data['ug_regno']
            ins.pg_degree=fm.cleaned_data['pg_degree']
            ins.pg_council=fm.cleaned_data['pg_council']
            ins.pg_college=fm.cleaned_data['pg_college']
            ins.pg_year=fm.cleaned_data['pg_year']
            ins.pg_regno=fm.cleaned_data['pg_regno']
            ins.consultation_fee=fm.cleaned_data['consultation_fee']
            ins.save()
            return HttpResponseRedirect(reverse('patient:index'))
    else:
        from django.forms.models import model_to_dict
        fm = DocProfileForm(data = model_to_dict(ins))

    variables = RequestContext(request, {'form': fm, \
        'flag':request.user.is_authenticated(), \
        'imdoc':'True','usrname':ins.username})
    return render_to_response('docview/edit.html',variables,)

@csrf_protect
@login_required
def history(request):
    '''
        Display The Appointment History of the Doctor
    '''
    try:
        doct = doctor.objects.get(user=request.user)
    except doctor.DoesNotExist:
        return HttpResponse("You are not authorised to see this page.")
    from prescription.models import prescription
    from prescription.forms import PrescriptionFilter
    filtered_list = PrescriptionFilter(request.GET, \
        queryset=prescription.objects.filter(doc=doct))
    return render_to_response('docview/history.html', \
        RequestContext(request, {'imdoc': 'True', \
            'flag':request.user.is_authenticated(), \
            'usrname': doct.username, \
            'filter': filtered_list}))

@login_required
def stat(request):
    '''
        Show statistics of the Doctor.
    '''
    import json
    try:
        doct = doctor.objects.get(user=request.user)
    except doctor.DoesNotExist:
        return HttpResponse("You are not authorised to see this page.")  
    apts = request_call.objects.filter(doc=doct)
    arr_count = {}
    for apt in apts.iterator():
        if apt.patient.username in arr_count:
            arr_count[str(apt.patient.username)] += 1
        else:
            arr_count[str(apt.patient.username)] = 1
    arr = [['Patient User Name', 'Appointment Frequency']]
    for arg, value in arr_count.items():
        arr.append([arg, value])
    gen_list = prescription.objects.filter(doc=doct)
    gen_count = {}
    for obj in gen_list:
        for dosobj in obj.medicines.iterator():
            print dosobj
            if dosobj.generic.name in gen_count:
                gen_count[dosobj.generic.name] +=1
            else:
                gen_count[dosobj.generic.name] =1 
    arr2 = [['Generic Name', 'Frequency Generic Prescribed']]
    for arg, value in gen_count.items():
        arr2.append([arg, value])

    return render_to_response('docview/stat.html', RequestContext(request, {
        'flag':request.user.is_authenticated(), 'imdoc':True, \
        'json_data': json.dumps(arr), 'json_data2': json.dumps(arr2), \
        'usrname':doct.username}))
