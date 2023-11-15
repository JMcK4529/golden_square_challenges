# Process Log

make_cipher(key):
uses chr() to increase unicode value of each letter in the alphabet by 98
concatenates this with the key's characters in a list
removes duplicates
returns this list as the cipher
> This was creating an alphabet of 25 letters, should be 26
> Alphabet ran from "b" to "{", should have been "a" to "z"
> Changed range(1,26) to range(26)
> Changed chr(i + 98) to chr(i + 97) 

Now the encoding works properly.

Decoding still fails.

decode(encrypted, key):
Should first create the same cipher as above
> It does

Then should take 65 off the chr() value for each ciphered character
This shoud produce a list of indices corresponding to the cipher
For each index, add cipher[index] to the plaintext_chars
return the plaintext_chars as a joined string
> Changed cipher[65 - ord(i)] to cipher[ord(i) - 65]

Decoding now works!
