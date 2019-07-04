from setuptools import setup
import json


with open('metadata.json') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_mitterhoferbena',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_mitterhoferbena'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'mitterhoferbena=lexibank_mitterhoferbena:Dataset',
        ]
    },
    install_requires=[
        'pylexibank==1.1.1',
        'segments==2.0.2'
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)

