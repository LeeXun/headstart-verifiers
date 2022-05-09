# HeadStart Verifiers

除了分組抽籤，您知道台大的選課和宿舍抽籤，其實也都可以更加地公開透明嗎？
社會中還有很多問題需要改變，從我們開始改革，邀請各位使用可驗證抽籤實現公平正義！

Aside from randomly deciding order, do you know that the course selection system and dormitory allocation in NTU could also be more transparent by adopting HeadStart?

HeadStart is a participatory randomness generation protocol that we presented at [NDSS 2022](https://www.ndss-symposium.org/ndss-paper/auto-draft-184/). People can contribute "random code" to influnce and verify the randomness is truly unpredictable and bias-resistant to ensure the fairness.

## Prerequisite

- python3 (tested in 3.9.12)

```sh
pip install -r ./requirements.txt
python ./verify_presentation_order_cns2022.py "your_random_code"
```

Paper links:
- https://yihchun.com/papers/ndss22.pdf
- https://www.ndss-symposium.org/ndss-paper/auto-draft-184/
