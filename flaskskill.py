#!/usr/bin/env python
import os
import subprocess
import logging
from flask import Flask, render_template, request
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.CRITICAL)

def execute(command):
	try:
		alexa_pid = subprocess.check_output('pgrep SampleApp', shell=True)
	except subprocess.CalledProcessError:
		alexa_pid = None

	if alexa_pid:
		os.system('kill -TSTP ' + alexa_pid)

	os.system(command)
	
	if alexa_pid:
		os.system('kill -CONT ' + alexa_pid)
	
@ask.intent('Fan', default={'speed':'off'})
def fan(speed):
	commands = {'low': 'fan_low',
				'medium': 'fan_med',
				'high': 'fan_high',
				'hi': 'fan_high',
				'off': 'fan_off'}
	print('Changing fan speed to ' + speed)
	if speed in commands:
		execute('./lights ' + commands[speed])
	else:
		return statement('Invalid fan speed')

	return statement('Fan set to ' + speed)

@ask.intent('LightsOn')
def lights_on(level):
	print('Toggling lights')
	execute('./lights lights_on')
	return  statement('on')



@app.route('/lights', methods=('GET', 'POST'))
def lights():
	if request.remote_addr != '192.168.0.1':
		return 'nah'

	if request.method == 'POST':
		actions = {'Lights': 'lights_on',
				   'Fan off': 'fan_off',
				   'Fan low': 'fan_low',
				   'Fan medium': 'fan_med',
				   'Fan high': 'fan_high'}

		action = request.form['action']
		if action in actions:
			a = actions[action]
			execute('./lights ' + a)
	else:
		print('GET')

	return '''<style>
				input { font-size: 24px; width: 200px; height: 200px; }
			  </style>
			  <form method="POST">
				<input type="submit" name='action' value="Lights" />
			    <input type="submit" name='action' value='Fan off' />
			    <input type="submit" name='action' value='Fan low' />
			    <input type="submit" name='action' value='Fan medium' />
			    <input type="submit" name='action' value='Fan high' />
			  </form>'''

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=443, ssl_context=('/etc/letsencrypt/live/end.asuscomm.com/fullchain.pem', '/etc/letsencrypt/live/end.asuscomm.com/privkey.pem'), debug=False)

