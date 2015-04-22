from crowdtimestory import app
PORT = 5000 
app.debug = True
app.run(host='127.0.0.1', port=PORT)

'''
from OpenSSL import SSL

PORT = 8012
URL_PREFIX = '/%02d'%(PORT % 100)

context = ('key.crt', 'key.key')
app.debug = True
app.run(host='128.46.32.82', port=8011, ssl_context=context)
'''
