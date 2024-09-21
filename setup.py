import setuptools

setuptools.setup(
    name='pyaradi',
    version='0.1.3',
    author='A. Purim, G. Praciano',
    url='https://github.com/AndreisPurim/ARADI',
    author_email='andreispurim@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description='ARADI encryption implementation with CTR modes',
    py_modules=['pyaradi','pyaradi.aradi_arg','pyaradi.aradi_core','pyaradi.aradi_utils','pyaradi.aradi'],
    install_requires=[
        'pycryptodome'
    ],
    entry_points={
        'console_scripts': ['pyaradi=pyaradi.aradi_arg:main']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)

