#!/bin/bash

#----------------------------------------------
# Note that this is the standard way of doing 
# things in Python 3.6. Earlier versions used
# virtulalenv. It is best to convert to 3.6
# before you do anything else. 
# Note that the default Python version in 
# the AWS Ubuntu is 3.5 at the moment. You
# will need to upgrade the the new version 
# if you wish to use this environment in 
# AWS
#----------------------------------------------
python3.6 -m venv env

# this is for bash. Activate
# it differently for different shells
#--------------------------------------
source env/bin/activate 

pip3.6 install --upgrade pip

if [ -e requirements.txt ]; then

    pip3.6 install -r requirements.txt

else

    pip3.6 install pytest
    pip3.6 install pytest-cov
    pip3.6 install sphinx
    pip3.6 install sphinx_rtd_theme

    # Logging into logstash
    pip3.6 install python-logstash

    # networkX for graphics
    pip3.6 install networkx
    pip3.6 install pydot # dot layout
    
    # Utilities
    pip3.6 install ipython
    pip3.6 install tqdm

    # scientific libraries
    pip3.6 install numpy
    pip3.6 install scipy
    pip3.6 install pandas

    # database stuff
    pip3.6 install psycopg2-binary

    # Charting libraries
    pip3.6 install matplotlib
    
    pip3.6 freeze > requirements.txt

fi

deactivate