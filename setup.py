from setuptools import setup

setup(
    name='Minetester',
    version='0.0.1',
    description='Complex environments based on Minetest.',
    author='EleutherAI',
    author_email='',
    packages=['minetester'],
    install_requires=[
        'opencv-python',
        'gym',
        'numpy',
        'matplotlib',
        'zmq',
        'protobuf==3.20.1',
        'psutil',
    ],
)
