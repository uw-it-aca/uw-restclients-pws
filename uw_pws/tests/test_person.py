# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from unittest import TestCase
from uw_pws import PWS
from restclients_core.exceptions import (InvalidRegID, InvalidNetID,
                                         DataFailureException,
                                         InvalidEmployeeID)
from uw_pws.exceptions import InvalidStudentNumber
from uw_pws.util import fdao_pws_override


@fdao_pws_override
class PWSTestPersonData(TestCase):

    def test_by_regid(self):
        # Valid data, shouldn't throw exceptions
        self._test_regid('javerage', '9136CCB8F66711D5BE060004AC494FFE')
        self._test_regid('phil', 'A9D2DDFA6A7D11D5A4AE0004AC494FFE')
        self._test_regid('eight', '12345678901234567890123456789012')

    def test_by_netid(self):
        # Valid data, shouldn't throw exceptions
        self._test_netid('javerage', '9136CCB8F66711D5BE060004AC494FFE')
        self._test_netid('phil', 'A9D2DDFA6A7D11D5A4AE0004AC494FFE')
        self._test_netid('eight', '12345678901234567890123456789012')

    def test_prior_ids(self):
        pws = PWS()
        person = pws.get_person_by_netid('javerage')
        self.assertEquals(len(person.prior_uwnetids), 1)
        self.assertEquals(person.prior_uwnetids[0], 'javerag')
        self.assertEquals(len(person.prior_uwregids), 1)
        self.assertEquals(person.prior_uwregids[0],
                          "9136CCB8F66711D5BE060004AC494FF0")

    def test_by_employeeid(self):
        pws = PWS()
        person = pws.get_person_by_employee_id('123456789')
        self.assertEquals(person.uwnetid, 'javerage', "Correct netid")
        self.assertEquals(
            person.uwregid,
            '9136CCB8F66711D5BE060004AC494FFE', "Correct regid")

        self.assertRaises(InvalidEmployeeID,
                          pws.get_person_by_employee_id,
                          '12345')

        # Valid non-existent employee ID
        self.assertRaises(DataFailureException,
                          pws.get_person_by_employee_id,
                          '999999999')

    def test_by_student_number(self):
        pws = PWS()
        person = pws.get_person_by_student_number('1234567')
        self.assertEquals(person.uwnetid, 'javerage', "Correct netid")
        self.assertEquals(person.uwregid,
                          '9136CCB8F66711D5BE060004AC494FFE', "Correct regid")

        # Valid non-existent student number
        self.assertRaises(DataFailureException,
                          pws.get_person_by_student_number,
                          '9999999')

        self.assertRaises(InvalidStudentNumber,
                          pws.get_person_by_student_number,
                          '123456')

    def test_person_search(self):
        persons = PWS().person_search(changed_since_date=2019)
        self.assertEqual(len(persons), 2)
        self.assertEqual(persons[0].uwnetid, "javerage")
        self.assertEqual(persons[1].uwnetid, "phil")

    def test_names(self):
        pws = PWS()
        person = pws.get_person_by_netid('javerage')
        self.assertEquals(person.surname, 'STUDENT')
        self.assertEquals(person.first_name, 'JAMES AVERAGE')
        self.assertEquals(person.full_name, 'JAMES AVERAGE STUDENT')
        self.assertEquals(person.preferred_first_name, 'Jamesy')
        self.assertEquals(person.preferred_middle_name, '')
        self.assertEquals(person.preferred_surname, 'McJamesy')
        self.assertEquals(person.display_name, 'Jamesy McJamesy')
        self.assertEquals(person.student_number, "1033334")
        self.assertEquals(person.employee_id, "123456789")
        self.assertEquals(person.student_class, "Junior")

    def test_formatted_name(self):
        pws = PWS()
        person = pws.get_person_by_netid('javerage')
        self.assertEquals(person.get_formatted_name(), person.display_name)

        person.display_name = 'JAMES AVERAGE STUDENT'
        self.assertEquals(person.get_formatted_name(), "James Average Student")

        person.display_name = ''
        self.assertEquals(person.get_formatted_name(), "James Average Student")

        person.display_name = None
        self.assertEquals(person.get_formatted_name(), "James Average Student")
        self.assertEquals(
            person.get_formatted_name(string_format='{first} {last}'),
            "James Student")

    def test_first_last_name(self):
        pws = PWS()
        person = pws.get_person_by_netid('javerage')
        self.assertEquals(person.get_first_last_name(),
                          ('Jamesy', 'McJamesy'))

        person = pws.get_person_by_netid('javerage')
        person.preferred_surname = None
        self.assertEquals(person.get_first_last_name(),
                          ('JAMES AVERAGE', 'STUDENT'))

        person = pws.get_person_by_netid('javerage')
        person.preferred_first_name = ''
        self.assertEquals(person.get_first_last_name(),
                          ('JAMES AVERAGE', 'STUDENT'))

    def test_bad_netids(self):
        # Invalid data, should throw exceptions
        pws = PWS()
        self.assertRaises(InvalidNetID, pws.get_person_by_netid, "")
        self.assertRaises(InvalidNetID, pws.get_person_by_netid, " ")
        self.assertRaises(InvalidNetID,
                          pws.get_person_by_netid, "one two")
        self.assertRaises(InvalidNetID,
                          pws.get_person_by_netid, "</html>")
        self.assertRaises(InvalidNetID,
                          pws.get_person_by_netid,
                          "0notareal_uwnetid")
        self.assertRaises(DataFailureException,
                          pws.get_person_by_netid, "hello")

    def test_bad_regids(self):
        # Invalid data, should throw exceptions
        pws = PWS()
        self.assertRaises(InvalidRegID, pws.get_person_by_regid, "")
        self.assertRaises(InvalidRegID, pws.get_person_by_regid, " ")
        self.assertRaises(InvalidRegID, pws.get_person_by_regid, "AAA")

        self.assertRaises(InvalidRegID,
                          pws.get_person_by_regid,
                          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        self.assertRaises(InvalidRegID,
                          pws.get_person_by_regid,
                          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG")

        self.assertRaises(DataFailureException,
                          pws.get_person_by_regid,
                          "9136CCB8F66711D5BE060004AC494FFF")

    def test_bad_employee_ids(self):
        pws = PWS()
        self.assertRaises(InvalidEmployeeID, pws.get_person_by_employee_id, "")
        self.assertRaises(InvalidEmployeeID,
                          pws.get_person_by_employee_id, " ")
        self.assertRaises(InvalidEmployeeID,
                          pws.get_person_by_employee_id, "A")
        self.assertRaises(InvalidEmployeeID,
                          pws.get_person_by_employee_id, "12345678N")
        self.assertRaises(InvalidEmployeeID,
                          pws.get_person_by_employee_id, "1")
        self.assertRaises(InvalidEmployeeID,
                          pws.get_person_by_employee_id, "1234567890")

    def test_compare_persons(self):
        pws = PWS()

        person1 = pws.get_person_by_regid("7718EB38AE3411D689DA0004AC494FFE")
        person2 = pws.get_person_by_regid("7718EB38AE3411D689DA0004AC494FFE")
        person3 = pws.get_person_by_regid("9136CCB8F66711D5BE060004AC494FFE")

        self.assertEquals(person1 == person2, True, "persons are equal")
        self.assertEquals(person1 == person3, False, "persons are inequal")

    def test_affiliation_data(self):
        pws = PWS()

        person1 = pws.get_person_by_netid("javerage")
        self.assertEquals(person1.is_student, True)
        self.assertEquals(person1.is_alum, True)
        self.assertEquals(person1.is_staff, True)
        self.assertEquals(person1.is_faculty, False)
        self.assertEquals(person1.is_employee, True)
        self.assertEquals(person1.student_state, "current")
        self.assertTrue(person1.is_alum_state_current())
        self.assertTrue(person1.is_emp_state_current())
        self.assertTrue(person1.is_stud_state_current())

        self.assertEquals(person1.mailstop, '359540', "MailStop")
        self.assertEquals(person1.home_department, "Computer Science",
                          "HomeDepartment")
        self.assertEquals(person1.student_number, "1033334")
        self.assertEquals(person1.employee_id, "123456789")
        self.assertEquals(len(person1.student_departments), 2)
        self.assertEquals(person1.student_departments[0], "Computer Science")

        person2 = pws.get_person_by_netid("finals1")
        self.assertEquals(person2.is_student, True)
        self.assertEquals(person2.is_alum, True)
        self.assertEquals(person2.is_staff, True)
        self.assertEquals(person2.is_faculty, False)
        self.assertEquals(person2.is_employee, True)

        self.assertEquals(person2.home_department, "C&C TEST BUDGET",
                          "HomeDepartment")
        self.assertEquals(person2.student_number, "1033334")
        self.assertEquals(person2.employee_id, "123456789")
        self.assertEquals(person2.student_class, None)
        self.assertEquals(len(person2.student_departments), 0)

    def _test_regid(self, netid, regid):
        pws = PWS()
        person = pws.get_person_by_regid(regid)

        self.assertEquals(person.uwnetid, netid, netid + "'s netid")
        self.assertEquals(person.uwregid, regid, netid + "'s regid")

    def _test_netid(self, netid, regid):
        pws = PWS()
        person = pws.get_person_by_netid(netid)

        self.assertEquals(person.uwnetid, netid, netid + "'s netid")
        self.assertEquals(person.uwregid, regid, netid + "'s regid")

    def test_employee_data(self):
        pws = PWS()
        person = pws.get_person_by_netid('bill')
        self.assertEqual(person.display_name, "Bill Teacher")
        self.assertEqual(person.get_formatted_name(), "Bill Teacher")
