from setuptools import setup, find_packages

setup(
  name='bojango',
  version='1.1.19',
  description='A lightweight framework for creating Telegram bots with advanced routing and localization.',
  long_description=open('README.md', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author='Mironov Daniil',
  author_email='hugantmirron@gmail.com',
  url='https://github.com/hugant/bojango',
  packages=find_packages(exclude=['tests*', '*.env']),
  include_package_data=True,
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
  python_requires='>=3.9',
  install_requires=[
    'python-telegram-bot>=20.0',
    'aiologger>=0.6.1',
    'aiofiles>=23.1.0',
    'polib>=1.1.1',
  ],
)
