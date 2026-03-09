from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
    name='chiefpay',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'aiohappyeyeballs==2.6.1',
        'aiohttp==3.13.3',
        'aiosignal==1.4.0',
        'annotated-types==0.7.0',
        'attrs==25.3.0',
        'bidict==0.23.1',
        'certifi==2025.6.15',
        'charset-normalizer==3.4.2',
        'frozenlist==1.7.0',
        'h11==0.16.0',
        'idna==3.10',
        'multidict==6.6.2',
        'pip_system_certs==5.3',
        'propcache==0.3.2',
        'pydantic==2.11.7',
        'pydantic_core==2.33.2',
        'python-engineio==4.12.2',
        'python-socketio==5.14.0',
        'requests==2.32.4',
        'simple-websocket==1.1.0',
        'typing-inspection==0.4.1',
        'typing_extensions==4.14.0',
        'urllib3==2.6.3',
        'websocket-client==1.8.0',
        'wsproto==1.2.0',
        'yarl==1.20.1',
    ],
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