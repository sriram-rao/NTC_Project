import random
import math
import itertools

def getPrime(k):
  num_list = range(2, int(math.sqrt(k)))
  factor = 1
  sieve = []
  for i in num_list:
     sieve.append({'num': i, 'state': "uncrossed"})

  for i in sieve:
     if (i['state'] == "crossed"):
  	continue;
     if (k % i['num'] == 0):
	factor = i['num']
	break;
     else:
	for j in sieve:
	   if (j['num'] % i['num'] == 0):
	      j['state'] = "crossed"
  
  if (factor == 1):
    return k
  else:
    return getPrime(k+2)

def getMersennePrime():
  k = random.getrandbits(10) * 2 + 1
  #print getPrime(k)
  s = 4
  for _ in itertools.repeat(None, k-2):
    s = ((s*s) - 2)%k
  if (s == 0): return k
  else: return 0

prime = getMersennePrime()
while (prime == 0):
  prime = getMersennePrime()

print prime
