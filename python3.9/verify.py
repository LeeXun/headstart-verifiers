import sys
if sys.version_info[0] != 3:
    print("\033[91m  Please use python 3.9!\033[0m")
    sys.exit()

# from lib.merkle import MerkleVerifier
import json
import urllib
import os
import requests
import random
from datetime import datetime, timedelta
# chiavdf 1.0.6
from chiavdf import create_discriminant, verify_wesolowski

if __name__ == "__main__":

    # 6 * 5 mins = 30 mins
    num_to_verify = 6

    initial_el = b"\x08" + (b"\x00" * 99)
    form_size = 100
    lambda_security_bits = 1024
    t = 25000000
    host = "https://api.hsrand.tw"
    url = "{0}/api/v1/delayproofs".format(
            host)
    response = requests.request("GET", url)
    if response.status_code != 200:
        print(response.text)
        sys.exit()

    delay_proofs = json.loads(response.text)

    for i, p in enumerate(delay_proofs):
        if i >= num_to_verify or i >= len(delay_proofs)-1:
            break

        prev_result = delay_proofs[i+1]["result"]
        discriminant_challenge = p["root_hash"] + prev_result
        discriminant = create_discriminant(
            discriminant_challenge.encode(), lambda_security_bits)
        result_bytes = bytes.fromhex(p["result"])

        is_valid = verify_wesolowski(
            str(discriminant),
            initial_el,
            result_bytes[:form_size],
            result_bytes[form_size: 2 * form_size],
            t,
        )
        print("i={0} id={1} date={2} is_valid={3}".format(
        i,
        p["id"],
        datetime.fromtimestamp(p["root_hash_time"]/1000),
        is_valid))

        if is_valid==False:
            os.exit()

    print("Valid")