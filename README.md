# columbia_micromono
A comparison between microservices and monolithic architectures

Author: Phil Park
UNI: pwp2106

# Instructions
After cloning, make sure the packages listed in requirements.txt are installed in your environment. 

There are 2 directories: microservices/ and monolithic/. Each has its own respective application that can be run by cd-ing into the directory and by running "python microservices.py" or "python monolith.py" depending on the app. 

The microservices app will also require the message and user controllers to be spun up as well. They are found within the models/ directory under the microservices folder. They are run by "python message_controller.py" and "python user_controller.py"

The monolithic app depends on a local database to be generated. This can be done by running a python shell within the directory and running:
  from monolith import db
  db.create_all()

This will create a sqlite db file in /tmp

Once all the python applications are running, they can be accessed through a browser. The monolithic app is accessible through 127.0.0.1:5000 and the microservices app is accessible through 127.0.0.1:5555. If you wish to access the model controllers they are found at ports 6000 and 7000. 


