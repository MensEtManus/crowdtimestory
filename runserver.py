from crowdtimestory import app
from OpenSSL import SSL

<<<<<<< HEAD
PORT = 5000 
=======
'''
PORT = 8012 
URL_PREFIX = '/%02d'%(PORT % 100)
>>>>>>> yauc-master
app.debug = True
app.run(host='127.0.0.1', port=PORT)
'''

context = ('key.crt', 'key.key')
<<<<<<< HEAD
app.debug = True
app.run(host='128.46.32.82', port=8011, ssl_context=context)
'''
=======
app.debug = False
app.run(host='128.46.32.82', port=8012, ssl_context=context)

>>>>>>> yauc-master

