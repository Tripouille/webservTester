import client
import os

class colors:
	GREEN = '\033[92m'
	RED = '\033[91m'
	RESET = '\033[0m'

def check(name, success):
	print(colors.RESET, name + ": ", colors.GREEN + "OK " if success else colors.RED + "KO ", colors.RESET, end='', sep='')

def test(expectedStatus, method, uri, body, headers, expectedHeaders, expectedBody):
	webserv = client.HTTPConnection('localhost:9999')
	print(colors.RESET, '{0: <100}'.format("\n{} {} {}".format(method, uri, headers)), end='')
	webservAnswer = doRequest(webserv, method, uri, body, headers)
	check("Status", expectedStatus == webservAnswer.status)
	headerSuccess = True
	if expectedHeaders:
		headers = dict(webservAnswer.getheaders())
		for key, value in expectedHeaders.items():
			if key not in headers or headers[key] != value:
				headerSuccess = false
				break
	check("Headers", headerSuccess)
	body = webservAnswer.read().decode("utf-8")
	check("Body", not expectedBody or body == expectedBody)
	webserv.close()

def doRequest(webserv, method, path, body, headers):
	webserv.request(method, path, body, headers)
	webservAnswer = webserv.getresponse()
	return webservAnswer

def putTest(expectedStatus, method, uri, body, headers, expectedHeaders, expectedBody, file):
	if os.path.exists(file): os.remove(file)
	test(expectedStatus, method, uri, body, headers, expectedHeaders, expectedBody)
	check("Put", os.path.exists(file))

test(200, 'GET', '/languages', None, {"Host": "localhost"}, None, None)
test(200, 'GET', '/languages/language.html', None, {"Host": "localhost"}, None, None)
test(200, 'GET', '/languages/language.html', None, {"Host": "localhost", "Accept-Language": "fr"}, {"Content-Location" : "/languages/language.html.fr-CA"}, None)
test(200, 'GET', '/languages/language.html', None, {"Host": "localhost", "Accept-Language": "fr-FR"}, {"Content-Location" : "/languages/language.html.fr-FR"}, None)
test(200, 'GET', '/languages/language.html', None, {"Host": "localhost", "Accept-Language": "fr-FR;q=0.5, en"}, {"Content-Location" : "/languages/language.html.en"}, None)
test(200, 'GET', '/', None, {"Host": "localhost"}, None, None)
test(200, 'GET', '/directory/nop', None, {"Host": "localhost"}, None, "youpi.bad_extension file in YoupiBanane/nop/ (in webservTester)")

putTest(201, 'PUT', '/put_test/createdFile', None, {"Host": "localhost"}, None, None, "www/put_saves/createdFile")
putTest(201, 'POST', '/post_test/createdFile', None, {"Host": "localhost"}, None, None, "www/put_saves/createdFile")

test(204, 'PUT', '/put_test/test_put_save', None, {"Host": "localhost"}, None, None)

test(400, 'GET', '/', None, {"Host": ""}, None, None)

test(501, 'GETO', '/', None, {"Host": "localhost"}, None, None)

print(colors.RESET)