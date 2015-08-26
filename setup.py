import setuptools

setuptools.setup(name='py-polymer',
                 version='0.0.1',
                 description='A manager that quickly creates an easy way custom element with Polymer',
                 long_description=open('README.md').read().strip(),
                 author='Horacio Ibrahim',
                 author_email='horacioibrahim@gmail.com',
                 url='https://github.com/horacioibrahim/py-polymer',
                 py_modules=['pyPolymer'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 scripts=[
                    'scripts/install.sh'
                 ],
                 keywords='polymer custom element seed-element generator',
                 classifiers= [
                    'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.7',
                    'Topic :: Software Development :: Libraries :: Python Modules'
                ]
)
