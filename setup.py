from setuptools import setup, find_packages

def requires():
    with open("requirements.txt", encoding="utf-16-le") as f:
        lst = f.read().splitlines()
        if lst and lst[0].startswith('\ufeff'):
            lst[0] = lst[0][1:]
        return lst

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
    name='chiefpay',
    version='1.2.0',
    packages=find_packages(),
    install_requires=requires(),
    author='nelsn',
    author_email='egor.larrr@gmail.com',
    description='ChiefPay Python SDK',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ChiefPay/ChiefPay.py',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)