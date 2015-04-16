import random
import socket

#Get prime p
#Get generator g
#Send both to server
#Get Xa
#Send g^Xa
#Receive g^Xb
#Compute (g^Xb)^(Xa) as the key

def modular_pow(base, exponent, modulus):

    result = 1
    base = base % modulus
    while (exponent > 0):
        if (exponent % 2 == 1):
           result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def dh_key_client(client):
  p = 2**256 - 189
  g = random.getrandbits(257) % p

  share = str(p) + "," + str(g)
  client.send(share)

  a = random.getrandbits(257) % p
  public = modular_pow(g, a, p)

  client.send(str(public))
  server_public = client.recv(1024)
  server_public = int(server_public)

  key = modular_pow(server_public, a, p)
  # print key
  return key
