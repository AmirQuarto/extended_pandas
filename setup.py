from setuptools import setup, find_packages

setup(
    name='augmented_pandas',  # Replace with your library name
    version='0.1.0',  # Initial version
    author='Amir',
    author_email='your.email@example.com',
    description='A short description of your library',
    long_description_content_type='text/markdown',
    url='https://github.com/AmirQuarto/extended_pandas',  # Optional: GitHub or docs link
    packages=find_packages(),
    install_requires=['xlwings', 'pandas', 'numpy', 'pyperclip'
        # List your dependencies here
        # e.g. 'requests>=2.25.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change if using another license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
