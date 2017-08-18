from setuptools import setup

setup(
    name='rice_bikes_flask',
    packages=['rice_bikes_flask'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-Restless',
        'Flask-SQLAlchemy',
        'psycopg2',
        'SQLAlchemy',
    ],
)
