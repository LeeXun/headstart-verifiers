#!/usr/bin/env python

import sys
if sys.version_info[0] != 3:
    print("\033[91m  Please use python 3.9!\033[0m")
    sys.exit()

from lib.merkle import MerkleVerifier
import json

import os
import requests
import random
from datetime import datetime
# chiavdf 1.0.6
from chiavdf import create_discriminant, verify_wesolowski


def shuffle_teams(seed, teams):
    random.Random(seed).shuffle(teams)
    return teams


if __name__ == "__main__":

    print("")
    print("-- Verification of the presentation order of CNS 2022 --")
    print("")

    if len(sys.argv) < 2 or sys.argv[1] == "":
        print("\033[91m  command:\033[0m  \033[96mpython ./{0} 'your_random_code'\033[0m".format(
            os.path.basename((__file__))))
        sys.exit()

    random_code = sys.argv[1]
    host = "https://headstart.leehsun.tw"
    event = {
        "start_time": "2022-05-10T17:00:00.000+08:00",
        "end_time": "2022-05-10T20:00:00.000+08:00",
    }

    start_time = datetime.fromisoformat(event["start_time"])
    end_time = datetime.fromisoformat(event["end_time"])
    span_count = 6
    if start_time >= end_time:
        print(
            "  \033[91mWarning\033[0m: end_time be must larger than start_time")
        sys.exit()
    print("  The event opens at {0}".format(start_time))
    print("  The event ends  at {0}".format(end_time))

    print("")
    print("  Verifying inclusion proof ...")
    print("")

    url = "{0}/api/v1/inclusionproofs".format(host)
    response = requests.request("GET", url, params={
        "random_code": random_code,
    })
    if response.status_code != 200:
        print(response.text)
        sys.exit()

    inclusion_proof = json.loads(response.text)
    root_hash = inclusion_proof["root"]["root_hash"]

    verifier = MerkleVerifier()
    inclusion_proof["root"]["root_hash"] = bytes.fromhex(
        inclusion_proof["root"]["root_hash"])
    is_included = verifier.verify_leaf_hash_inclusion(
        bytes.fromhex(inclusion_proof["leaf_hash"]),  # bytes
        inclusion_proof["audit_paths"][0]["leaf_index"],
        [bytes.fromhex(p)
         for p in inclusion_proof["audit_paths"][0]["hashes"]],
        inclusion_proof["root"]
    )
    if is_included is False:
        print("The random code is not found.")
        sys.exit()

    print(
        "  \033[96mSuccess!\033[0m Merkle tree is \033[96munpredictable\033[0m because of your contribution.")

    print("")
    print("  Verifying delay functions ...")
    print("")

    print("{0}                     random_code = '{1}'       ".format(
        " "*span_count, random_code))
    print("{0}                          |                    ".format(" "*span_count))
    print("{0}                          v                    ".format(" "*span_count))
    print("{0}                     merkle_root               ".format(" "*span_count))
    print("{0}                          |                    ".format(" "*span_count))
    print("{0}                          v                    ".format(" "*span_count))

    initial_el = b"\x08" + (b"\x00" * 99)
    form_size = 100
    lambda_security_bits = 1024

    url = "{0}/api/v1/delayproofs?after={1}".format(
        host, event["start_time"].replace("+", "%2b"))
    response = requests.request("GET", url)
    if response.status_code != 200:
        print(response.text)
        sys.exit()

    delay_proofs = json.loads(response.text)

    found = False
    is_clear = False
    discriminant_challenge = ""
    root_0_status_id = 0
    seed = ""
    j = 0
    for i, proof in enumerate(delay_proofs):
        if proof["root_hash"] == root_hash:
            root_0_create_time = proof["create_time"]/1000
            root_0_status_id = proof["twitter_status_id"]
            # print("  Found proof_{0} in {1} proofs".format(i, len(delay_proofs)))
            print(
                "{0}    (result_01) <- VDF(root_01 + ..)           ".format(" "*span_count))
            print("{0}                          v                  ".format(
                " "*span_count))
            print(
                "{0}    (result_02) <- VDF(root_02 + result_01)    ".format(" "*span_count))
            print("{0}                          .                  ".format(
                " "*span_count))
            print("{0}                          .                  ".format(
                " "*span_count))
            print("{0}                          v                  ".format(
                " "*span_count))
            found = True

        if found is False:
            continue

        j += 1
        if i == 0:
            discriminant_challenge = proof["root_hash"]
        else:
            discriminant_challenge = proof["root_hash"] + \
                delay_proofs[i-1]["result"]

        discriminant_challenge = discriminant_challenge.encode()
        discriminant = create_discriminant(
            discriminant_challenge, lambda_security_bits)
        result_bytes = bytes.fromhex(proof["result"])
        is_valid = verify_wesolowski(
            str(discriminant),
            initial_el,
            result_bytes[:form_size],
            result_bytes[form_size: 2 * form_size],
            proof["t"],
        )

        if is_valid is False:
            print("proof id={0} is invalid", proof["id"])
            sys.exit()

        if datetime.timestamp(end_time) < proof["create_time"]/1000:
            is_clear = True
            seed = proof["result"]
            break

    if found is False:
        print("Corresponding delayproofs is still computing. Please wait for a moment.")
        sys.exit()

    i += 1
    print("{0}    (result_{1}) <- VDF(root_{1} + result_{2}) ".format(" "*span_count, i, i-1))
    print("{0}                          |                    ".format(" "*span_count))
    print("{0}                          v                    ".format(" "*span_count))
    print("{0}              \033[96mseed\033[0m  <- result_{1} {2}".format(
        " "*span_count, i, proof["result"]))
    print("{0}                          |                    ".format(" "*span_count))
    print("{0}                          v                    ".format(" "*span_count))
    print("\033[96m  presentation_order\033[0m <- shuffle(\033[96mseed\033[0m, original_list) ".format(i))

    if is_clear is False:
        print("")
        print("  \033[96mSuccess!\033[0m ")
        print("  ")
        print("  Some upcoming delayproofs are still computing. Please wait for a moment.")
        print(
            "  root_0   is at https://twitter.com/HeadStartRandom/status/{0}".format(root_0_status_id))
        print("  root_{0} is at https://twitter.com/HeadStartRandom/status/{1}".format(
            i, proof["twitter_status_id"]))
        sys.exit()

    original_list = list(range(1, 11))
    print("  original_list:      {0}".format(original_list))
    presentation_order = shuffle_teams(seed, original_list)
    print("  presentation_order: {0}".format(presentation_order))
    print("")
    print(
        "  \033[96mSuccess!\033[0m The result is \033[96mFAIR!\033[0m")
    print(
        "  The seed tooks more than \033[96m{0} minutes\033[0m to compute after you contributed at around {1}.".format(j, datetime.fromtimestamp(int(root_0_create_time))))
    print("  As a result, the adversaries CANNOT predict and bias the result!")
    print(
        "  Please check our paper for \033[96mMORE!\033[0m -> \033[92mhttps://www.ndss-symposium.org/ndss-paper/auto-draft-184/\033[0m")
    print("")
    print(
        "  root_0   is at https://twitter.com/HeadStartRandom/status/{0}".format(root_0_status_id))
    print("  root_{0} is at https://twitter.com/HeadStartRandom/status/{1}".format(
        i, proof["twitter_status_id"]))
