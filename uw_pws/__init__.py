# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with the Person Web Service.
"""

import json
import re
from io import BytesIO as streamIO
from urllib.parse import urlencode

from restclients_core.exceptions import (
    DataFailureException,
    InvalidEmployeeID,
    InvalidNetID,
    InvalidRegID,
)

from uw_pws.dao import PWS_DAO
from uw_pws.exceptions import (
    InvalidIdCardPhotoSize,
    InvalidProxRFID,
    InvalidStudentNumber,
)
from uw_pws.exceptions import (
    InvalidStudentSystemKey as InvalidStudentSystemKey,
)
from uw_pws.models import Entity, Person

PERSON_PREFIX = '/identity/v2/person'
ENTITY_PREFIX = '/identity/v2/entity'
CARD_PREFIX = '/idcard/v1/card'
PHOTO_PREFIX = '/idcard/v1/photo'


class PWS:
    """
    The PWS object has methods for getting person information.
    """
    def __init__(self, actas=None):
        self.actas = actas
        # netid format:
        #     https://wiki.cac.washington.edu/display/SMW/UW+NetID+Namespace
        self._re_netid = re.compile(r'^[a-z][a-z0-9\-\_\.]{,127}$', re.IGNORECASE)
        self._re_regid = re.compile(r'^[A-F0-9]{32}$', re.IGNORECASE)
        self._re_employee_id = re.compile(r'^\d{9}$')
        self._re_student_number = re.compile(r'^\d{7}$')
        self._re_student_system_key = re.compile(r'^\d{9}$')
        self._re_prox_rfid = re.compile(r'^\d{16}$')
        self.dao = PWS_DAO()

    def get_person_by_regid(self, regid):
        """
        Returns a restclients.Person object for the given regid.  If the
        regid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        url = f"{PERSON_PREFIX}/{regid.upper()}/full.json"
        return Person.from_json(self._get_resource(url))

    def get_person_by_netid(self, netid):
        """
        Returns a restclients.Person object for the given netid.  If the
        netid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        url = f"{PERSON_PREFIX}/{netid.lower()}/full.json"
        return Person.from_json(self._get_resource(url))

    def get_person_by_employee_id(self, employee_id):
        """
        Returns a restclients.Person object for the given employee id.  If the
        employee id isn't found, or if there is an error communicating with the
        PWS, a DataFailureException will be thrown.
        """
        if not self.valid_employee_id(employee_id):
            raise InvalidEmployeeID(employee_id)

        url = f"{PERSON_PREFIX}.json?{urlencode({'employee_id': employee_id})}&verbose=on"
        data = self._get_resource(url)

        # Search does not return a full person resource
        if not len(data["Persons"]):
            raise DataFailureException(url, 404, "No person found")
        return Person.from_json(data["Persons"][0])

    def get_person_by_student_number(self, student_number):
        """
        Returns a restclients.Person object for the given student number.  If
        the student number isn't found, or if there is an error communicating
        with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_student_number(student_number):
            raise InvalidStudentNumber(student_number)

        url = f"{PERSON_PREFIX}.json?{urlencode({'student_number': student_number})}&verbose=on"
        data = self._get_resource(url)

        # Search does not return a full person resource
        if not len(data["Persons"]):
            raise DataFailureException(url, 404, "No person found")

        return Person.from_json(data["Persons"][0])

    def person_search(self, **kwargs):
        """
        Returns a list of Person objects
        Parameters can be:
        uwregid=UWRegId
        uwnetid=UWNetId
        employee_id=EmployeeId
        student_number=StudentNumber
        student_system_key=StudentSystemKey
        development_id=DevelopmentId
        edupersonaffiliation_student={true/false}
        edupersonaffiliation_staff={true/false}
        edupersonaffiliation_faculty={true/false}
        edupersonaffiliation_employee={true/false}
        edupersonaffiliation_member={true/false}
        edupersonaffiliation_alum={true/false}
        edupersonaffiliation_affiliate={true/false}
        changed_since_date=YYYY-MM-DD+hh:mm:ss (5 minutes ago up to 24 hours)
        last_name=LastName
        first_name=FirstName
        registered_surname=
        registered_first_middle_name=
        phone_number=
        mail_stop=
        home_dept=
        department=
        address=
        title=
        email=
        page_start=
        """
        # Boolean params must be lowercased
        params = [(k, str(v).lower() if isinstance(v, bool) else v) for (
            k, v) in kwargs.items()]
        url = f"{PERSON_PREFIX}.json?{urlencode(params)}&page_size=250&verbose=on"

        persons = []

        while True:
            data = self._get_resource(url)

            if len(data["Persons"]) > 0:
                for person_data in data.get("Persons"):
                    persons.append(Person.from_json(person_data))

            if data.get("Next") is not None and len(data["Next"]["Href"]) > 0:
                url = data["Next"]["Href"]
            else:
                break
        return persons

    def get_person_by_prox_rfid(self, prox_rfid):
        """
        Returns a restclients.Person object for the given rfid.  If the rfid
        isn't found, or if there is an error communicating with the IdCard WS,
        a DataFailureException will be thrown.
        """
        if not self.valid_prox_rfid(prox_rfid):
            raise InvalidProxRFID(prox_rfid)

        url = f"{CARD_PREFIX}.json?{urlencode({'prox_rfid': prox_rfid})}"
        data = self._get_resource(url)
        if not len(data["Cards"]):
            raise DataFailureException(url, 404, "No card found")

        regid = data["Cards"][0]["RegID"]
        return self.get_person_by_regid(regid)

    def entity_search(self, **kwargs):
        """
        Returns a list of Person objects
        Parameters can be:
        display_name=
        is_test_entity={true/false}
        changed_since_date=YYYY-MM-DD+hh:mm:ss (5 minutes ago up to 24 hours)
        """
        # Boolean params must be lowercased
        params = [(k, str(v).lower() if isinstance(v, bool) else v) for (
            k, v) in kwargs.items()]
        url = f"{ENTITY_PREFIX}.json?{urlencode(params)}&page_size=250"

        entities = []

        while True:
            data = self._get_resource(url)

            if len(data["Entities"]) > 0:
                for result_data in data.get("Entities"):
                    uwnetid = result_data.get("UWNetID")
                    if uwnetid:
                        entities.append(self.get_entity_by_netid(uwnetid))

            if data.get("Next") is not None and len(data["Next"]["Href"]) > 0:
                url = data["Next"]["Href"]
            else:
                break
        return entities

    def get_entity_by_regid(self, regid):
        """
        Returns a restclients.Entity object for the given regid.  If the
        regid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        url = f"{ENTITY_PREFIX}/{regid.upper()}.json"
        return Entity.from_json(self._get_resource(url))

    def get_entity_by_netid(self, netid):
        """
        Returns a restclients.Entity object for the given netid.  If the
        netid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        url = f"{ENTITY_PREFIX}/{netid.lower()}.json"
        return Entity.from_json(self._get_resource(url))

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

        url = f"{PHOTO_PREFIX}/{regid.upper()}-{size}.jpg"

        headers = {"Accept": "image/jpeg"}

        if self.actas is not None:
            if not self.valid_uwnetid(self.actas):
                raise InvalidNetID(self.actas)
            headers["X-UW-Act-as"] = self.actas

        response = self.dao.getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return streamIO(response.data)

    def _get_resource(self, url,
                      header={"Accept": "application/json",
                              'Connection': 'keep-alive'}):
        response = self.dao.getURL(url, header)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        # Search does not return a full person resource
        return json.loads(response.data)

    def valid_uwnetid(self, netid):
        return (netid is not None and
                self._re_netid.match(str(netid)) is not None)

    def valid_uwregid(self, regid):
        return (regid is not None and
                self._re_regid.match(str(regid)) is not None)

    def valid_employee_id(self, employee_id):
        return (employee_id is not None and
                self._re_employee_id.match(str(employee_id)) is not None)

    def valid_student_number(self, student_number):
        return (
            student_number is not None and
            self._re_student_number.match(str(student_number)) is not None)

    def valid_student_system_key(self, system_key):
        return (
            system_key is not None and
            self._re_student_system_key.match(str(system_key)) is not None)

    def valid_prox_rfid(self, prox_rfid):
        return (prox_rfid is not None and
                self._re_prox_rfid.match(str(prox_rfid)) is not None)
