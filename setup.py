from setuptools import setup, find_packages

setup(
    name='urlfwd',
    version='0.3.0',
    py_modules=['urlfwd','urlfwd.genpage','urlfwd.manage_links',
                'urlfwd.cli','urlfwd.assets'],
    install_requires=[
        'Click', 'pyyaml','qrcode','Pillow'
    ],
    packages=find_packages(where=".", exclude=["tests*", "docs*"]),
    author='Sarah M Brown',
    entry_points={
        'console_scripts': [
            'urlfwd = urlfwd.cli:urlfwd_cli',
            # 'genqrs = urlfwd.cli:generate_qrs',
            # 'addlink = urlfwd.cli:add_short_link',
        ],
    },
    include_package_data=True,
    package_dir={'': '.'},
    package_data={"urlfwd": ["assets/*.md", "*.rst"]}
)