"""pypinyin-g2pS: use g2pS models as the polyphone disambiguator inside pypinyin.

Backends:
  - 'numpy' : g2ps       (baicai-1145/g2pS)        — zero heavy deps
  - 'onnx'  : g2ps_onnx  (baicai-1145/g2pS-onnx)   — onnxruntime, GPU-capable
  - 'torch' : g2ps_torch (baicai-1145/g2pS-torch)  — PyTorch, GPU-capable

g2pS decides polyphonic characters; monophonic chars fall back to pypinyin's dictionaries.
"""
from pypinyin import Style
from pypinyin.core import Pinyin
from pypinyin.contrib.tone_convert import to_normal, to_tone, to_tone2, to_tone3
from pypinyin.converter import UltimateConverter

_ENGINES = {
    'numpy': ('g2ps', 'G2pS'),
    'onnx': ('g2ps_onnx', 'G2pS'),
    'torch': ('g2ps_torch', 'G2pS'),
}


def load_engine(backend, model_dir, tier=None, **engine_kwargs):
    if backend not in _ENGINES:
        raise ValueError(f"backend must be one of {list(_ENGINES)}, got {backend!r}")
    mod_name, cls_name = _ENGINES[backend]
    try:
        mod = importlib.import_module(mod_name)
    except ImportError as e:
        raise ImportError(
            f"backend {backend!r} needs the {mod_name} package "
            f"(github.com/baicai-1145/{'g2pS' if backend == 'numpy' else mod_name.replace('_', '-')})") from e
    G2pS = getattr(mod, cls_name)
    return G2pS(model_dir, tier=tier, **engine_kwargs) if tier else G2pS(model_dir, **engine_kwargs)


import importlib  # noqa: E402  (kept close to use site)


def _styled(py_num, style):
    py_num = py_num.replace('u:', 'v')          # g2pS ü convention -> pypinyin v
    if style == Style.TONE:
        return to_tone(py_num)
    if style == Style.TONE2:
        return to_tone2(py_num)
    if style == Style.TONE3:
        return to_tone3(py_num)
    if style == Style.NORMAL:
        return to_normal(py_num)
    return to_tone(py_num)


class _Converter(UltimateConverter):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self._engine = engine

    def _to_pinyin(self, han, style=None, heteronym=False, errors='default',
                   strict=True, **kwargs):
        style = style if style is not None else self.style
        _, pairs = self._engine.convert(han)
        out = []
        for ch, py in pairs:
            if py is None:
                # not a g2pS polyphone: pypinyin dictionary decides
                out.extend(super().convert(ch, style=style, heteronym=heteronym,
                                           errors=errors, strict=strict, **kwargs))
            else:
                out.append([_styled(py, style)])
        return out


class G2pSPinyin(Pinyin):
    """drop-in pypinyin engine backed by g2pS.

    p = G2pSPinyin(backend='onnx', model_dir='models/tiny')
    p.pinyin('他在银行工作，行踪不定。')
    """

    def __init__(self, backend='numpy', model_dir=None, tier=None,
                 style=Style.TONE, **kwargs):
        engine_kwargs = {}
        if tier:
            engine_kwargs['tier'] = tier
        self._engine = load_engine(backend, model_dir, **engine_kwargs)
        self._converter = _Converter(self._engine, style=style, **kwargs)
        super().__init__(style=style, **kwargs)


__all__ = ['G2pSPinyin', 'load_engine']
