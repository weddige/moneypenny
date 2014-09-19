# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import sys
import os


def main():
    from moneypenny.conf import settings
    from moneypenny.core import MoneypennyDaemon

    daemon = MoneypennyDaemon(
        os.path.expanduser(settings['daemon']['pidfile']),
        os.path.expanduser(settings['logging']['file'])
    )
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('Unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        daemon.foreground()


if __name__ == '__main__':
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
    main()
