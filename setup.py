from setuptools import setup

setup(
	name='gym_openmaze',
	version='0.0.1',
	install_requires=['gym','numpy'],
	packages=['gym_openmaze','gym_openmaze.envs']
)

