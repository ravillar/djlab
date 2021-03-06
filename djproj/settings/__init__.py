import os
from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
# sudo vim /etc/profile.d/djproj.sh # en ubuntu
# export DJPROJ=dev
#comentado por las dudas hasta que funcione bien jeje
# if os.environ['DJPROJ'] == 'prod':
    # from .prod import *
# else:
    # from .dev import *
from .dev import *
