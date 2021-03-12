import os
from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
# sudo vim /etc/profile.d/djproj.sh # en ubuntu
# export DJPROJ=dev
if os.environ['DJPROJ'] == 'prod':
    from .prod import *
else:
    from .dev import *
