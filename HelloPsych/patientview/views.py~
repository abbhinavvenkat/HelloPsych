from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from login.models import *
from login.views import *
from patientview.models import *
from docview.models import *
from prescription.models import prescription
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from itertools import chain
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_control, never_cache
from prescription.utils import generate_pdf
import stripe, re, urllib2, urllib, datetime

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('patient:index'))
    else:
        if request.method=='POST':
            request.session['sex']=request.POST['sex']
            request.session['age']=request.POST['age']
            request.session['marital']=request.POST['marital']
            request.session['cond']=request.POST['selected_image']
            return HttpResponseRedirect(reverse('patient:index_init'))
        else:
            return render_to_response('patientview/home.html',
                RequestContext(request,{'user':request.user, 'range':range(18,71)}))

@login_required
def index(request):

        patient_profile = patient.objects.filter(user=request.user)
        doctor_profile = doctor.objects.filter(user=request.user)
        request.session['reschedule']=0
        if request.method == 'POST':
                request.session['concern']=request.POST['concern']
                if request.POST['concern']=="all":
                        doc=doctor.objects.all()
                else:
                        special=specializations.objects.filter(expertise=request.POST['concern'])
                        doc=[]
                        for i in special:
                                doc.append(i.doc)
        else:
                doc=doctor.objects.all()

        if not profileupdate.objects.filter(user=request.user.id).exists() and not doctor.objects.filter(user=request.user.id).exists():
                return HttpResponseRedirect(reverse('login:profile'))
        if doctor.objects.filter(user=request.user.id).exists():
                return HttpResponseRedirect(reverse('docview:dashboard',args=(str(request.user.username),)))

        docs=[]
        pat=patient.objects.get(user=request.user.id)
        bFlag=False
        for i in doc:
                req_exists=False
                try:
                        req=request_call.objects.filter(doc=i,patient=pat,acknowledged=False)
                        req_exists=True if len(req)>0 else False
                        br=broadcast.objects.filter(patient=pat,acknowledged=False)
                        bFlag=False
                        if br:
                                bFlag=True
                except:
                        pass#print "light"

                if req_exists:
                        i.rflag=True
                else:
                        i.rflag=False

                docs.append(i)

        edit_profile_flag=False
        if request.user.is_authenticated():
                if patient.objects.filter(user=request.user).exists():
                        edit_profile_flag=True
                else:
                        edit_profile_flag=False
        else:
                edit_profile_flag=False

        iconflag=True
        first=pat.first_call
        appoint=[]
        appointments=[]
        pat = patient.objects.get(user=request.user)
        appoint=request_call.objects.filter(patient=pat)
        for i in appoint:
                if i.prescription_sent==False:
                        appointments.append(i)
        
        if request.method == 'GET':
            if 'cancel' in request.GET:
                delAppoint = request_call.objects.get(id=request.GET['appointID'])
                delAppoint.delete()
                return HttpResponseRedirect(reverse('patient:index'))   

            if 'reschedule' in request.GET:
                request.session['reschedule']=1
                request.session['appointID']=request.GET['appointID']
                docID=request.GET['docID']
                url = "/cal/" + str(docID) + "/"
                return HttpResponseRedirect(url)

        return render_to_response('patientview/index.html', 
                RequestContext(request, {'iconflag':iconflag, 'edprofFlag':edit_profile_flag, 
                'pat':pat, 'usrname':request.user.username, 'user':request.user, 'docs':docs, 
                'flag':request.user.is_authenticated(), 'bflag':bFlag, 'first':first, 
                'appointments':appointments}))

def index_init(request):
        special=specializations.objects.filter(expertise=request.session['cond'])
        doc=doctor.objects.filter(expertise=request.session['cond'])
        docs=[]

        for i in special:
                docs.append(i.doc)

        return render_to_response('patientview/index_init.html',RequestContext(request,{'user':request.user,'usrname':request.user.username,'docs':docs,'flag':request.user.is_authenticated()}))


def index_search(request):
        query=request.POST['q'].split(' ')
        docs=list()
        for i in query:
                fname=User.objects.filter(first_name__icontains=i)
                lname=User.objects.filter(last_name__icontains=i)
                uname=doctor.objects.filter(username__icontains=i)
                desc=doctor.objects.filter(description__icontains=i)
                add=doctor.objects.filter(address__icontains=i)
                loc=doctor.objects.filter(location__icontains=i)
                ugd=doctor.objects.filter(ug_degree__icontains=i)
                ugcol=doctor.objects.filter(ug_college__icontains=i)
                ugcou=doctor.objects.filter(ug_council__icontains=i)
                ugreg=doctor.objects.filter(ug_regno__icontains=i)
                pgd=doctor.objects.filter(pg_degree__icontains=i)
                pgcol=doctor.objects.filter(pg_college__icontains=i)
                pgcou=doctor.objects.filter(pg_council__icontains=i)
                pgreg=doctor.objects.filter(pg_regno__icontains=i)
                oth=doctor.objects.filter(others__icontains=i)
                cur=doctor.objects.filter(current_job__icontains=i)
                proj=doctor.objects.filter(projects__icontains=i)
                prev=doctor.objects.filter(prev_exp__icontains=i)
                mem=doctor.objects.filter(memberships__icontains=i)
                special=specializations.objects.filter(expertise__icontains=i)
                if i.lower() == 'others':
                        i='anon'
                if i.lower() == 'hallucination':
                        i='halu'
                if i.lower() == 'education':
                        i='edu'
                if i.lower() == 'phobias':
                        i='fear'

                special=specializations.objects.filter(expertise__icontains=i)
                ail=[]
                for i in special:
                        ail.append(i.doc)
                doc=list(chain(uname,fname,lname,desc,add,loc,ail,ugd,ugcol,ugcou,ugreg,pgd,pgcol,pgcou,pgreg,oth,mem,proj,prev,cur))
                if len(docs) == 0:
                        docs=doc
                else:
                        docs=list(set(docs) & set(doc))

        docs=f7(docs)

        if request.user.is_authenticated() and patient.objects.filter(user=request.user).exists():
                pat=patient.objects.get(user=request.user)
                for i in docs:
                        req_exists=False
                        try:

                                req=request_call.objects.filter(doc=i,patient=pat,acknowledged=False)
                                req_exists=True if len(req)>0 else False
                        except:
                                pass#print "light"

                        if req_exists:
                                i.rflag=True
                        else:
                                i.rflag=False
        if request.user.is_authenticated():
                if doctor.objects.filter(user=request.user).exists():
                        imdoc=True
                else:
                        imdoc=False
        else:
                imdoc=False



        return render_to_response('patientview/index_init.html',RequestContext(request,{'imdoc':imdoc,'usrname':request.user.username,'user':request.user,'docs':docs,'flag':request.user.is_authenticated()}))

def notify(request):
    if not request.is_ajax():
        return  HttpResponse (" Not an AJAX request ")
    if request.method == 'GET':
        us=request.user.id
        pat=patient.objects.get(user=us)
        req1=request_call.objects.filter(patient=pat.id,acknowledged=False)
        ans=""
        for j in req1:
                ans+='call requested with ' + j.doc.username + ' on ' + str(j.date_booked) + ' from ' + str(j.start_tim) + ' to ' + str(j.end_tim) + '. Please Be online at that time$'

        return HttpResponse(ans)

def director(request):
        if request.method == 'POST':
         request.session['sex']=request.POST['sex']
         request.session['age']=request.POST['age']
         request.session['marital']=request.POST['marital']
         request.session['cond']=request.POST['data-value']
        return HttpResponseRedirect(reverse('patient:index_init'))#'../../index')


def fix(request, did):

        doct=doctor.objects.get(id=did)
        pat=patient.objects.get(username=request.user)
        if pat.credits < (doct.consultation_fee + 1):
                return HttpResponseRedirect(reverse('patient:buy'))
        else:
                pat.credits-=1
                pat.save()

       # msg='Dear Doctor, '+pat.username +' has requested your online consultation on' + request.GET['db'] + ' . Please connect with the patient at ' + request.GET['st']
       # url="http://api.mVaayoo.com/mvaayooapi/MessageCompose"
       # values={'user':'hemanth@imaginate.in:imaginate',
        #        'senderID':'DOCTOR',
         #       'receipientno':doct.phone_no,
         #       'dcs':'0',
          #      'msgtxt':msg,
           #     'state':'4'}

      #  data = urllib.urlencode(values)
       # req = urllib2.Request(url, data)
        #serialized_data = urllib2.urlopen(req).read()


        if request.session['reschedule']==1:
            request.session['reschedule']=0
            pat.credits+=1
            pat.save()
            pat1=User.objects.get(username=request.user)
            doct1=User.objects.get(username=doct)
            req1=reschedule_request(id=request.session['appointID'],request_from=pat1,requested_to=doct1,date_booked=request.GET['db'],end_tim=request.GET['et'],start_tim=request.GET['st'])
            req1.save()

        else:
            req=request_call(patient=pat,doc=doct,date_booked=request.GET['db'],end_tim=request.GET['et'],start_tim=request.GET['st'],sent=True)
            req.save()
	    #==============SMS Notification ==== Donot uncomment ==== SMS are chargeble ===============================================================================================================================================================
           
        #    url = "http://api.mvaayoo.com/mvaayooapi/MessageCompose?user=hemanth@imaginate.in:imaginate&senderID=DOCTOR&receipientno=8897346807&dcs=0&msgtxt=HelloPsych%20Appt!%20with%20Test1Doc1%20on%2024/11/14%20at%2009:00&state=4"
        #   req = urllib2.Request(url)
        #    serialized_data = urllib2.urlopen(req).read()


        if not pat.first_call:
                pat.first_call=True
                pat.save()

        return HttpResponseRedirect(request.GET['next'])

@csrf_protect
def help(request):
    if request.method == 'POST':
        request.session['sex']=request.POST['sex']
        request.session['age']=request.POST['age']
        request.session['marital']=request.POST['marital']
        return HttpResponseRedirect(reverse('patient:issue'))
    else:
        return render_to_response('patientview/help.html',RequestContext(request,{'user':request.user,'range':range(18,71),'flag':request.user.is_authenticated()}))

@csrf_protect
def issue(request):
    if request.method == 'POST':
        request.session['issue']=request.POST['issue']
        return HttpResponseRedirect(reverse('patient:index'))
    else:
        return render_to_response('patientview/issue.html',RequestContext(request,{'user':request.user,'flag':request.user.is_authenticated()}))



def get(request):
    if not request.is_ajax():
        return  HttpResponse (" Not an AJAX request ")
    if request.method == 'GET':
        us=request.user.id
        pat=patient.objects.get(user=us)
        req=request_call.objects.filter(patient=pat.id)
        ans=""
        for i in req:
                if i.sent==True and i.acknowledged==False:
                        requ=request_call.objects.get(id=i.id)
                        requ.callpending=True
                        requ.save()

                elif i.sent==True and i.acknowledged==True and i.callinprogress==True and i.calldone==False:
                        requ=request_call.objects.get(id=i.id)
                        requ.callpending=False
                        requ.save()
                        ans+=str(i.doc.first_name)+':'+str(i.doc.last_name) + ':' + str(i.id) + ','

                elif i.sent==True and i.acknowledged==True and i.callinprogress==False:
                        requ=request_call.objects.get(id=i.id)
                        requ.calldone=True
                        requ.save()

        return HttpResponse(ans)
    return HttpResponse('ACTIVatr')

def iget(request):
    if not request.is_ajax():
        return  HttpResponse (" Not an AJAX request ")
    if request.method == 'GET':
        us=request.user.id
        pat=patient.objects.get(user=us)
        ans=""
        try:
                req=broadcast.objects.get(patient=pat.id,taken=False,acknowledged=True)
                req.Taken=True
                req.save()
                ans+=str(req.doc.first_name)+':'+str(req.doc.last_name) + ':' + str(req.id)
        except:
                pass#print 'light'

        return HttpResponse(ans)

    return HttpResponse('ACTIVatr')


def iFix(request):
    pat=patient.objects.get(username=request.user)
    req = broadcast(patient=pat,taken=False, acknowledged=False, ailment=request.session['concern'])
    req.save()
    return HttpResponseRedirect(request.GET['next'])

def payment(token, amnt):
    req=urllib2.Request("http://openexchangerates.org/api/latest.json?app_id=83db09f8d9c14105a7573467dfe5164c")
    data=urllib2.urlopen(req).read()
    a=re.search(r'"INR":.*,\n',data)
    b=float(a.group(0).split(':')[1].split(',')[0])
    chg=int(amnt*100/b)
    #print chg
    stripe.api_key = "sk_test_2BExwDOqp9iizCQGvU8SnoWJ"
    try:
        charge = stripe.Charge.create(
             amount=chg, 
             currency="usd",
             card=token,
             description="payinguser@example.com"
        )
    except stripe.CardError as e:
        return HttpResponse("Invalid Card Credentials. Payment Unsuccesful. please go back and try again")
    
cost={}
cost['10']=500
cost['20']=1000
#1 Credit = Re. 50/-

@login_required
def buy(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are not authorized to view this page. You must be logged in to view this page.")
    pat=patient.objects.get(user=request.user)
    if 'stripeToken' in request.POST:
        amount=request.POST['amnt']
        payment(request.POST['stripeToken'], cost[amount])
        pat.credits+=int(amount)
        pat.save()
        return render_to_response('patientview/payment.html', RequestContext(request,{\
            'msg':'Your payment of Rs.' + str(cost[amount]) + '  was succesful',\
            'credits':pat.credits, 'flag':request.user.is_authenticated()}))
    else:
        return render_to_response('patientview/payment.html', \
            RequestContext(request, {'credits':pat.credits, \
            'flag':request.user.is_authenticated()}))

def history(request):
    try:
        pat = patient.objects.get(user=request.user)
    except patient.DoesNotExist:
        return HttpResponse("You are not authorised to see this page.")
    from prescription.models import prescription
    from prescription.forms import PrescriptionFilter2
    filtered_list = PrescriptionFilter2(request.GET, \
        queryset=prescription.objects.filter(patient=pat))
    return render_to_response('patientview/history.html', 
        RequestContext(request, { 'filter': filtered_list, \
            'usrname':request.user.username, 'user':request.user, \
            'flag':request.user.is_authenticated(), 'imdoc':False}))

