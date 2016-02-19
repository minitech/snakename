from setuptools import setup

setup(
    name="snakename",
    version="1.0.0",
    packages=["snakename"],
    install_requires=[
        "Flask>=0.10.1",
        "SQLAlchemy>=1.0.12",
    ],
    author="Ryan O’Hara",
    author_email="ryan@ohara.me",
    description="A web app to suggest snake names.",
    license="ISC",
    keywords="snake",
)
