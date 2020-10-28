import setuptools

# with open('README.md', 'r') as rf:
#     long_description = rf.read()
#

setuptools.setup(
    name='filedict',
    version="0.1b",
    author='n0x1s',
    author_email='n0x1s0x01@gmail.com',
    url='https://github.com/n0x1s/filedict',
    description='Dict like file',
    license='MIT',
    # long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer='n0x1s',
    maintainer_email='n0x1s0x01@gmail.com',
    packages=['filedict'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    python_requires='>=3'
)
