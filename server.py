import socket
import MySQLdb
import dh_server
import blowfish_server
from base64 import b64decode

# Accept connection from client
# Check credentials in database and respond, continue if success
# Establish key
# Accept ciphertext
# Decrypt ciphertext and add to database

#Set up connection with database
db = MySQLdb.connect(host='localhost', user='root', passwd='fluffier', db='ntc')
cur = db.cursor()

#Set up socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 10001))
server.listen(5)

connection, address = server.accept()

while True:

  key = dh_server.dh_key_server(connection)

  key_length = len(str(key)) + 1
  text_key = ('%%0%dx' % (key_length << 1) % key).decode('hex')[-key_length:]
  text_key = text_key[-32:]
  print "Plaintext key: " + text_key
  buff = connection.recv(1024)
  if buff == 'Q':
   break
  if len(buff) > 0:
   pass_enc = blowfish_server.Blowfish(text_key)
   choice, username, pass_cipher = buff.split(',')
   password = pass_enc.decrypt(pass_cipher)

   #Database check
   if choice == 'L':
      cur.execute('SELECT password FROM users WHERE username = \'' + username + '\'')
      if ( password == cur.fetchall()[0][0] ):
         connection.send('True')
         #continue with micropost
         print 'Agreed key: ' + str(key)

         decryption = blowfish_server.Blowfish(text_key)

         login_choice = 'k'
         while login_choice != 'Q':
            login_choice, cipher = connection.recv(1024).split(',')

            if (login_choice == 'M'):
               print 'Received ciphertext: ' + cipher
               message = decryption.decrypt(b64decode(cipher))
               print 'Received post: ' + message
               message = message.replace('\0','')

               cur.execute('INSERT INTO microposts (post, username) VALUES(\'' + message + '\', \'' + username + '\')')
               db.commit()
            elif (login_choice == 'V'):
               cur.execute('SELECT * FROM microposts')
               result = ''
               for i in cur.fetchall():
                  result += i[2] + ': ' + i[1] + "\n"
               connection.send(result)
      else:
         connection.send('False')
   elif choice == 'R':
      cur.execute('INSERT INTO users (username, password) VALUES(\'' + username + '\', \'' + password + '\')')
      db.commit()

server.close()
