import client

serv = client.HTTPConnection('localhost:80')
#serv.set_debuglevel(1);
print('GET', '/')
serv.request('GET', '/')
answer = serv.getresponse()
print('Status: ', answer.status,' Reason: ', answer.reason)
print("{}\n".format(answer.read()))

print('GET', '/banana')
serv.request('GET', '/banana')
answer = serv.getresponse()
print('Status: ', answer.status,' Reason: ', answer.reason)
print("{}\n".format(answer.read()))

serv.close()