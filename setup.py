from distutils.core import setup

setup(
  name='streamslib',
  packages=['streamslib'],
  version='0.1',
  license='MIT',
  description='Library to interact with streamsapp.io',
  author='Howard Paget',
  author_email='contact@streamsapp.io',
  url='https://github.com/streamsapp/streamslib',
  download_url='https://github.com/streamsapp/streamslib/archive/v_01.tar.gz',
  keywords=['STREAMSAPP.IO'],
  install_requires=['requests', 'datetime'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)