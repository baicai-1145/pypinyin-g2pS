# pypinyin-g2pS — context-aware polyphones for pypinyin

Plug [g2pS](https://github.com/baicai-1145/g2pS) models into [pypinyin](https://github.com/mozillazg/python-pinyin) as the polyphone disambiguator. g2pS decides the ~852 polyphonic characters from sentence context; everything else falls back to pypinyin's dictionaries.

Three interchangeable inference backends:

| backend | package | deps | GPU |
|---|---|---|---|
| `numpy` | [g2pS](https://github.com/baicai-1145/g2pS) | numpy only | — |
| `onnx` | [g2pS-onnx](https://github.com/baicai-1145/g2pS-onnx) | onnxruntime(-gpu) | ✔ CUDA |
| `torch` | [g2pS-torch](https://github.com/baicai-1145/g2pS-torch) | torch | ✔ CUDA + fp16 |

## Usage

```python
from pypinyin_g2pS import G2pSPinyin

p = G2pSPinyin(backend='onnx', model_dir='models/tiny')   # any backend, any tier
p.pinyin('他在银行工作，行踪不定。')
# [['tā'], ['zài'], ['yín'], ['háng'], ['gōng'], ['zuò'], ['，'], ['xíng'], ['zōng'], ['bù'], ['dìng'], ['。']]
p.lazy_pinyin('恢复汉阳区人民政府')
# ['hui', 'fu', 'han', 'yang', 'qu', 'ren', 'min', 'zheng', 'fu']
```

`G2pSPinyin` subclasses pypinyin's `Pinyin` — styles (`Style.TONE/TONE2/TONE3/NORMAL`), `lazy_pinyin`, heteronym handling and errors behavior all work as usual.

## Install

```bash
pip install pypinyin
pip install git+https://github.com/baicai-1145/pypinyin-g2pS.git
# plus exactly one backend:
pip install git+https://github.com/baicai-1145/g2pS.git          # numpy
pip install git+https://github.com/baicai-1145/g2pS-onnx.git    # onnx (GPU)
pip install git+https://github.com/baicai-1145/g2pS-torch.git   # torch (GPU)
```

Model weights ship inside the backend repos (`models/<tier>/`). Tiers: small (16.0M, 98.49) / tiny (4.9M, 98.51) / nano (1.1M, 98.41) — see the main repo for details.
