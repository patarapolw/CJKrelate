from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CJKrelate',  # Required
    version='0.1.2',  # Required
    description='Generate related Hanzi/Kanji by various means. Visually. Also, a summary table is humanly made.',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/patarapolw/CJKrelate',  # Optional
    author='Pacharapol Withayasakpunt',  # Optional
    author_email='patarapolw@gmail.com',  # Optional
    keywords='CJK chinese japanese hanzi kanji',  # Optional
    packages=find_packages(exclude=['automate', 'manual', 'test']),  # Required
    install_requires=['pillow', 'PyYAML'],  # Optional
    python_requires='>=3.5',
    extras_require={  # Optional
        'tests': ['pytest'],
    },
    package_data={  # Optional
        'CJKrelate': ['database', 'font'],
    },
    include_package_date=True,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Cantonese',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],
)
