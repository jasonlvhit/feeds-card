import requests
import urllib2
from lxml import etree
from lxml import html
from feeds import app
from flask import render_template, request


@app.route("/git_activity", methods=['GET', 'POST'])
def git_activity():
    username = request.args.get('username')
    number = 10
    if request.args.get('number'):
        number = request.args.get('number')

    BASE_URL = 'https://github.com/{{ username }}.atom'
    req_url = BASE_URL.replace('{{ username }}', username)

    try:
        f = urllib2.urlopen(req_url)
    except Exception as e:
        print(e.code)

    r = etree.XML(f.read())
    activity_node = [i[-1].text for i in r[5:5 + int(number)]]
    return render_template('git_activity.html', activities=activity_node)


@app.route("/douban_activity", methods=['GET'])
def douban_activity():
    username = request.args.get('username')
    number = 20
    if request.args.get('number'):
        number = int(request.args.get('number'))

    BASE_URL = "http://www.douban.com/people/{{ username }}/statuses"
    req_url = BASE_URL.replace('{{ username }}', username)

    r = urllib2.Request(req_url)
    r.add_header('User-Agent',
                 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')

    try:
        f = urllib2.urlopen(r)
    except Exception as e:
        print(e.code)

    e = html.fromstring(f.read())
    l = e.find_class("status-item")
    contents = [html.tostring(i) for i in l[:int(number)]]
    return render_template('douban_activity.html', contents=contents, username=username)
