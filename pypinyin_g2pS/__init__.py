"""pypinyin-g2pS: g2pS-backed polyphone disambiguation for pypinyin."""
from .adapter import G2pSPinyin, load_engine

__all__ = ['G2pSPinyin', 'load_engine']
