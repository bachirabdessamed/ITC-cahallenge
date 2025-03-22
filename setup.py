from setuptools import setup, find_packages

setup(
    name='pythonsql', 
    version='1.0',
    install_requires=[
        'psycopg2-binary',
        'pandas'
        'asgiref==3.8.1',
        'Django==5.1.7',
        'psycopg2-binary==2.9.10',
        'python-http-client==3.3.7',
        'sendgrid==6.11.0',
        'sqlparse==0.5.3',
        'starkbank-ecdsa==2.2.0',
        'typing_extensions==4.12.2',         
    ], 
    
    packages=find_packages()
)
