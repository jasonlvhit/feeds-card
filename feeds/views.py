import requests
from lxml import etree
from feeds import app
from flask import render_template, request

@app.route("/git_activity", methods = ['GET','POST'])
def git_activity():
	username = request.args.get('username')
	number = 10
	if request.args.get('number'):
		number = request.args.get('number')
	
	BASE_URL = 'https://github.com/{{ username }}.atom'
	req_url = BASE_URL.replace('{{ username }}', username)

	try:
 		f = requests.get(req_url)
	except requests.exceptions.RequestsException as e:
		print(e.message)

	r = etree.XML(f.content)
	activity_node = [i[-1].text for i in r[5:5 + number]]
	return render_template('git_activity.html', activities = activity_node)
