import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from config import *
import json
import nexmo
import requests
from datetime import datetime
from base64 import urlsafe_b64encode
import os
import calendar
from jose import jwt
from pubnub import Pubnub

pubnub = Pubnub(publish_key=pubnubPubKey, subscribe_key=pubnubSubKey)


def mint_token(application_id=app_uuid, keyfile=keyfile):
	application_private_key = open(keyfile, 'r').read()
	d = datetime.utcnow()
	token_payload = {
		"iat": calendar.timegm(d.utctimetuple()),  # issued at
		 "application_id": application_id,  # application id
		 "jti": urlsafe_b64encode(os.urandom(64)).decode('utf-8')
	}
	return jwt.encode(
		claims=token_payload,
		key=application_private_key,
		algorithm='RS256')


class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render('templates/index.html',
					inboundNumber=inboundNumber,
					pubnubPubKey=pubnubPubKey, 
					pubnubSubKey=pubnubSubKey)
		
class CallHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		fr=self.get_argument("from", None)
		to = self.get_argument("to", None)
		ncco=[]
		a= {}
		a['action'] = 'record'
		a['eventUrl'] = [ base+'/recording?fr={}&to={}'.format(fr, to) ]
		a['beepStart'] = "false"
		ncco.append(a)
		a = {}
		a['action'] = "connect"
		a['eventUrl'] = [ base + "/event"]
		a['endpoint'] = []
		e = {}
		e['type'] = 'phone'
		e['number'] = proxyToNumber
		a['endpoint'].append(e)	
		a['from'] = fr
		ncco.append(a)
		self.content_type = 'application/json'
		self.write(json.dumps(ncco))
		self.set_header('Content-Type', 'application/json')
		self.finish()

class RecordingHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		data = json.loads(self.request.body)
		download_id = data["recording_url"].split("=")[1]
		playback_url = base + "/play/" + download_id
		to = self.get_argument("to", None)
		fr = self.get_argument("fr", None)
        
		message = "Recording of call From: {} To: {} Recording: {}".format(fr, to, playback_url)
        
		client = nexmo.Client(key=nexmo_apikey, secret=nexmo_secret)
		client.send_message({'from': 'Nexmo', 'to': proxyToNumber, 'text': message})
		
		pubnub.publish('call', message)
		
		self.content_type = 'text/plain'
		self.write('ok')
		self.finish()


class PlaybackHandler(tornado.web.RequestHandler):
	def get(self, slug):
		url = 'https://api.nexmo.com/media/download?id={}&api_key={}&api_secret={}'.format(slug, nexmo_apikey, nexmo_secret)
		response = requests.get(url)
		self.write(response.content)
		self.set_header('Content-Type', 'audio/mpeg')
		self.finish()

class EventHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		data = json.loads(self.request.body)
		pubnub.publish('call', data)
		self.set_status(204)
		self.finish()
		
class MessageHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		if self.get_argument('text', None) == None:
			self.content_type = 'text/plain'
			self.write("No Text")
			self.finish()
		else:
			msisdn=self.get_argument("msisdn", None)
			text = self.get_argument("text", None)
			to=self.get_argument("to", None)
			message = "New Message From: {} to {}\r\r{}".format(msisdn, to, text)
			client = nexmo.Client(key=nexmo_apikey, secret=nexmo_secret)
			client.send_message({'from':  msisdn, 'to': destination, 'text': message})
			self.content_type = 'text/plain'
			self.write("OK")
			self.finish()
			
					
def main():
	static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	print static_path
	application = tornado.web.Application([(r"/", MainHandler),
											(r"/call", CallHandler),
											(r"/event", EventHandler),
											(r"/recording", RecordingHandler),
											(r"/play/(.*)", PlaybackHandler),
											(r"/message", MessageHandler),
											(r'/s/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
											])
	application.debug = True
	http_server = tornado.httpserver.HTTPServer(application)
	port = int(os.environ.get("PORT", 5000))
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
	
	
