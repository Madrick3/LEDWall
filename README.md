
LED Wall - XProjects Spring 2020

Written by: Patrick Flaherty, Elizabeth Gilman, Emilyn Jaros, Jack Ruzzo, Hanlan Yang

Java and Python Repository for the development of the LED wall X Project at the University of Pittsburgh.
This will be developed with two primary master branches:

	master: the standard master branch will include python programs which utilize various forms of sensing (e.g. microphones, cameras, heat) to create images. 
	These images will then be pushed to the portion of the project in the second branch
	
	JavaControl: This branch will be responsible for controlling the pixelpusher itself and will be utilized by the programs in the first master branch. 
	It will be given an image and be tasked with transliterating that image to the pixelpusher within the LEDWall
	
	As this project nears its completion these two branches will be merged into one item and provide an API for users to develop their own programs to interface with the LEDWall.
