Moneypenny
==========

Moneypenny is a simple and extensible XMPP bot. It was intended as my personal playground and contains a mess of
half-baked ideas.

This is an condensed version of the core functionality. Although I provide this code "as is", without any support, I
accept bug reports or suggestions gladly.

Requirements
------------ 

 * git+git://github.com/weddige/pyaiml3.git#egg=PyAIML
 * SQLAlchemy
 * adventure
 * dnspython3
 * psutil
 * python-seth
 * sleekxmpp

Installation
------------

Make::

    pip install git+https://github.com/weddige/moneypenny.git

and create ~/.moneypenny/config::

    [daemon]
    pidfile=~/.moneypenny/moneypenny.pid
    [moneypenny]
    user=MONEYPENNY@SERVER.TLD
    password=PASSWORD
    admin=YOU@SERVER.TLD
    [database]
    url=sqlite:////~/.moneypenny/local.db
    [logging]
    level=INFO
    file=~/.moneypenny/moneypenny.log
    [textadventure]
    file=~/.moneypenny/sessiondata/{0}.savegame
    [conversation]
    file=~/.moneypenny/sessiondata/{0}.conversation

You can start moneypenny with::

    moneypenny START

To stop ist run::

    moneypenny STOP

Have fun!
