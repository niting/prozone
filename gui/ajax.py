from django.utils import simplejson
from django.db.models import Q
from gui.models import EventsPz
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from gui.core import *
from itertools import chain

"""Setting the field size to 580 by 390"""
@dajaxice_register
def update_players(request, option):
	"""Returns the players for both teams involved"""
	dajax = Dajax()
	if(option == '#'):
		dajax.add_data([], 'doNothing')
		return dajax.json()
	idx_v = option.find(" v ")	
	team1 = option[0:idx_v]
	team2 = option[idx_v+3:]

	out1 = EventsPz.objects.filter(fixture=option).exclude(player1name='NULL').values_list('player1name', flat=True).distinct()
	out2 = EventsPz.objects.filter(fixture=option).exclude(player2name='NULL').values_list('player2name', flat=True).distinct()

	out = list(out1) + list(out2)
	out = set(out)
	out_list = []
	out_list.append("<option value='#'>Select a Player</option>")
	for i in out:
		out_list.append("<option value='%s'>%s</option>" % (i,i))

	dajax.assign('#id_head_player', 'innerHTML', ''.join(out_list))
	dajax.assign('#id_tohead_player', 'innerHTML', ''.join(out_list))

	half1, half2 = find_half_time(EventsPz.objects.filter(fixture=option))
	total = int(half1+half2)/60 + 1
	#dajax.assign('#half_time_value', 'innerHTML', int(half1)/60)
	#dajax.assign('#full_time_value', 'innerHTML', total)
	dajax.script("$('#slider_range').slider( 'option' , { min: 0, max: %d } );" % total)
	dajax.script("$('#slider_range').slider( 'option',  'values', [0, %d]); " % total)
	dajax.script('$("#loader").hide()')
	dajax.script("$( '#time_range' ).val('0 mins - 90 + %d mins')" %(total-int(half1)/60-45));
	times = {'time1': int(half1)/60, 'time2': total-int(half1)/60}
	dajax.add_data(times, 'updateTimes')
	return dajax.json()

def decide_max_count(sz):
	"""Function that evaluates the COUNT/MAX ratio"""
	max_val = 100
	if(sz <= 1):
		count_val = 100
	elif(sz <= 2):
		count_val = 94
	elif(sz <= 5):
		count_val = 93 
	elif(sz <= 10):
		count_val = 90
	elif(sz <= 15): 
		count_val = 89
	elif(sz <=20):
		count_val = 85
	elif(sz <= 30):
		count_val = 85
	elif(sz <= 40):
		count_val = 80
	elif(sz <= 50):
		count_val = 72
	elif(sz <= 60):
		count_val = 65
	elif(sz <= 70):
		count_val = 58
	elif(sz <= 80):
		count_val = 52
	elif(sz <= 90):
		count_val = 48
	else:
		count_val = 43
	return (count_val,max_val)

def construct_gradient(sz):
	"""Contructs varying gradients depending on the number of sample 
	points"""
	colors = ["rgb(0,0,255)", "rgb(0,255,255)", "rgb(0,255,0)", 
					"yellow", "rgb(255,0,0)"]
	color_stops = [ [0.2 ,0.3 ,0.3],
					[0.4 ,0.45,0.5],
					[0.5 ,0.6 ,0.7],
					[0.6 ,0.8 ,0.9],
					[1 ,    1 ,1   ]]
	if(sz <= 5):
		idx = 0
	elif(sz <= 30):
		idx = 1
	else:
		idx = 2
	grad_dict = {}
	for i in range(0,5):
		grad_dict[color_stops[i][idx]] = colors[i]
	return grad_dict

@dajaxice_register
def dataEverything(request, event, fixture_name, head_player_name, tohead_player_name, time1, time2):
	""" Each time a change happens we call this. Returns filtered data
	for heatmaps/pass patterns"""
	factor = 5
	lsum = 290
	bsum = 195
	dajax = Dajax()
	fixture = EventsPz.objects.filter(fixture=fixture_name)
	half1 = 0
	half2 = 0
	half_time_crossed = False

	if(fixture_name == '#'):
		dajax.add_data([], 'doNothing')
		return dajax.json()
	
	half1, half2 = find_half_time(fixture)
	half1 = int(half1)/60 
	half2 = int(half2)/60
	half_time_crossed = (time1<=half1<=time2)
	if(half_time_crossed):
		qset = fixture.filter(Q(half=1, time__gte=time1*60) | Q(half=2, time__lte=(time2-half1)*60))
	else:
		if time2<=half1: 
			qset = fixture.filter(half=1, time__gte=time1*60, time__lte=time2*60)
		else:
			qset = fixture.filter(half=2, time__gte=(time1-half1)*60,time__lte=(time2-half1)*60)

	# Time and match has been filtered, now onto what more is required
	if(int(event) == 0):
		#Draw a heat map

		out = qset.filter(player1name=head_player_name).values_list('xposorigin', 'yposorigin', 'half')
		sz_head = len(out)	
		data_list = []
		#Reflection about the origin according to the half
		count_head, max_head = decide_max_count(sz_head)
		gradient_head = construct_gradient(sz_head)
		for i in out:
			if(int(i[2]) == 2):
				data_list.append({'x': -factor*int(i[0])+lsum, 'y': factor*int(i[1])+bsum, 'count': count_head})
			else:
				data_list.append({'x': factor*int(i[0])+lsum, 'y': -factor*int(i[1])+bsum, 'count': count_head})
		
		data_head = {'max':max_head, 'data': data_list}


		out = qset.filter(player1name=tohead_player_name).values_list('xposorigin', 'yposorigin', 'half')
		sz_tohead = len(out)
		data_list = []
		count_tohead, max_tohead = decide_max_count(sz_tohead)
		gradient_tohead = construct_gradient(sz_tohead)
		#Reflection about the origin according to the half
		for i in out:
			if(int(i[2]) == 2):
				data_list.append({'x': -factor*int(i[0])+lsum, 'y': factor*int(i[1])+bsum, 'count': count_tohead})
			else:
				data_list.append({'x': factor*int(i[0])+lsum, 'y': -factor*int(i[1])+bsum, 'count': count_tohead})

		data_tohead = {'max':max_tohead, 'data': data_list}
		data = {'data_head':data_head, 
				'data_tohead':data_tohead, 
				'gradient_head':gradient_head, 
				'gradient_tohead':gradient_tohead}

		dajax.add_data(data, 'drawHeatMaps')
		return dajax.json()
	else:
		data = {}
		out = qset.filter(player1name=head_player_name, 
							eventname='Pass').values_list(
							'xposorigin', 
							'yposorigin', 
							'xposdest', 
							'yposdest', 'half')
		data_list = []
		for i in out:
			if(int(i[4]) == 2):
				data_list.append((-factor*int(i[0])+lsum, factor*int(i[1])+bsum, -factor*int(i[2])+lsum, factor*int(i[3])+bsum))
			else:
				data_list.append((factor*int(i[0])+lsum, -factor*int(i[1])+bsum, factor*int(i[2])+lsum, -factor*int(i[3])+bsum))

		data['head'] = data_list
		out = qset.filter(player1name=tohead_player_name, 
							eventname='Pass').values_list(
							'xposorigin', 
							'yposorigin', 
							'xposdest', 
							'yposdest', 'half')

		data_list = []
		for i in out:
			if(int(i[4]) == 2):
				data_list.append((-factor*int(i[0])+lsum, factor*int(i[1])+bsum, -factor*int(i[2])+lsum, factor*int(i[3])+bsum))
			else:
				data_list.append((factor*int(i[0])+lsum, -factor*int(i[1])+bsum, factor*int(i[2])+lsum, -factor*int(i[3])+bsum))

		data['tohead'] = data_list
		dajax.add_data(data, 'drawPassMaps')
		return dajax.json()	

