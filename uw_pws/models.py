from nameparser import HumanName
from restclients_core import models


class Person(models.Model):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)

    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    whitepages_publish = models.NullBooleanField()

    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    full_name = models.CharField(max_length=250)
    display_name = models.CharField(max_length=250)
    preferred_name = models.CharField(max_length=250)

    student_number = models.CharField(max_length=9,
                                      null=True, default=None)
    student_system_key = models.SlugField(max_length=10,
                                          null=True, default=None)
    employee_id = models.CharField(max_length=9, null=True, default=None)

    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_alum = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

    email1 = models.CharField(max_length=255, null=True, default=None)
    email2 = models.CharField(max_length=255, null=True, default=None)
    phone1 = models.CharField(max_length=255, null=True, default=None)
    phone2 = models.CharField(max_length=255, null=True, default=None)
    voicemail = models.CharField(max_length=255, null=True, default=None)
    fax = models.CharField(max_length=255, null=True, default=None)
    touchdial = models.CharField(max_length=255, null=True, default=None)
    address1 = models.CharField(max_length=255, null=True, default=None)
    address2 = models.CharField(max_length=255, null=True, default=None)
    mailstop = models.CharField(max_length=255)
    title1 = models.CharField(max_length=255)
    title2 = models.CharField(max_length=255, null=True, default=None)
    department1 = models.CharField(max_length=255, null=True, default=None)
    department2 = models.CharField(max_length=255, null=True, default=None)
    home_department = models.CharField(max_length=255)
    publish_in_emp_directory = models.BooleanField()

    student_class = models.CharField(max_length=255,
                                     null=True, default=None)
    student_department1 = models.CharField(max_length=255,
                                           null=True, default=None)
    student_department2 = models.CharField(max_length=255,
                                           null=True, default=None)
    student_department3 = models.CharField(max_length=255,
                                           null=True, default=None)

    def json_data(self):
        return {'uwnetid': self.uwnetid,
                'uwregid': self.uwregid,
                'first_name': self.first_name,
                'surname': self.surname,
                'full_name': self.full_name,
                'display_name': self.display_name,
                'preferred_name': self.preferred_name,
                'whitepages_publish': self.whitepages_publish,
                'email1': self.email1,
                'email2': self.email2,
                'phone1': self.phone1,
                'phone2': self.phone2,
                'title1': self.title1,
                'title2': self.title2,
                'voicemail': self.voicemail,
                'fax': self.fax,
                'touchdial': self.touchdial,
                'address1': self.address1,
                'address2': self.address2,
                'mailstop': self.mailstop,
                'department1': self.department1,
                'department2': self.department2,
                'home_department': self.home_department,
                'publish_in_emp_directory': self.publish_in_emp_directory,
                }

    def __eq__(self, other):
        return self.uwregid == other.uwregid

    def get_formatted_name(self):
        if self.preferred_name != "":
            return self.preferred_name

        if ((self.display_name is None or not len(self.display_name) or
             self.display_name.isupper()) and hasattr(self, 'first_name')):
            fullname = HumanName(self.display_name)
            fullname.capitalize()
            fullname.string_format = '{first} {middle} {last}'
            return str(fullname)
        else:
            return self.display_name

    @staticmethod
    def from_json(person_data):
        person = Person()
        person.uwnetid = person_data["UWNetID"]
        person.uwregid = person_data["UWRegID"]

        person.whitepages_publish = person_data["WhitepagesPublish"]
        person.surname = person_data["RegisteredSurname"]
        person.first_name = person_data["RegisteredFirstMiddleName"]
        person.full_name = person_data["RegisteredName"]
        person.display_name = person_data["DisplayName"]

        if "PreferredName" in person_data:
            person.preferred_name = person_data["PreferredName"]
        else:
            person.preferred_name = ""

        person_affiliations = person_data.get('PersonAffiliations')
        if person_affiliations is not None:
            student_affiliations = (person_affiliations
                                    .get('StudentPersonAffiliation'))
            if student_affiliations is not None:
                person.student_number = (student_affiliations
                                         .get('StudentNumber'))
                person.student_system_key = (student_affiliations
                                             .get('StudentSystemKey'))
            employee_affiliations = (person_affiliations
                                     .get('EmployeePersonAffiliation'))
            if employee_affiliations is not None:
                person.employee_id = (employee_affiliations
                                      .get('EmployeeID'))

        for affiliation in person_data["EduPersonAffiliations"]:
            if affiliation == "student":
                person.is_student = True
            elif affiliation == "alum":
                person.is_alum = True
            elif affiliation == "staff":
                person.is_staff = True
            elif affiliation == "faculty":
                person.is_faculty = True
            elif affiliation == "employee":
                person.is_employee = True

        affiliations = person_data["PersonAffiliations"]
        if "EmployeePersonAffiliation" in affiliations:
            employee = affiliations["EmployeePersonAffiliation"]
            person.mailstop = employee["MailStop"]
            person.home_department = employee["HomeDepartment"]
            white_pages = employee["EmployeeWhitePages"]
            person.publish_in_emp_directory = white_pages["PublishInDirectory"]

            if person.publish_in_emp_directory:
                person.email1 = white_pages["Email1"]
                person.email2 = white_pages["Email2"]
                person.phone1 = white_pages["Phone1"]
                person.phone2 = white_pages["Phone2"]
                person.title1 = white_pages["Title1"]
                person.title2 = white_pages["Title2"]
                person.voicemail = white_pages["VoiceMail"]
                person.fax = white_pages["Fax"]
                person.touchdial = white_pages["TouchDial"]
                person.address1 = white_pages["Address1"]
                person.address2 = white_pages["Address2"]
                person.department1 = white_pages["Department1"]
                person.department2 = white_pages["Department2"]

        if "StudentPersonAffiliation" in affiliations and person.is_student:
            student = affiliations["StudentPersonAffiliation"]
            if "StudentWhitePages" in student:
                white_pages = student["StudentWhitePages"]
                if "Class" in white_pages:
                    person.student_class = white_pages["Class"]
                if "Department1" in white_pages:
                    person.student_department1 = (white_pages
                                                  .get('Department1'))
                if "Department2" in white_pages:
                    person.student_department2 = (white_pages
                                                  .get('Department2'))
                if "Department3" in white_pages:
                    person.student_department3 = (white_pages
                                                  .get('Department3'))
        return person


# PWS Person
class Entity(models.Model):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)
    uwnetid = models.CharField(max_length=128,
                               db_index=True,
                               unique=True)
    display_name = models.CharField(max_length=250)

    def json_data(self):
        return {'uwnetid': self.uwnetid,
                'uwregid': self.uwregid,
                'display_name': self.display_name,
                }

    def __eq__(self, other):
        return self.uwregid == other.uwregid
