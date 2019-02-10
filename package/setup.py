import os

from setuptools import setup, find_packages

setup(
   name='query_db',
   version='0.1.0',
   maintainer='Sabine Bertram',
   maintainer_email='sabine.bertram@mailbox.org',
   package_dir={'': 'src'},
   packages=find_packages('src'),
   package_data={'swagger_server': ['swagger/swagger.yaml']},

   install_requires=['connexion[swagger-ui]', 'flask_cors', 'pymongo', 'python-dotenv', 'python-jose-cryptodome'],
)
