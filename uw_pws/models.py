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

    student_number = models.CharField(max_length=9,
                                      null=True, default=None)
    student_system_key = models.SlugField(max_length=10,
                                          null=True, default=None)
    employee_id = models.CharField(max_length=9, null=True, default=None)

    is_student = models.NullBooleanField()
    is_staff = models.NullBooleanField()
    is_employee = models.NullBooleanField()
    is_alum = models.NullBooleanField()
    is_faculty = models.NullBooleanField()

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
