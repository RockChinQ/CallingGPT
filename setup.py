from setuptools import setup, find_namespace_packages

setup(
    name='CallingGPT',
    version='0.0.1.0',
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
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    # only path CallingGPT
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    py_modules=["CallingGPT"],
)