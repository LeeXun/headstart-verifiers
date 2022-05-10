# HeadStart Verifiers

<img width="421" alt="image" src="https://user-images.githubusercontent.com/12629194/167590726-25e55d5e-35b1-4eaf-b75b-e0d70f12ce1d.png">

安全的隨機抽籤，是確保沒有任何人能夠預知、控制結果。除了分組抽籤，您知道台大的選課和宿舍抽籤，其實也都可以更加地公開透明嗎？
社會中還有很多問題需要改變，從我們開始改革，邀請各位使用可驗證抽籤實現公平正義！

Secure randomness should be unpredictable, bias-resistant and verifiable.
Aside from randomly deciding order, do you know that the course selection system and dormitory allocation in NTU could also be more transparent by adopting HeadStart?

HeadStart is a participatory randomness generation protocol that we presented at [NDSS 2022](https://www.ndss-symposium.org/ndss-paper/auto-draft-184/). People can contribute "random code" to influnce and verify the randomness is truly unpredictable and bias-resistant to ensure the fairness.

## Prerequisite

- python3 (tested in 3.9.12)

```sh
pip install -r ./requirements.txt
```

Or you can run by [Docker](https://docs.docker.com/get-docker/).

```sh
docker-compose -f ./docker-compose.yml up
```

## How to verify

```sh
python ./verify_presentation_order_cns2022.py "your_random_code"
```

This script will verify:
1. Your random_code is included in the Merkle tree to make the tree root "unpredictable".
2. The "unpredictable" root is in the verifiable delay functions (VDFs) to make the result seed "bias-resistant".

## Our Paper
For more details, please refer to our paper:
- https://www.ndss-symposium.org/ndss-paper/auto-draft-184/
