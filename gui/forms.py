from django import forms
from gui.models import EventsPz

EVENT_CHOICES = ((0, 'Heat Map'), (1, 'Passes by Player'))
class LeftPanel(forms.Form):
	""" The only form widget in the entire webapp belongs to this class """
	dajax_call = "Dajaxice.gui.dataEverything(Dajax.process, {'event':$('#id_event_type').val(),'fixture_name':$('#id_match_name').val(), \
													'head_player_name':$('#id_head_player').val(), \
													'tohead_player_name':$('#id_tohead_player').val(), \
													'time1':$('#slider_range').slider('values', 0),  \
													'time2':$('#slider_range').slider('values', 1)}); \
													$('#loader').show();"
	event_type = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'clearCanvas();'+dajax_call}),
			required=True, choices=EVENT_CHOICES)

	matches = EventsPz.objects.values_list('fixture', flat=True).distinct().order_by('fixture')
	match_list = []
	match_list.append(('#','Select a Match'))
	for i in matches:
		match_list.append((str(i),str(i)))

	match_name = forms.ChoiceField(widget=forms.Select(
		attrs={'onchange':"Dajaxice.gui.update_players(Dajax.process, {'option':this.value}); $('#loader').show(); clearCanvas();",'size':"1"}), 
			required=True, choices=match_list)

	#Can we clean up this code a bit please? 
	dajax_call = "Dajaxice.gui.dataEverything(Dajax.process, {'event':$('#id_event_type').val(),'fixture_name':$('#id_match_name').val(), \
													'head_player_name':$('#id_head_player').val(), \
													'tohead_player_name':$('#id_tohead_player').val(), \
													'time1':$('#slider_range').slider('values', 0),  \
													'time2':$('#slider_range').slider('values', 1)}); \
													$('#loader').show();"

	head_player = forms.ChoiceField(widget=forms.Select(attrs={'onchange':dajax_call,  'size':"1"}), required=False, choices=[])

	dajax_call = "Dajaxice.gui.dataEverything(Dajax.process, {'event':$('#id_event_type').val(),'fixture_name':$('#id_match_name').val(), \
													'head_player_name':$('#id_head_player').val(), \
													'tohead_player_name':$('#id_tohead_player').val(), \
													'time1':$('#slider_range').slider('values', 0),  \
													'time2':$('#slider_range').slider('values', 1)}); \
													$('#loader').show();"

	tohead_player = forms.ChoiceField(widget=forms.Select(attrs={'onchange':dajax_call, 'size':"1"}), required=False, choices=[])


