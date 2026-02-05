#!/usr/bin/env python3
"""
Setup script for NotifySend Python Client
"""

from setuptools import setup

setup(
    name='notify-send-client',
    version='1.0.0',
    description='TCP message dispatcher and desktop notification client',
    author='NotifySend Project',
    py_modules=['notify_send'],
    install_requires=[
        'plyer>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'notify_send=notify_send:main_orchestrator',
        ],
    },
    python_requires='>=3.6',
)
