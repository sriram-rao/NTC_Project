import socket
import dh_client
import blowfish_client
import sha1
from base64 import b64encode

# Make connection with server
# Log in using password - SHA1 and send
# Establish key
# Use key to encrypt micropost
# Send ciphertext

# Set up socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 10001))

choice = 'False'
while(choice != 'Q'):
   choice = raw_input("Login(L) or Register(R) <(Q) to Quit>? ")

   if choice == 'L':
      #Login
      username = raw_input('Username: ')
      password = raw_input('Password: ')
      password = sha1.sha1(password)

      #Get key for all future encryption
      key = dh_client.dh_key_client(client)

      #Convert 256-bit key to (Blowfish) 55-byte ASCII key
      key_length = len(str(key)) + 1
      text_key = ('%%0%dx' % (key_length << 1) % key).decode('hex')[-key_length:]
      text_key = text_key[-32:]
      print "Plaintext key: " + text_key
      pass_enc = blowfish_client.Blowfish(text_key)
      pass_cipher = pass_enc.encrypt(password)
      print "Password ciphertext: " + pass_cipher

      credentials = choice + ',' + username + "," + pass_cipher
      client.send(credentials)

      response = client.recv(1024)
      if response == 'True':
         #Continue with micropost
         print 'Agreed key: ' + str(key)

         login_choice = 'k'
         while login_choice != 'Q':
            login_choice = raw_input('Make a post (M) or View all posts (V) <(Q) for Quit>? ')
            if login_choice == 'M':
               micropost = raw_input('Post: ')
               if len(micropost) < 250:
                  micropost += '\0' * ( 250 - len(micropost) )
               elif len(micropost) > 250:
                  print 'Micropost length must be at most 255 characters'
               if len(micropost) == 250:
                  encryption = blowfish_client.Blowfish(text_key)
                  cipher = b64encode(encryption.encrypt(micropost))
                  print "Ciphertext: " + cipher
                  print "Ciphertext length: " + str(len(cipher)) + "\n"
                  client.send('M,' + cipher)
            elif login_choice == 'V':
               client.send('V,nil')
               all_posts = client.recv(65536)
               print "List of all posts: \n" + all_posts + "\n"
         client.send('Q,nil')
      else:
         print 'Invalid login credentials'
   elif choice == 'R':
      username = raw_input('Enter Username: ')
      password = raw_input('Enter Password: ')
      password = sha1.sha1(password)

      key = dh_client.dh_key_client(client)

      key_length = len(str(key)) + 1
      text_key = ('%%0%dx' % (key_length << 1) % key).decode('hex')[-key_length:]
      text_key = text_key[-55:]

      pass_enc = blowfish_client.Blowfish(text_key)
      pass_cipher = pass_enc.encrypt(password)
      # print "Ciphertext: " + pass_cipher

      credentials = choice + ',' + username + "," + pass_cipher
      client.send(credentials)

client.send('Q')
client.close()
