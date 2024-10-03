from setuptools import setup, find_packages

setup(
    name="snake_multiplayer_challenge",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "snake_game=snake_game.game:main",
        ],
    },
    author="Baptiste Sauvecanne (ELYSIUM AIRCRAFT)",
    description="Multiplayer Snake Game Challenge",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
