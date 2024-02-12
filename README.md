# REST client for the UW Person Web Service

[![Build Status](https://github.com/uw-it-aca/uw-restclients-pws/workflows/tests/badge.svg?branch=main)](https://github.com/uw-it-aca/uw-restclients-pws/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/uw-restclients-pws/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/uw-restclients-pws?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-pws.svg)](https://pypi.python.org/pypi/uw-restclients-pws)
![Python versions](https://img.shields.io/badge/python-3.10-blue.svg)

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

How to use this client:

    from commonconf.backends import use_configparser_backend                        
    from commonconf import settings
    from uw_pws import PWS
    import os
    
    
    if __name__ == '__main__':
        settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     'settings.cfg')
        use_configparser_backend(settings_path, 'PWS')
        
        client = PWS()
        person1 = client.get_person_by_netid('javerage')
        person2 = client.get_person_by_regid('12345678901234567890123456789012')
        person3 = client.get_person_by_student_number('1234567')
    
