#!/usr/bin/env python
import os
import sys
from auto_install.settings import server_ip,content_ip
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto_install.settings")
    
    if not server_ip and not content_ip:
        print "server ip or content ip is empty in settings.py!!"
        sys.exit(211)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
