Reporting CLI for Oracle Cloud Infrastructure Classic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

=====
About
=====

Provides a CLI to report resources deployed to an OCIC Identity Domain.


============
Installation
============

Python 2.7+ and 3.5+ are supported.

Requires the Python packages
::

    pip install configureparser, requests



============
Development
============



========
Examples
========
::
  
  python cli.py ocic_config1.txt compute
  python cli.py ocic_config1.txt storage
  python cli.py ocic_config1.txt database
  python cli.py ocic_config1.txt shapes

=============
Documentation
=============


====
Help
====

Project is maintained by David Ryder - David.Ryder@oracle.com, DavidRyder@yahoo.com

=======
Changes
=======

See `CHANGELOG`__.

__ https://github.com/DDDRYDER/OCIC-Reporting-CLI/blob/master/CHANGELOG.rst

============
Contributing
============



============
Known Issues
============




=======
License
=======

Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.

This CLI is dual licensed under the Universal Permissive License 1.0 and the Apache License 2.0.

See `LICENSE`__ for more details.

__ https://github.com/DDDRYDER/OCIC-Reporting-CLI/blob/master/LICENSE.txt
