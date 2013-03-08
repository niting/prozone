# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class EventsPz(models.Model):
    row_id = models.IntegerField(primary_key=True)
    matchid = models.IntegerField(null=True, db_column='MatchID', blank=True) # Field name made lowercase.
    fixture = models.CharField(max_length=174, db_column='Fixture', blank=True) # Field name made lowercase.
    team1_name = models.CharField(max_length=135)
    team2_name = models.CharField(max_length=135)
    half = models.IntegerField(null=True, db_column='Half', blank=True) # Field name made lowercase.
    time = models.DecimalField(decimal_places=1, null=True, max_digits=12, db_column='Time', blank=True) # Field name made lowercase.
    eventname = models.CharField(max_length=153, db_column='EventName', blank=True) # Field name made lowercase.
    player1 = models.IntegerField(null=True, db_column='Player1', blank=True) # Field name made lowercase.
    player1name = models.CharField(max_length=177, db_column='Player1Name', blank=True) # Field name made lowercase.
    player1clubid = models.IntegerField(null=True, db_column='Player1ClubID', blank=True) # Field name made lowercase.
    player1club = models.CharField(max_length=150, db_column='Player1Club', blank=True) # Field name made lowercase.
    player2 = models.IntegerField(null=True, db_column='Player2', blank=True) # Field name made lowercase.
    player2name = models.CharField(max_length=177, db_column='Player2Name', blank=True) # Field name made lowercase.
    player2clubid = models.IntegerField(null=True, db_column='Player2ClubID', blank=True) # Field name made lowercase.
    player2club = models.CharField(max_length=150, db_column='Player2Club', blank=True) # Field name made lowercase.
    xposorigin = models.DecimalField(decimal_places=3, null=True, max_digits=12, db_column='XPosOrigin', blank=True) # Field name made lowercase.
    yposorigin = models.DecimalField(decimal_places=3, null=True, max_digits=12, db_column='YPosOrigin', blank=True) # Field name made lowercase.
    xposdest = models.DecimalField(decimal_places=3, null=True, max_digits=12, db_column='XPosDest', blank=True) # Field name made lowercase.
    yposdest = models.DecimalField(decimal_places=3, null=True, max_digits=12, db_column='YPosDest', blank=True) # Field name made lowercase.
    team1_id = models.IntegerField(null=True, blank=True)
    team2_id = models.IntegerField(null=True, blank=True)
 
    class Meta:
        db_table = u'events_pz'

