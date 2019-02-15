from setuptools import setup, find_packages

setup(
    name             = 'utailBase',
    version          = '0.0.34',
    description      = 'unlimit tail basementlib',
    long_description = open('README.md').read(),
    author           = 'chase',
    author_email     = '',
    url              = 'https://...',
    download_url     = 'https://...',
    install_requires = ['pyaml'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['utail', 'base'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)