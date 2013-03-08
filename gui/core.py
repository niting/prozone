from gui.models import EventsPz

def find_half_time(qset):
	"""Finding the lengths of the first and second half in Python"""
	half1 = qset.filter(half=1, eventname='End Of Half').values_list('time')[0][0]
	half2 = qset.filter(half=2, eventname='End of Half').values_list('time')[0][0]
	return (half1, half2)
