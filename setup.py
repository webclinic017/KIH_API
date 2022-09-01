from setuptools import setup

setup(
    name='KIH API',
    version='1.1',
    url='https://github.com/Kontinuum-Investment-Holdings/KIH_API',
    author='Kavindu Athaudha',
    author_email='kavindu@k-ih.co.uk',
    packages=['kih-api'],
    install_requires=[
        "requests",
        "urllib3",
        "pytz",
        "python-dateutil",
        "pandas",
        "numpy",
        "ibapi",
        "validators",
        "dacite",
        "mongoengine",
        "pymongo",
        "dataclass_csv"
    ]
)
