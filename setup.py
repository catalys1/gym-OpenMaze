from setuptools import setup

setup(
	name='gym_openmaze',
	version='0.1.0',
	url='https://github.com/catalys1/gym-openmaze',
	install_requires=['gym','numpy','pygame'],
	packages=['gym_openmaze','gym_openmaze.envs']
)

