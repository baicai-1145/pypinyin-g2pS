from setuptools import setup

setup(
    name='pypinyin-g2pS',
    version='0.1.0',
    description='Context-aware Mandarin polyphone disambiguation for pypinyin, backed by g2pS models (numpy/onnx/torch backends)',
    packages=['pypinyin_g2pS'],
    install_requires=['pypinyin>=0.49'],
    python_requires='>=3.8',
)
