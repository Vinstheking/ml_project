from setuptools import find_packages,setup
from typing import List

hypen_e_symbol='-e .'
def get_requirements(fle_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(fle_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n",'') for req in requirements]
        if hypen_e_symbol in requirements:
            requirements.remove(hypen_e_symbol)
    return requirements






setup(
name='mlproject',
version='0.0.1',
author='Vins',
author_email='vinaysvinays456@gmail.com',
packages=find_packages(),
# install_requires=['pandas','numpy','seaborn']
install_requires=get_requirements('requirements.txt')
)