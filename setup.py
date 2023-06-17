from setuptools import setup, find_packages

setup(
    name='CallingGPT',
    version='0.0.0.2',
    description="GPT's function calling feature wrapper",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'openai',
    ],
    author='RockChinQ',
    author_email="1010553892@qq.com",
    url="https://github.com/RockChinQ/CallingGPT",
    classifiers=[
        'Programming Language :: Python :: 3',
        # Apache License 2.0
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    # only path CallingGPT
    package_dir={'': 'CallingGPT'},
    packages=find_packages('CallingGPT'),
)