from setuptools import setup

setup(
    name='urlfwd',
    version='0.0.3',
    py_modules=['urlfwd','urlfwd.genpage','urlfwd.manage_links',
                'urlfwd.cli'
                ],
    install_requires=[
        'Click', 'pyyaml','qrcode'
    ],
    entry_points={
        'console_scripts': [
            'genlinks = urlfwd.cli:generate_links',
            'genqrs = urlfwd.cli:generate_qrs',
            'addlink = urlfwd.cli:add_short_link',
        ],
    },
)