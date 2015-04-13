import random

#Get prime p
#Get generator g which is a primary root
#Send both to server
#Get Xa
#Send g^Xa
#Receive g^Xb
#Compute (g^Xb)^(Xa) as the key

p = 2**256 - 189
phiP = p - 1
g = 0
i = 2
j = 1
while(i < p):
  print i
  while(j < phiP + 1):
    if ( (i**j % p == 1) and j<phiP ):
      break
    elif ( (i**j % p == 1) and (j == phiP) ):
      g = i
      break
    j += 1
  if (g != 0):
    break
  i += 1

print g
