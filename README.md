# Python-VAPI-Demo

This app used the Voice API to demonstrate a few features.

*Incomming calls are proxied to a destination number
*The call is recorded
*A Link to the recording is sent to the destination number after the call

*All Call Events are published using PubNub to the main web page, Currently the events are just logged to the console, extend this view as you wish.

## Installation
You will need:
* A Nexmo LVN (Phone Number)
* A New application
* Somewhere to host this web app, Heroku or Your Local Machine with ngrok both work well

clone this repo `git clone https://github.com/nexmo-community/Python-VAPI-Demo.git`
Move into the application director `cd Python-VAPI-Demo`
Create the nexmo applicaiton, using the nexmo cli type `nexmo app:create MyFirstVAPIApp --keyfile key.txt http://example.com http://example.com`
Check that the private key has been saved to key.txt `cat key.txt`

rename example_config.py to config.py
Fill in the values in config.py as appropriate.

link the LVN to the app id with the nexmo cli `nexmo link:app [LVN] [app-id]`
Update the app to set the webhook urls to be your server instead of the example.com placeholders used at creation.
`nexmo app:update ['app-id'] MyFirstVAPIApp [your url]/call [your url]/event`
