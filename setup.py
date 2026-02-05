from setuptools import setup

setup(
    name='banana-pancake-redistributor',
    version='1.0.0',
    description='Culinary streaming pipeline for message distribution',
    py_modules=['notify_send'],
    install_requires=['plyer>=2.0.0'],
    entry_points={
        'console_scripts': [
            'notify_send=notify_send:blend_smoothie',
        ],
    },
    python_requires='>=3.6',
)
