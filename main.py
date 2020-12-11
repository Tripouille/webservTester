import client

class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def checkStatus(answer, status, reason):
	print("Status: nginx: [{}] webserv: [{}]".format(status, answer.status), colors.GREEN + "OK" if answer.status == status else colors.RED + "KO", colors.RESET)

serv = client.HTTPConnection('localhost:80')
#serv.set_debuglevel(1);
headers = {"Host": ""}
print('GET', '/', "no host")
serv.request('GET', '/',None, headers)
answer = serv.getresponse()
checkStatus(answer, 400, "OK")
#print("{}\n".format(answer.read()))
headers = {"Host": "localhost"}
print('GET', '/', "valid host")
serv.request('GET', '/',None, headers)
answer = serv.getresponse()
checkStatus(answer, 200, "OK")
#print("{}\n".format(answer.read()))

serv.close()