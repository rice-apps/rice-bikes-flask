from setuptools import setup

setup(
    name='rice_bikes_flask',
    packages=['rice_bikes_flask'],
    include_package_data=True,
    install_requires=[
        'postgres',
        'Flask',
        'Flask-Restless',
        'psycopg2',
        'SQLAlchemy',
        'Flask-SQLAlchemy',
    ],
)
