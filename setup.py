from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='pymigemo',
    version='0.0.1',
    description='Migemo implementation on Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='oguna',
    author_email='',
    url='https://github.com/oguna/pymigemo',
    license='MIT',
    test_suite='tests',
    entry_points={
        "console_scripts": [
            "pymigemo=migemo.migemo:main",
        ]
    },
    packages=['migemo'],
    package_data={
        'migemo': ['dict/migemo-compact-dict', 'dict/LICENSE']
    }
)
