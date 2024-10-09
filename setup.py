from setuptools import find_packages, setup

setup(
    name="MCQ Generator",
    version="0.0.1",
    author="Muhammad Usman Akram",
    author_email="m.usman.akram021@gmail.com",
    install_requires=[
        "openai",
        "langchain",  # Corrected typo here
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)
