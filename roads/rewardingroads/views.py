from django.shortcuts import render
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from django.shortcuts import HttpResponse
from rewardingroads.forms import *
from rewardingroads.decorators import *
from django.views.decorators.csrf import csrf_exempt
import json

@user_session_set
def index(request):
	user = Traveller.objects.get(name=request.session['username'])
	total_reports = Report.objects.filter(reporter=user)
	verified_reports = Report.objects.filter(reporter=user).filter(processed=1)
	context = {
		'user' : user,
		'total_reports' : total_reports,
		'verified_reports' : verified_reports
	}
	return render(request,'rewardingroads/home.html',context)

@user_session_set
def drive(request):
	user = Traveller.objects.get(name=request.session['username'])
	roads = Road.objects.all()
	checked = Information.objects.filter(trust__lte=0.80)
	complete = []
	for info in checked:
		temp = [float(info.latitude),float(info.longitude)]
		complete.append(temp)
	final = json.dumps(complete)
	context = {
		'user' : user,
		'roads' : roads,
		'toBeChecked' : final
	}
	return render(request,'rewardingroads/drive.html',context)

def login(request):
	request.session.pop('username',None)
	if request.method == "POST":
		print(request.POST)
		username = request.POST.get('name','nikhil96sher')
		request.session['username'] = username
		return HttpResponseRedirect('/roads/')
	return render(request,'rewardingroads/login.html')

@csrf_exempt
def report(request):
	try:
		data = json.loads(request.body)
		rows = data['myrows']
		road = Road.objects.get(pk = int(data['road']))
		user = Traveller.objects.get(name = request.session['username'])
		for report in rows:
			latitude = float(report['Latitude'])
			longitude = float(report['Longitude'])
			reporttype = report['Type']
			time = report['Incident Time']
			d = Report()
			d.reporting_time = time
			d.reporter = user
			d.latitude = latitude
			d.longitude = longitude
			d.road = road
			delta = 0.001
			lat = round(latitude,4)
			lon = round(longitude,4)
			infos = Information.objects.filter(latitude__lte=lat+delta, latitude__gte=lat-delta).filter(longitude__lte=lon+delta, longitude__gte=lon-delta)
			if(infos.count() != 0):
				info = infos[0]
				info.last_report_time = d.reporting_time
				info.trust = ((info.report_count * info.trust) + (user.trust))/(info.report_count+1)
				info.report_count += 1
				info.save()
			else:
				info = Information()
				info.latitude = lat
				info.longitude = lon
				info.trust = user.trust
				info.road = road
				info.last_report_time = d.reporting_time
				info.save()
			d.information = info
			d.save()
		return HttpResponse("success")
	except Exception as e:
		print(e)
		return HttpResponse("error")