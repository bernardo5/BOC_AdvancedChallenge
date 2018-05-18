import requests
from flask import Flask, request, make_response, redirect, abort, render_template
from requests.auth import HTTPBasicAuth
from StringIO import StringIO
from PIL import Image
import profile
import json

app=Flask(__name__) #needs to be right after import

#this is the start of the main script
devId='aaa6195f-fa9b-42d9-af14-915abaec20e7'

#initialize lists
locations=[]
TheServers=[]
TheApps=[]

#------------------------------------------------------------------------- 4 List of Locations ----------------------------------------------------------------------
#this function will handle the get requests for bot locations, servers and info
def getRequestChallengeTwo(devId, endpoint):
	response=requests.get(endpoint, auth=('WeAreDevelopers', 'YesWeAre'), headers={'Authorization': 'TOK:aaa6195f-fa9b-42d9-af14-915abaec20e7', 'developerID' : devId})
	return response

#this class stores the info regarding the locations
class LocationObject(object):
	"""docstring for LocationObject"""
	def __init__(self, id, name, description, servers, latitude, longitude):
		super(LocationObject, self).__init__()
		self.id = id
		self.name=name
		self.description=description
		self.servers=servers
		self.latitude=latitude
		self.longitude=longitude

#this class stores the info regarding the servers inside the locations
class ServerObject(object):
	"""docstring for ServerObject"""
	def __init__(self, id, name):
		super(ServerObject, self).__init__()
		self.id = id
		self.name=name
		
#this method stores the locations inside the classes
def processListOfLocations(response):
	if response.status_code==requests.codes.ok:
		#the request was successfull
		print 'got the locations'
		myLocationsJSON = json.loads(response.text)
		myPayload=myLocationsJSON['payload']
		#get the locations as a list
		for loc in myPayload:
			itServers=[]
			#get the servers from a location
			for s in loc['servers']:
				itServers.append(ServerObject(s['id'], s['name']))

			itLocation=LocationObject(loc['id'], loc['name'], loc['description'], itServers, loc['latitude'], loc['longitude'])
			locations.append(itLocation)
	else:
		print 'error fetching locations'
		exit(0)

#---------------------------------------------------------------------------------- 5 List of servers ----------------------------------------------------------------
class ServerObjectMain(object):
	"""docstring for ServerObjectMain"""
	def __init__(self, id, name, description, applications):
		super(ServerObjectMain, self).__init__()
		self.id=id
		self.name=name
		self.description=description
		self.applications=applications

class ApplicationObject(object):
	"""docstring for ApplicationObject"""
	def __init__(self, id, name):
		super(ApplicationObject, self).__init__()
		self.id=id
		self.name=name

def processListOfServers():
	serversResponse=getRequestChallengeTwo(devId, 'https://wad-challenge-2018.boc-cloud.com/rest/dev/servers/')
	if serversResponse.status_code==requests.codes.ok:
		print 'got the servers'
		serversPayload=json.loads(serversResponse.text)['payload']
		for serv in serversPayload:
			itApps=[]
			#get the servers from a location
			for s in serv['applications']:
				itApps.append(ApplicationObject(s['id'], s['name']))

			itServer=ServerObjectMain(serv['id'], serv['name'], serv['description'], itApps)
			TheServers.append(itServer)
	else:
		print 'error fetching the servers'


#---------------------------------------------------------------------- 6 List of Applications-----------------------------------------------------------------------------
class ApplicationsObjectMain(object):
	"""docstring for ApplicationsObjectMain"""
	def __init__(self, id, name, description):
		super(ApplicationsObjectMain, self).__init__()
		self.id=id
		self.name=name
		self.description=description

def processListOfApps():
	AppsResponse=getRequestChallengeTwo(devId, 'https://wad-challenge-2018.boc-cloud.com/rest/dev/applications/')
	if AppsResponse.status_code==requests.codes.ok:
		print 'got the apps'
		AppsPayload=json.loads(AppsResponse.text)['payload']
		for app in AppsPayload:
			TheApps.append(ApplicationsObjectMain(app['id'], app['name'], app['description']))
	else:
		print 'error fetching the servers'

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#From here on, the calls just retrieve one entry and actions are regarding the click of a single id (user interaction in the website)

#-------------------------------------------------------------------- 7 List of Location Details --------------------------------------------------------

class LocationDetails(object):
	"""docstring for TheLocationDetails"""
	def __init__(self, id, name, description, needForAction, servers, latitude, longitude):
		super(LocationDetails, self).__init__()
		self.id=id
		self.name=name
		self.description=description
		self.needForAction=needForAction
		self.servers=servers
		self.latitude=latitude
		self.longitude=longitude

class ServerLocDetail(object):
	"""docstring for ServerLocDetail"""
	def __init__(self, id, name):
		super(ServerLocDetail, self).__init__()
		self.id=id
		self.name=name
		

def getLocationDetails(locId):
	LocationDetailsResponse=getRequestChallengeTwo(devId, 'https://wad-challenge-2018.boc-cloud.com/rest/dev/locations/'+locId+'/')
	if LocationDetailsResponse.status_code==requests.codes.ok:
		print 'got the location details'
		LocationDetailsPayload=json.loads(LocationDetailsResponse.text)['payload']
		#need_for_action
		serversInLocDetails=[]
		for servDet in LocationDetailsPayload['servers']:
			serversInLocDetails.append(ServerLocDetail(servDet['id'], servDet['name']))
		return LocationDetails(LocationDetailsPayload['id'], LocationDetailsPayload['name'], LocationDetailsPayload['description'], LocationDetailsPayload['need_for_action'], serversInLocDetails ,LocationDetailsPayload['latitude'], LocationDetailsPayload['longitude'])
	else:
		print 'error fetching the servers'

#--------------------------------------------------------------- 8 location of server details ------------------------------------------------------

class ServerDetails(object):
	"""docstring for TheLocationDetails"""
	def __init__(self, id, name, description, apps,need_for_action):
		super(ServerDetails, self).__init__()
		self.id=id
		self.name=name
		self.description=description
		self.applications=apps
		self.needForAction=need_for_action

class AppLocDetail(object):
	"""docstring for ServerLocDetail"""
	def __init__(self, id, name):
		super(AppLocDetail, self).__init__()
		self.id=id
		self.name=name

def getServerDetails(serverId):
	ServerDetailsResponse=getRequestChallengeTwo(devId, 'https://wad-challenge-2018.boc-cloud.com/rest/dev/servers/'+serverId+'/')
	if ServerDetailsResponse.status_code==requests.codes.ok:
		print 'got the server details'
		ServerDetailsPayload=json.loads(ServerDetailsResponse.text)['payload']
		#need_for_action
		AppsInDetails=[]
		for appDet in ServerDetailsPayload['applications']:
			AppsInDetails.append(AppLocDetail(appDet['id'], appDet['name']))
		return ServerDetails(ServerDetailsPayload['id'], ServerDetailsPayload['name'], ServerDetailsPayload['description'], AppsInDetails,ServerDetailsPayload['need_for_action'])
	else:
		print 'error fetching the servers'

#----------------------------------------------------------- 9 Application details -----------------------------------------------------
class ApplicationDetails(object):
	"""docstring for ApplicationDetails"""
	def __init__(self, id, name, description, need_for_action, investment_cost, operation_cost, category):
		super(ApplicationDetails, self).__init__()
		self.id=id
		self.name=name
		self.description=description
		self.need_for_action=need_for_action
		self.investment_cost=investment_cost
		self.operation_cost=operation_cost
		self.category=category

def getApplicationDetails(AppId):
	ApplicationDetailsResponse=getRequestChallengeTwo(devId, 'https://wad-challenge-2018.boc-cloud.com/rest/dev/applications/'+AppId+'/')
	if ApplicationDetailsResponse.status_code==requests.codes.ok:
		print 'got the application details'
		ApplicationDetailsPayload=json.loads(ApplicationDetailsResponse.text)['payload']
		print ApplicationDetailsPayload
		return ApplicationDetails(ApplicationDetailsPayload['id'], ApplicationDetailsPayload['name'], ApplicationDetailsPayload['description'],ApplicationDetailsPayload['need_for_action'],ApplicationDetailsPayload['investment_cost'],ApplicationDetailsPayload['operating_cost'],ApplicationDetailsPayload['category'])
	else:
		print 'error fetching the servers'
		

#----------------------------------------------------------------------------------------------------------------------------------------------------------


@app.route('/')
def index():
	#4 fetch list of locations
	myLocationsRaw=getRequestChallengeTwo(devId, 'https://wad-challenge-2018.boc-cloud.com/rest/dev/locations/')

	if len(locations)==0:
		processListOfLocations(myLocationsRaw)

	if len(TheServers)==0:
		#5
		processListOfServers()
	if len(TheApps)==0:
		#6
		processListOfApps()
	#7
	#print getLocationDetails(locations[0].id).name
	#8
	#print getServerDetails(TheServers[0].id).name
	#9
	#print getApplicationDetails(TheApps[0].id).category
	return render_template('index.html', applications=TheApps, servers=TheServers, locations=locations, LocationDetails=[], locCoordinates=[], loc=False, detail=False)

@app.route('/detailsServer', methods=['POST'])
def ServDetails():
	if request.method=="POST":
		ServId = request.form['idServer']
		myServDetails=getServerDetails(ServId)
		detailsDictionary={}
		detailsDictionary["Id"]=myServDetails.id
		detailsDictionary["Name"]=myServDetails.name
		detailsDictionary["Description"]=myServDetails.description
		detailsDictionary["Applications"]=listList(myServDetails.applications)
		detailsDictionary["Need For Action"]=myServDetails.needForAction
		return render_template('index.html', applications=TheApps, servers=TheServers, locations=locations, details=detailsDictionary, loc=False, detail=True, locCoordinates=[])

def listList(serversList):
	listToGet=""
	i=0
	for server in serversList:
		if i==0:
			listToGet=listToGet+server.name
		else:
			listToGet=listToGet+", "+server.name
		i=i+1
	return listToGet

@app.route('/detailsLocation', methods=['POST'])
def LocDetails():
	if request.method=="POST":
		LocId = request.form['idLocation']
		myLocDetails=getLocationDetails(LocId)
		detailsDictionary={}
		detailsDictionary["Id"]=myLocDetails.id
		detailsDictionary["Name"]=myLocDetails.name
		detailsDictionary["Description"]=myLocDetails.description
		detailsDictionary["Need For Action"]=myLocDetails.needForAction
		detailsDictionary["Servers"]=listList(myLocDetails.servers)
		detailsDictionary["Latitude"]=myLocDetails.latitude
		detailsDictionary["Longitude"]=myLocDetails.longitude

		return render_template('index.html', applications=TheApps, servers=TheServers, locations=locations, details=detailsDictionary, locCoordinates=myLocDetails, loc=True, detail=True)

@app.route('/detailsApplication', methods=['POST'])
def AppDetails():
	if request.method=="POST":
		AppId = request.form['idApplication']
		myAppDetails=getApplicationDetails(AppId)
		detailsDictionary={}
		detailsDictionary["Id"]=myAppDetails.id
		detailsDictionary["Name"]=myAppDetails.name
		detailsDictionary["Description"]=myAppDetails.description
		detailsDictionary["Need For Action"]=myAppDetails.need_for_action
		detailsDictionary["Investment Cost"]=myAppDetails.investment_cost
		detailsDictionary["Operation Cost"]=myAppDetails.operation_cost
		detailsDictionary["Category"]=myAppDetails.category
		return render_template('index.html', applications=TheApps, servers=TheServers, locations=locations, details=detailsDictionary, loc=False, detail=True, locCoordinates=[])
