from setuptools import setup

setup(
    name='urlfwd',
    version='0.1.0',
    py_modules=['urlfwd','urlfwd.genpage','urlfwd.manage_links',
                'urlfwd.cli','urlfwd.assets'],
    install_requires=[
        'Click', 'pyyaml','qrcode','Pillow'
    ],
    entry_points={
        'console_scripts': [
            'urlfwd = urlfwd.cli:urlfwd_cli',
            # 'genqrs = urlfwd.cli:generate_qrs',
            # 'addlink = urlfwd.cli:add_short_link',
        ],
    },
)