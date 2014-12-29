from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from docview.models import *
from login.models import *
from patientview.models import *
from prescription.models import *
import vline

apo_req_id = 0

@login_required
def home(request,reciever,req_id):
    #calendar = get_object_or_404(Calendar, slug=calendar_slug)
    r=request_call.objects.get(id=req_id)
    pat=r.patient
    apo_req_id=req_id
    credits=pat.credits
    request.session['credits']=credits
    request.session['id']=req_id
    if request.user.is_authenticated():
	if reciever=="doctor":
        	users = vline.create_user_profile(User.objects.get(id=r.doc.user.id))
		imdoc=False
		request.session['imdoc']=False
	else:
		r=request_call.objects.get(id=req_id)
        	users = vline.create_user_profile(User.objects.get(id=r.patient.user.id))
		imdoc=True
		request.session['imdoc']=True

		if r.acknowledged == False:
		    r.acknowledged=True
		    r.callinprogress=True
		    r.callpending=False
                    p = patient.objects.get(user=r.patient.user)
                    d = doctor.objects.get(user=r.doc.user)
                    request.session['credits']=p.credits-d.consultation_fee
                    p.credits -= d.consultation_fee                    
                    p.save()
		    r.save()
    else:
        users = None


    doct=r.doc
    prescription_pending = request_call.objects.filter(id=req_id, doc=doct, acknowledged=True, sent=True, calldone=True, callinprogress=False, prescription_sent=False)
    presc_pending = []
    for i in prescription_pending:
        presc_pending.append(i)

    
    appoint=[]
    appointments=[]
    appoint=request_call.objects.filter(id=req_id, patient=pat, doc=doct)
    for i in appoint:
        if i.prescription_sent==False:
            appointments.append(i)
    
    roger=False
    if request.method == 'GET':
        roger=True
        if 'reschedule' in request.GET:
            delAppoint = request_call.objects.get(id=request.GET['appointID'])
            delAppoint.delete()
            docID=request.GET['docID']
            url = "/cal/" + str(docID) + "/"
            return HttpResponseRedirect(url)

        if 'sentpres' in request.GET:
            r.callinprogress = False
            r.calldone = True
            r.save()
            url =  "/presc/prescribe/" + str(req_id) + "/1/"
            return HttpResponseRedirect(url)   

    return render_to_response("vline/home.html", {
        "users": users,'flag':request.user.is_authenticated(),'req_id': req_id, 'prescription_pending':prescription_pending,'pending': presc_pending,'roger':roger,'pat':pat,'doct':doct,'appointments':appointments,'imdoc':imdoc,
    }, context_instance=RequestContext(request))


def update_comments(request):
    req_id = request.GET['req_id']
    textis = request.GET['textis']
    r=request_call.objects.get(id=req_id)
    r.doctor_comments=textis
    r.save() 
    return HttpResponse(r.doctor_comments)


def update_credits(request):
	if request.session['imdoc']==True:
		request.session['credits']-=1
		r=request_call.objects.get(id=int(request.session['id']))
		r.credits=request.session['credits']
		r.save()
	
	if request.session['credits']<=1:
		return HttpResponse('done')
	else:
		return HttpResponse('cool')
	return HttpResponse('somethings fishy')

@login_required
def broad(request,reciever,req_id):
    #calendar = get_object_or_404(Calendar, slug=calendar_slug)
    r=broadcast.objects.get(id=req_id)
    if request.user.is_authenticated():
	if reciever=="patient":
#		r=broadcast.objects.get(id=req_id)
		
        	users = vline.create_user_profile(User.objects.get(id=r.patient.user.id))
		imdoc=True		
		r.acknowledged=True
		r.doc=doctor.objects.get(user=request.user)
		r.save()
	else:
        	users = vline.create_user_profile(User.objects.get(id=r.doc.user.id))
		r.taken=True
		r.save()
		imdoc=False

    else:
        users = None
    print users
    return render_to_response("vline/home.html", {
        "users": users,'flag':request.user.is_authenticated(),'imdoc':imdoc
    }, context_instance=RequestContext(request))
