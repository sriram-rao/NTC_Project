import socket
import random

#Receive g, p from client
#Get an Xb
#Receive g^Xa
#Send g^Xb
#Compute key

def modular_pow(base, exponent, modulus):

    result = 1
    base = base % modulus
    while (exponent > 0):
        if (exponent % 2 == 1):
           result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def dh_key_server(connection):
   buff = connection.recv(1024)
   if len(buff) > 0:
      p = int(buff.split(',')[0])
      g =int(buff.split(',')[1])
   # print p
   # print g

   a = random.getrandbits(257) % p
   public = modular_pow(g, a, p)

   client_public = connection.recv(1024)
   client_public = int(client_public)
   # print client_public

   connection.send(str(public))

   key = modular_pow(client_public, a, p)
   # print key
   return key
