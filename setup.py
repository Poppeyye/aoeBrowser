from setuptools import setup, find_packages

setup(
    name='aoeBrowser',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'discord==2.3.2',
        'selenium==4.11.2',
    ],
    entry_points={
        'console_scripts': [
            'aoeBrowser = discord_bot.run_bot:main'
        ]
    },
)
