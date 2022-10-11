from django.db import models


class UserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "user_group"


class GroupPermission(models.Model):
    id = models.AutoField(primary_key=True)
    user_group = models.ForeignKey(UserGroup, on_delete=models.PROTECT, null=True, blank=True)
    table_name = models.CharField(max_length=200)
    add = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    list = models.BooleanField(default=False)
    view = models.BooleanField(default=False)

    class Meta:
        db_table = "group_permission"


class UserAccount(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user_photo = models.CharField(max_length=150, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    primary_email = models.CharField(max_length=50, null=True, blank=True)
    secondary_email = models.CharField(max_length=50, null=True, blank=True)
    primary_phone = models.CharField(max_length=50, null=True, blank=True)
    secondary_phone = models.CharField(max_length=50, null=True, blank=True)

    user_group = models.ForeignKey(UserGroup, on_delete=models.PROTECT, null=True, blank=True)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=10, null=True, blank=True)

    entry_date = models.DateTimeField(null=True, blank=True)
    entered_by = models.CharField(max_length=50, null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "user_account"


class UserSetting(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="user_setting_user")
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    entry_date = models.DateTimeField(null=True, blank=True)
    entered_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True, related_name="user_setting_entered_by")
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True, related_name="user_setting_modified_by")

    class Meta:
        db_table = "user_setting"


class SystemLog(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    entry_date = models.DateTimeField(null=True, blank=True)
    table_name = models.CharField(max_length=50)
    record_id = models.CharField(max_length=50, null=True, blank=True)
    operation_type = models.CharField(max_length=50)
    operation_summary = models.CharField(max_length=100)
    full_description = models.CharField(max_length=500)
    user_id = models.CharField(max_length=50, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "system_log"


class Country(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    entry_date = models.DateTimeField(null=True, blank=True)
    entered_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="country_entered_by")
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="country_modified_by")

    class Meta:
        db_table = "country"


class DepartmentType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    entry_date = models.DateTimeField(null=True, blank=True)
    entered_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_type_entered_by")
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_type_modified_by")

    class Meta:
        db_table = "department_type"


class Department(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_country")
    department_type = models.ForeignKey(DepartmentType, on_delete=models.PROTECT, null=True, blank=True,
                                related_name="department_department_type")

    entry_date = models.DateTimeField(null=True, blank=True)
    entered_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_entered_by")
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_modified_by")

    class Meta:
        db_table = "department"


class DepartmentSupervisor(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_supervisor_department")
    user = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                related_name="department_supervisor_user")

    entry_date = models.DateTimeField(null=True, blank=True)
    entered_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_supervisor_entered_by")
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_supervisor_modified_by")

    class Meta:
        db_table = "department_supervisor"


class DepartmentEmployee(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_employee_department")
    user = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                related_name="department_employee_user")

    entry_date = models.DateTimeField(null=True, blank=True)
    entered_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_employee_entered_by")
    last_modified = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(UserAccount, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="department_employee_modified_by")

    class Meta:
        db_table = "department_employee"




