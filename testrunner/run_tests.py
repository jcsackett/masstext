import sys

from django.core import management

import test_settings

sys.path += ['..', '.']
management.setup_environ(test_settings)

if __name__=="__main__":
    management.call_command('test', 'masstext')
