from setuptools import setup, find_packages

setup(
    name='autoclicker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Liste les dépendances ici, par exemple:
        # 'requests', 'flask',
    ],
    entry_points={
        'console_scripts': [
            'run_project=autoclicker.main:main',  # Commande pour exécuter ton projet
        ],
    }
)
