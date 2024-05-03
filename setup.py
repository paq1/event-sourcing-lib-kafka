from setuptools import setup, find_packages

setup(
    name='event-sourcing-lib-kafka',
    packages=find_packages(include=['event_sourcing']),
    version='0.1.0',
    description='Kafka event sourcing library',
    author='MKD',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)