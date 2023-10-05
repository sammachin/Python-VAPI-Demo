# Python-VAPI-Demo

## ❗❗❗ **This repo is now deprecated. Check the [Vonage Developer Blog](https://developer.vonage.com/en/blog) for more blog posts and tutorials. For more sample Vonage projects, check the [Vonage Community GitHub repo](https://github.com/Vonage-Community).**

This app used the Voice API to demonstrate a few features.

* Incoming calls are proxied to a destination number
* The call is recorded
* A Link to the recording is sent to the destination number after the call

* All Call Events are published using PubNub to the main web page. Currently the events are just logged to the console. Please extend this view as you wish.

## Prerequisites

You will need:

* A Nexmo LVN (Phone Number)
* A New application
* Somewhere to host this web app, Heroku or Your Local Machine with ngrok both work well

## Installation

```sh
git clone https://github.com/nexmo-community/Python-VAPI-Demo.git
cd Python-VAPI-Demo
pip install -r requirements.txt
```

## Setup

Create the nexmo applicaiton, using the [Nexmo CLI](https://github.com/nexmo/nexmo-cli):

```sh
nexmo app:create MyFirstVAPIApp --keyfile key.txt http://example.com http://example.com
```

Check that the private key has been saved to key.txt e.g. `cat key.txt`.

Rename the config file:

```sh
mv example_config.py config.py
```

Fill in the values in `config.py` as appropriate.

Link the LVN to the app id with the Nexmo CLI:

```sh
nexmo link:app [LVN] [app-id]
```

Update the app to set the webhook urls to be your server instead of the example.com placeholders used at creation.

```sh
nexmo app:update ['app-id'] MyFirstVAPIApp [your url]/call [your url]/event
```

We recommend using [ngrok](https://ngrok.com/) to tunnel through to your locally running application. In which case the command above is likely to be something similar to:

```sh
nexmo app:update ['app-id'] MyFirstVAPIApp https://___.ngrok.io/call https://___.ngrok.io/event
```

Where `___` should be replaced with the `ngrok.io` subdomain you are assigned.

### Running the App

If you have [foreman](https://github.com/ddollar/foreman) installed you can start the app by running:

```sh
foreman start
```

Otherwise, you can run directly using Python:

```sh
python app.py
```

In both cases the application should be available on <http://localhost:5000>.

### Using the App

Navigate to <http://localhost:5000>, and open up the JavaScript console.

Now, call the number that's listed on the page. From there you'll see events being logged to the JavaScript console as they come in to your application.

When the call is finished a text message will be sent to the number that all calls are being proxied to with a URL for the call recording. The URL for the call recording will also be pushed to the web browser.
