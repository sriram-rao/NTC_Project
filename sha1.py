import struct

def left_rotate(number, bits):
   result = ( (number << bits) | ( number >> (32 - bits) ) ) & 0xffffffff
   return result

def sha1(message):

   h0 = 0x67452301
   h1 = 0xEFCDAB89
   h2 = 0x98BADCFE
   h3 = 0x10325476
   h4 = 0xC3D2E1F0

   message_len_in_bytes = len(message)
   message_len_in_bits = message_len_in_bytes * 8

   #Padding:
   #Append a '1' bit
   message += b'\x80'
   #Append '0' bits until message length is 64 bits less than a multiple of 512 bits
   message += b'\x00' * ( ( 56 - (message_len_in_bytes + 1) % 64) % 64 )
   #Append 64 bits of length of string
   message += struct.pack(b'>Q', message_len_in_bits)

   #Message is hashed in pieces of 512 bits = 64 bytes
   for i in range(0, len(message), 64):

      w = [0] * 80

      for j in range(16):
         w[j] = struct.unpack(b'>I', message[i + j*4:i + j*4 + 4])[0]
      for j in range(16, 80):
         w[j] = left_rotate(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)

      a = h0
      b = h1
      c = h2
      d = h3
      e = h4

      for j in range(80):
         if ( 0 <= j <= 19 ):
            f = d ^ (b & (c ^ d))
            k = 0x5A827999
         elif ( 20 <= j <= 39 ):
            f = b ^ c ^ d
            k = 0x6ED9EBA1
         elif ( 40 <= j <= 59 ):
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
         elif ( 60 <= j <= 79 ):
            f = b ^ c ^ d
            k = 0xCA62C1D6

         a, b, c, d, e = ((left_rotate(a, 5) + f + e + k + w[j]) & 0xffffffff, a, left_rotate(b, 30), c, d)

      h0 = (h0 + a) & 0xffffffff
      h1 = (h1 + b) & 0xffffffff
      h2 = (h2 + c) & 0xffffffff
      h3 = (h3 + d) & 0xffffffff
      h4 = (h4 + e) & 0xffffffff

   return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)
