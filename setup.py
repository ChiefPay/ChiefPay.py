from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
    name='chiefpay',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0,<3.0.0',
        'aiohttp>=3.8.0,<4.0.0',
        'python-socketio[client]>=5.1.0,<6.0.0',
        'pydantic>=2.0.0,<3.0.0',
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