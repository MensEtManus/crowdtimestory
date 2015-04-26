from crowdtimestory import app
from OpenSSL import SSL

'''
PORT = 8012 
URL_PREFIX = '/%02d'%(PORT % 100)
app.debug = True
app.run(host='127.0.0.1', port=PORT)
'''

context = ('key.crt', 'key.key')
app.debug = True
app.run(host='128.46.32.82', port=8012, ssl_context=context)


