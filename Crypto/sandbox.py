import numpy as np
from client_side_psi import *
import cuckoo_hash as ch

passwords = ["hello", "welcome", "sup"]
# for p in passwords:
#     print(f'{p=}')
#     print(f'{tools.sha256_to_int32(p)=}')

c: ch.Cuckoo = get_cuckoo_items(passwords)
for i, x in enumerate(c.data_structure):
    # print(x)
    pass

windowing_tensor = get_windowing_tensor(c)
# print(windowing_tensor)

context = tools.get_context()
enc_msg = prepare_encrypted_message(windowing_tensor, context)
# print(enc_msg)


from server_side_psi import *

enc = deserialize_client_powers(enc_msg)
# print(enc)
powers = calculate_encrypted_powers(enc)
# print(powers)

passwords_server = ["welcome", "hello", "blabla", "123123123", "asdasdasd", "123qwe"]

h = insert_to_hash_table(passwords_server)
coefficients = get_poly_coefficients(h)

response = get_server_response(powers, coefficients)

dec = decrypt_server_answer(response, context[0])
# print(dec)

intersection = find_intersection(dec, c)
print(intersection)
