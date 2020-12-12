import client

#Connection
nginx = client.HTTPConnection('localhost:80')
#nginx.set_debuglevel(1)
webserv = client.HTTPConnection('localhost:8080')

class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def checkStatus(nginxAnswer, webservAnswer):
	print("Status: nginx: [{}] webserv: [{}]".format(nginxAnswer.status, webservAnswer.status), colors.GREEN + "OK" if nginxAnswer.status == webservAnswer.status else colors.RED + "KO", colors.RESET)

def doRequest(method, path, body, headers):
    nginx.request(method, path, body, headers)
    nginxAnswer = nginx.getresponse()
    webserv.request(method, path, body, headers)
    webservAnswer = webserv.getresponse()
    return nginxAnswer, webservAnswer

def getBody(nginxAnswer, webservAnswer):
    return  nginxAnswer.read(), webservAnswer.read()

#Test 1
print('Test 1:', 'GET', '/', "no host")
nginxAnswer, webservAnswer = doRequest('GET', '/', None, {"Host": ""})
checkStatus(nginxAnswer, webservAnswer)
getBody(nginxAnswer, webservAnswer)
#Test 2
print('Test 2:', 'GET', '/', "valid host")
nginxAnswer, webservAnswer = doRequest('GET', '/', None, {"Host": "localhost"})
checkStatus(nginxAnswer, webservAnswer)
getBody(nginxAnswer, webservAnswer)

#Close
nginx.close()
webserv.close()