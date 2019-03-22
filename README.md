# REST client for the UW Person Web Service

[![Build Status](https://api.travis-ci.org/uw-it-aca/uw-restclients-pws.svg?branch=master)](https://travis-ci.org/uw-it-aca/uw-restclients-pws)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/uw-restclients-pws/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/uw-restclients-pws?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-pws.svg)](https://pypi.python.org/pypi/uw-restclients-pws)
![Python versions](https://img.shields.io/pypi/pyversions/uw-restclients-pws.svg)

Installation:

    pip install UW-RestClients-PWS

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_PWS_DAO_CLASS='Live'

    # Paths to UWCA cert and key files
    RESTCLIENTS_PWS_CERT_FILE='/path/to/cert'
    RESTCLIENTS_PWS_KEY_FILE='/path/to/key'

    # Person Web Service hostname (eval or production)
    RESTCLIENTS_PWS_HOST='https://ws.admin.washington.edu'

Optional settings:

    # Customizable parameters for urllib3
    RESTCLIENTS_PWS_TIMEOUT=5
    RESTCLIENTS_PWS_POOL_SIZE=10

See examples for usage.  Pull requests welcome.
