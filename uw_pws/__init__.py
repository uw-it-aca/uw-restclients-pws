"""
This is the interface for interacting with the Person Web Service.
"""

from restclients_core.exceptions import (InvalidRegID, InvalidNetID,
                                         InvalidEmployeeID,
                                         DataFailureException)
from uw_pws.exceptions import (InvalidStudentNumber, InvalidIdCardPhotoSize,
                               InvalidProxRFID)
from uw_pws.dao import PWS_DAO
from uw_pws.models import Person, Entity
try:
    from io import BytesIO as streamIO
    from urllib.parse import urlencode
except ImportError:
    from StringIO import StringIO as streamIO
    from urllib import urlencode
import json
import re


PERSON_PREFIX = '/identity/v1/person'
ENTITY_PREFIX = '/identity/v1/entity'
CARD_PREFIX = '/idcard/v1/card'
DAO = PWS_DAO()


class PWS(object):
    """
    The PWS object has methods for getting person information.
    """
    def __init__(self, actas=None):
        self.actas = actas
        self._re_regid = re.compile(r'^[A-F0-9]{32}$', re.I)
        self._re_personal_netid = re.compile(r'^[a-z][_a-z0-9]{0,14}$', re.I)
        self._re_admin_netid = re.compile(r'^[a-z]adm_[a-z][a-z0-9]{0,14}$',
                                          re.I)
        self._re_application_netid = re.compile(r'^a_[a-z0-9\-\_\.$.]{1,18}$',
                                                re.I)
        self._re_employee_id = re.compile(r'^\d{9}$')
        self._re_student_number = re.compile(r'^\d{7}$')
        self._re_prox_rfid = re.compile(r'^\d{16}$')

    def get_person_by_regid(self, regid):
        """
        Returns a restclients.Person object for the given regid.  If the
        regid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        url = "%s/%s/full.json" % (PERSON_PREFIX, regid.upper())
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._person_from_json(response.data)

    def get_person_by_netid(self, netid):
        """
        Returns a restclients.Person object for the given netid.  If the
        netid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        url = "%s/%s/full.json" % (PERSON_PREFIX, netid.lower())
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._person_from_json(response.data)

    def get_person_by_employee_id(self, employee_id):
        """
        Returns a restclients.Person object for the given employee id.  If the
        employee id isn't found, or if there is an error communicating with the
        PWS, a DataFailureException will be thrown.
        """
        if not self.valid_employee_id(employee_id):
            raise InvalidEmployeeID(employee_id)

        url = "%s.json?%s" % (PERSON_PREFIX,
                              urlencode({"employee_id": employee_id}))
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        # Search does not return a full person resource
        data = json.loads(response.data)
        if not len(data["Persons"]):
            raise DataFailureException(url, 404, "No person found")

        regid = data["Persons"][0]["PersonURI"]["UWRegID"]
        return self.get_person_by_regid(regid)

    def get_person_by_student_number(self, student_number):
        """
        Returns a restclients.Person object for the given student number.  If
        the student number isn't found, or if there is an error communicating
        with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_student_number(student_number):
            raise InvalidStudentNumber(student_number)

        url = "%s.json?%s" % (PERSON_PREFIX,
                              urlencode({"student_number": student_number}))
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        # Search does not return a full person resource
        data = json.loads(response.data)
        if not len(data["Persons"]):
            raise DataFailureException(url, 404, "No person found")

        regid = data["Persons"][0]["PersonURI"]["UWRegID"]
        return self.get_person_by_regid(regid)

    def get_person_by_prox_rfid(self, prox_rfid):
        """
        Returns a restclients.Person object for the given rfid.  If the rfid
        isn't found, or if there is an error communicating with the IdCard WS,
        a DataFailureException will be thrown.
        """
        if not self.valid_prox_rfid(prox_rfid):
            raise InvalidProxRFID(prox_rfid)

        url = "%s.json?%s" % (CARD_PREFIX,
                              urlencode({"prox_rfid": prox_rfid}))
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)
        if not len(data["Cards"]):
            raise DataFailureException(url, 404, "No card found")

        regid = data["Cards"][0]["RegID"]
        return self.get_person_by_regid(regid)

    def get_entity_by_regid(self, regid):
        """
        Returns a restclients.Entity object for the given regid.  If the
        regid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        url = "%s/%s.json" % (ENTITY_PREFIX, regid.upper())
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._entity_from_json(response.data)

    def get_entity_by_netid(self, netid):
        """
        Returns a restclients.Entity object for the given netid.  If the
        netid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        url = "%s/%s.json" % (ENTITY_PREFIX, netid.lower())
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._entity_from_json(response.data)

    def get_contact(self, regid):
        """
        Returns data for the given regid.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        url = "%s/%s/full.json" % (PERSON_PREFIX, regid.upper())
        response = DAO.getURL(url, {"Accept": "application/json"})

        if response.status == 404:
            return

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def get_idcard_photo(self, regid, size="medium"):
        """
        Returns a jpeg image, for the passed uwregid. Size is configured as:
            "small" (20w x 25h px),
            "medium" (120w x 150h px),
            "large" (240w x 300h px),
            {height in pixels} (custom height, default aspect ratio)
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        size = str(size)
        if (not re.match(r"(?:small|medium|large)$", size) and
                not re.match(r"[1-9]\d{1,3}$", size)):
            raise InvalidIdCardPhotoSize(size)

        url = "/idcard/v1/photo/%s-%s.jpg" % (regid.upper(), size)

        headers = {"Accept": "image/jpeg"}

        if self.actas is not None:
            if not self.valid_uwnetid(self.actas):
                raise InvalidNetID(self.actas)
            headers["X-UW-Act-as"] = self.actas

        response = DAO.getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return streamIO(response.data)

    def valid_uwnetid(self, netid):
        uwnetid = str(netid)
        return (self._re_personal_netid.match(uwnetid) is not None or
                self._re_admin_netid.match(uwnetid) is not None or
                self._re_application_netid.match(uwnetid) is not None)

    def valid_uwregid(self, regid):
        return True if self._re_regid.match(str(regid)) else False

    def valid_employee_id(self, employee_id):
        return True if self._re_employee_id.match(str(employee_id)) else False

    def valid_student_number(self, student_number):
        return True if (
            self._re_student_number.match(str(student_number))) else False

    def valid_prox_rfid(self, prox_rfid):
        return True if self._re_prox_rfid.match(str(prox_rfid)) else False

    def _person_from_json(self, data):
        """
        Internal method, for creating the Person object.
        """
        person_data = json.loads(data)
        person = Person.from_json(person_data)

        return person

    def _entity_from_json(self, data):
        entity_data = json.loads(data)
        entity = Entity()
        entity.uwnetid = entity_data["UWNetID"]
        entity.uwregid = entity_data["UWRegID"]
        entity.display_name = entity_data["DisplayName"]

        return entity
