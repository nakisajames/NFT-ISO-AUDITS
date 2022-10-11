class Language:
    def __init__(self, m_lang_id="en"):
        self.lang_id = m_lang_id
        self.global_phrases = dict()
        self.table_phrases = dict()
        self.menu_phrases = dict()
        self.load_language(m_lang_id)

    def phrase(self, phrase_id):
        return str(self.global_phrases.get(phrase_id, phrase_id))

    def men_phrase(self, phrase_id):
        return str(self.menu_phrases.get(phrase_id, phrase_id))

    def tbl_phrase(self, tbl_id):
        return str(self.table_phrases.get(tbl_id, dict()).get("caption", tbl_id))

    def fld_phrase(self, tbl_id, fld_id):
        return str(self.table_phrases.get(tbl_id, dict()).get("fields", dict()).get(fld_id, fld_id))

    def load_language(self, m_lang_id):
        import xml.etree.ElementTree as ET
        from django_jailuapp.settings import BASE_DIR
        filename = BASE_DIR + '/JailuApp/lang/english.xml'
        tree = ET.parse(filename)
        root = tree.getroot()
        # read global phrases
        for node in root[0]:
            self.global_phrases[node.attrib["id"]] = node.attrib["caption"]
        # read table phrases
        for node in root[1]:
            fields = dict()  # capture all fields for said table
            for a_field in node:
                fields[a_field.attrib["id"]] = a_field.attrib["caption"]
            self.table_phrases[node.attrib["id"]] = dict(caption=node.attrib["caption"], fields=fields)
        # read menu phrases
        for node in root[2]:
            self.menu_phrases[node.attrib["id"]] = node.attrib["caption"]


Lang = Language()


class DefaultValues:
    from django_jailuapp.settings import TIME_ZONE
    records_per_page = 10
    session_logged_in_user_id = "session_logged_in_user_id"
    session_logged_in_user_expiry = "session_logged_in_user_expiry"
    notification_icon = 'https://nftconsult.com/wp-content/uploads/2018/02/f65ccf_8b10605fb8ee412ca4f3e87d26dc1718_mv2.png'
    notification_click_url = "https://nftconsult.com"
    default_timezone = TIME_ZONE
    uptime_http_type = "Http_Request"
    uptime_ip_type = "IP_Request"
    uptime_imap_type = "Imap_Request"
    uptime_network_internet = "Internet"
    uptime_network_lan = "Local_Area"
    uptime_record_internet = "1"
    uptime_record_lan = "2"
    js_notification_timer = 60000
    max_bulk_size = 1000  # maximum importable size per group insert


EW = DefaultValues()


class AnItem:
    def __init__(self, m_code, m_caption):
        self.code = m_code
        self.caption = m_caption

    def name(self):
        return str(self.caption)


class CSystemActions:
    List = AnItem('list', 'List')
    Add = AnItem('add', 'Add')
    Edit = AnItem('edit', 'Edit')
    View = AnItem('view', 'View')
    SubmitAdd = AnItem('submit_add', 'Submit Add')
    SubmitEdit = AnItem('submit_edit', 'Submit Edit')
    Delete = AnItem('submit_delete', 'Delete')
    ExcelExport = AnItem('excel', 'Excel Export')
    PdfExport = AnItem('pdf', 'Pdf Export')


Actions = CSystemActions()


class CInputTypes:
    TEXT = AnItem('text', 'text')
    DROPDOWN = AnItem('drop_down', 'drop_down')
    DATETIME = AnItem('date_time', 'date_time')
    DATE = AnItem('date', 'date')
    FILE = AnItem('file', 'file')
    TEXTAREA = AnItem('textarea', 'textarea')
    RADIOBUTTON = AnItem('radiobutton', 'radiobutton')
    SELECT2DROPDOWN = AnItem('select_2_drop_down', 'select_2_drop_down')
    MULTISELECTION_CHECKBOX = AnItem('multi_selectcion_checkbox', 'multi_selectcion_checkbox')
    HTML_EDITOR_TINYMCE = AnItem('html_editor_tinymce', 'html_editor_tinymce')


InputTypes = CInputTypes()


class CValidationTypes:
    INT = AnItem('int', 'int')
    NONE = AnItem('none', 'none')
    FLOAT = AnItem('float', 'float')
    DATE = AnItem('date', 'date')
    DATETIME = AnItem('date_time', 'date_time')
    EMAIL = AnItem('email', 'email')
    NON_NUMERIC = AnItem('non_numeric', 'non_numeric')
    PHONE_NUMBER_10 = AnItem('phone_number_10', 'phone_number_10')


ValidationTypes = CValidationTypes()


class CFilterTypes:
    EQUAL = AnItem('equal', 'equal')
    LIKE = AnItem('like', 'like')
    BETWEEN = AnItem('between', 'between')


FilterTypes = CFilterTypes()


class CPaginationLimits:
    EQUAL = AnItem('equal', 'equal')
    LIKE = AnItem('like', 'like')
    BETWEEN = AnItem('between', 'between')


PageSizes = [2, 5, 10, 25, 50, 100, 250, 500, 1000]


class CLookups:

    def __init__(self):
        from django.db import transaction
        transaction.commit()  # Whenever you want to see new data

    def extract_lookup(self, id_field, name_field, data):
        lookup_data = list()
        for ele in data:
            item = (ele if type(ele) is dict else ele.__dict__)
            lookup_data.append([item.get(id_field), item.get(name_field)])
        return lookup_data

    def user_groups(self):
        from JailuApp.models import UserGroup
        return self.extract_lookup('id', 'name', my_custom_sql("select id, name from user_group order by name asc"))

    def non_admin_user_groups(self):
        from JailuApp.models import UserGroup
        return self.extract_lookup('id', 'name', my_custom_sql("select id, name from user_group where id not in (-2,-1) order by name asc"))

    def non_developer_users(self):
        return self.extract_lookup('id', 'full_name', my_custom_sql("""select id, full_name as full_name from user_account where id != '1' order by full_name asc"""))

    def all_users(self):
        return self.extract_lookup('id', 'full_name', my_custom_sql("""select id, full_name as full_name from user_account order by full_name asc"""))


    def genders(self):
        return self.extract_lookup('id', 'name', [dict({'id': "Male", 'name': "Male"})
                                                  , dict({'id': "Female", 'name': "Female"})])


    def yes_no_status(self):
        return self.extract_lookup('id', 'name', [dict({'id': "Yes", 'name': "Yes"})
                                                  , dict({'id': "No", 'name': "No"})])
    def active_disabled_status(self):
        return self.extract_lookup('id', 'name', [dict({'id': "Active", 'name': "Active"})
                                                  , dict({'id': "Disabled", 'name': "Disabled"})])
    def true_false_yn_status(self):
        return self.extract_lookup('id', 'name', [dict({'id': "True", 'name': "Yes"})
                                                  , dict({'id': "False", 'name': "No"})])

    def countrys(self):
        return self.extract_lookup('id', 'name', my_custom_sql("""select id, name from country order by name """))

    def department_types(self):
        return self.extract_lookup('id', 'name', my_custom_sql("""select id, name from department_type order by name """))

    def departments(self):
        return self.extract_lookup('id', 'name', my_custom_sql("""select d.id, concat_ws('-',c.name,dt.name) as name 
        from department d join department_type dt on d.department_type_id = dt.id join country c on d.country_id = c.id 
          order by c.entry_date, dt.name """))

    def project_status(self):
        return self.extract_lookup('id', 'name', [dict({'id': "In Progress", 'name': "In Progress"})
                                                  , dict({'id': "Complete", 'name': "Complete"})
                                                  , dict({'id': "Canceled", 'name': "Canceled"})
                                                  , dict({'id': "On Hold", 'name': "On Hold"})
                                                  ])



    def get_name_by_id(self, item_id, lookup_list):
        for ele in lookup_list:
            if str(ele[0]) == str(item_id):
                return ele[1]
        return item_id


Lookups = CLookups()


class MenuItem:
    def __init__(self, m_id, m_icon, m_target_object, m_target_action, m_target_object_id='', m_items=None):
        if m_items is None:
            m_items = []
        self.id = str(m_id)
        self.icon = str(m_icon)
        self.caption = Lang.men_phrase(self.id)
        self.target_object = str(m_target_object)
        self.target_action = str(m_target_action)
        self.target_object_id = str(m_target_object_id)
        self.items = m_items

    def code(self):
        return str(self.code)

    def name(self):
        return str(self.caption)

    def html_link(self):
        # for single items
        if self.items.__len__() == 0:
            return """
            <li id='li_""" + self.id + """'>
             <a href="javascript:void(0);" id='""" + self.id + """' 
             onclick="ShowForm(this,'""" + self.target_action + """','""" + self.target_object + """','""" + \
                   str(self.target_object_id) + """')">
                  <i class="metismenu-icon """ + self.icon + """ "></i>""" + self.caption + """
              </a>
            </li>
            """ if Security.check_permission(self.target_object, self.target_action) is True else ""
        else:
            html = """"""
            # check if we need to draw
            if self.has_active_items() is True:
                html += """
                <li id='li_""" + self.id + """'>
                 <a href="javascript:void(0);" id='""" + self.id + """' >
                      <i class="metismenu-icon """ + self.icon + """ "></i>
                      """ + self.caption + """
                      <i class="metismenu-state-icon pe-7s-angle-down caret-left"></i>
                  </a>
                  <ul class="mm-collapse" style="height: 0px;">
                      """
                #draw sub items
                for x in self.items:
                    html += x.html_link()
                html += """
                      </ul>
                </li>
                """
            return html

    def has_active_items(self):
        for x in self.items:
            # if it has other sub items then check collective sub items
            if x.items.__len__() > 0:
                for inner_item in x.items:
                    if Security.check_permission(inner_item.target_object, inner_item.target_action) is True:
                        return True
            else:  # if its a single item
                if Security.check_permission(x.target_object, x.target_action) is True:
                    return True
        return False


class Menu:

    items = list()

    def __init__(self):
        self.items = list()

        self.items.append(
            MenuItem('mi_security_value_list', 'fas fa-lock'
                     , None, None, ""
                     , [MenuItem(m_id='mi_department', m_icon='fas fa-cog'
                                 , m_target_object='department', m_target_action=Actions.List.code)
                         , MenuItem(m_id='mi_country', m_icon='fas fa-cog'
                                    , m_target_object='country', m_target_action=Actions.List.code)
                         , MenuItem(m_id='mi_department_type', m_icon='fas fa-cog'
                                    , m_target_object='department_type', m_target_action=Actions.List.code)
                         ,MenuItem(m_id='mi_user_group', m_icon='fas fa-cog'
                                 , m_target_object='user_group', m_target_action=Actions.List.code)
                         , MenuItem(m_id='mi_user_account', m_icon='fas fa-cog'
                                    , m_target_object='user_account', m_target_action=Actions.List.code)
                         , MenuItem(m_id='mi_system_log', m_icon='fas fa-tag'
                                    , m_target_object='system_log', m_target_action=Actions.List.code)
                        ])
        )






    def add_item(self, m_item):
        self.items.append(m_item)

    def draw_menu(self):
        #html = """<ul class="nav nav-pills nav-sidebar flex-column"
        #data-widget="treeview" role="menu" data-accordion="false">"""
        html = """ <div class="app-sidebar-wrapper">
                <div class="app-sidebar sidebar-shadow">
                    <div class="app-header__logo">
                        <a href="#" data-toggle="tooltip" data-placement="bottom" title="KeroUI Admin Template" class="logo-src"></a>
                        <button type="button" class="hamburger hamburger--elastic mobile-toggle-nav">
                                <span class="hamburger-box">
                                    <span class="hamburger-inner"></span>
                                </span>
                        </button>
                    </div>
                    <div class="scrollbar-sidebar scrollbar-container">
                        <div class="app-sidebar__inner">
                            <ul class="vertical-nav-menu">
                                <li class="app-sidebar__heading">Menu</li>
                                <li><a href="#"><i class="metismenu-icon pe-7s-rocket"></i>Dashboards</a></li>
                                <li><a href="#"><i class="metismenu-icon pe-7s-rocket"></i>Dashboards</a></li>
                                <li><a href="#"><i class="metismenu-icon pe-7s-rocket"></i>Dashboards</a></li>

                            </ul>
                        </div>
                    </div>
                </div>
            </div> """
        html = """ <div class="app-sidebar-wrapper">
                        <div class="app-sidebar sidebar-shadow ">
                            <div class="app-header__logo">
                                <a href="#" data-toggle="tooltip" data-placement="bottom" title="KeroUI Admin Template" class="logo-src"></a>
                                <button type="button" class="hamburger hamburger--elastic mobile-toggle-nav">
                                        <span class="hamburger-box">
                                            <span class="hamburger-inner"></span>
                                        </span>
                                </button>
                            </div>
                            <div class="scrollbar-sidebar scrollbar-container">
                                <div class="app-sidebar__inner">
                                    <ul class="vertical-nav-menu">
                  """
        for x in self.items:
            html += x.html_link()
        html += """
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div> """
        return html

# decalre all menus


class CSecurity:
    permitted_actions = [Actions.Add.code, Actions.SubmitAdd.code, Actions.Edit.code
        , Actions.SubmitEdit.code, Actions.Delete.code, Actions.List.code, Actions.ExcelExport.code
        , Actions.View.code, Actions.PdfExport.code]
    super_admin_group_id = -1
    anonymous_group_id = -2
    table_objects = ["user_group", "user_account", "system_log", "country", "department_type", "department"
        , "department_supervisor", "department_employee"]

    is_logged_in = False
    user_profile = dict()
    user_group_id = -2
    user_account_id = None
    user_group = dict()
    permissions = dict()
    req = None
    expiry_seconds = 43200 # 300 is 5 minutes

    def __init__(self):
        self.prepare_security()

    def prepare_security(self):
        self.is_logged_in = False
        self.user_profile = dict()
        self.user_group_id = -2
        self.user_account_id = None
        self.user_group = dict()
        self.permissions = dict()

    def reset_expiry(self):
        # reset expiry due to detected activity
        from datetime import datetime
        self.req.session[EW.session_logged_in_user_expiry] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.req.session.modified = True
        self.req.session.save()

    def has_session_expired(self):

        # check if session timer value exists
        if is_empty(self.req.session.get(EW.session_logged_in_user_expiry, '')) is True:
            return True
        # check if timer value is a valid integer
        elif is_datetime(self.req.session.get(EW.session_logged_in_user_expiry)) is False:
            return True
        # check if timer has expired
        from datetime import datetime
        diff = datetime.now() - convert_to_datetime(self.req.session.get(EW.session_logged_in_user_expiry))
        seconds_elapsed = diff.total_seconds()
        if seconds_elapsed > self.expiry_seconds:
            return True
        else:
            return False

    def save_user_session(self, user_id):
        # set sessions
        self.req.session[EW.session_logged_in_user_id] = user_id
        self.req.session.modified = True
        self.req.session.save()

        self.reset_expiry()

        # save this user now
        # clear any data
        self.prepare_security()
        self.initialise(self.req)

    def clear_user_session(self):
        # check if session key is there before deleting
        if is_empty(self.req.session.get(EW.session_logged_in_user_id, None)) is False:
            del self.req.session[EW.session_logged_in_user_id]
        # clear logout timer
        if is_empty(self.req.session.get(EW.session_logged_in_user_expiry, None)) is False:
            del self.req.session[EW.session_logged_in_user_expiry]

        self.req.session.modified = True
        self.req.session.save()
        # clear any data
        self.prepare_security()

    def has_session_id(self):
        # check for browser level cookie setting
        from django_jailuapp.settings import SESSION_COOKIE_NAME
        # check if a valid cookie session value exists independent browser
        if is_empty(self.req.COOKIES.get(SESSION_COOKIE_NAME, '')) is False:
            return True
        else:
            return False

    def initialise(self, request):
        #  self.prepare_security()
        self.req = request
        # must have a valid browser cookie, a loggin session ID and session value timeout should still be valid
        if self.has_session_expired() is False and self.has_session_id() is True and is_empty(self.req.session.get(EW.session_logged_in_user_id, '')) is False:
            # setup for saved user
            from JailuApp.models import UserAccount
            user = UserAccount.objects.filter(id=self.req.session.get(EW.session_logged_in_user_id))
            if user.count() == 1:  # make sure user was found
                self.user_profile = user[0].__dict__
                self.is_logged_in = True
                self.user_group_id = user[0].user_group_id
                self.user_account_id = user[0].id
                self.user_group = user[0].user_group.__dict__
                # reset expiry
                self.reset_expiry()
        # empty all secuity settings if no session or browser cookie found
        else:
            self.prepare_security()
        from JailuApp.models import GroupPermission
        permission_list = GroupPermission.objects.all().filter(user_group_id=self.user_group_id)
        for item in permission_list:
            self.permissions[item.table_name] = dict({Actions.Add.code: item.add, Actions.SubmitAdd.code: item.add
                                                         , Actions.Edit.code: item.edit,
                                                      Actions.SubmitEdit.code: item.edit
                                                         , Actions.Delete.code: item.delete,
                                                      Actions.List.code: item.list
                                                         , Actions.ExcelExport.code: item.list
                                                      , Actions.View.code: item.view
                                                      , Actions.PdfExport.code: item.list})



    def initialise_api_user(self, user_id):
        self.prepare_security()
        if is_empty(user_id) is False:
            # setup for saved user
            from JailuApp.models import UserAccount
            user = UserAccount.objects.filter(id=user_id)
            if user.count() == 1:  # make sure user was found
                self.user_profile = user[0].__dict__
                self.is_logged_in = True
                self.user_group_id = user[0].user_group_id
                self.user_account_id = user[0].id
                self.user_group = user[0].user_group.__dict__
        from JailuApp.models import GroupPermission
        permission_list = GroupPermission.objects.all().filter(user_group_id=self.user_group_id)
        for item in permission_list:
            self.permissions[item.table_name] = dict({Actions.Add.code: item.add, Actions.SubmitAdd.code: item.add
                                                         , Actions.Edit.code: item.edit,
                                                      Actions.SubmitEdit.code: item.edit
                                                         , Actions.Delete.code: item.delete,
                                                      Actions.List.code: item.list
                                                         , Actions.ExcelExport.code: item.list
                                                      , Actions.View.code: item.view
                                                      , Actions.PdfExport.code: item.list})

    def user_full_names(self):
        return str( self.user_profile.get("full_name", "Unknown"))

    def user_group_names(self):
        return str(self.user_group.get("name", "Unknown"))

    def get_user_info(self,param):
        return self.user_profile.get(param, None)

    def check_permission(self, table_name, action):
        if self.is_admin() is True:  # allow all for super admins
            return True
        if action in self.permitted_actions:  # restrict known actions
            return bool(self.permissions.get(table_name, dict()).get(action, False))
        else:
            return True # allow unknown && actions

    def is_admin(self):
        return True if self.user_group_id == self.super_admin_group_id else False


Security = CSecurity()

def new_guid():
    import uuid
    return uuid.uuid4().hex


def generate_otp():
    import math, random
    digits = "0123456789"
    value = ""
    for i in range(4):
        value += digits[math.floor(random.random() * 10)]
    return value


def generate_password(size=10):
    import math, random
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    value = ""
    length = len(string)
    for i in range(size):
        value += string[math.floor(random.random() * length)]
    return value

def enrypt_passwordMd5(str):
    import hashlib
    return hashlib.md5(str.encode()).hexdigest()


def my_custom_sql(sql, params = []):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(sql, params) # "SELECT foo FROM bar WHERE baz = %s", [self.baz]
        #  "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]



def add_link(object_name, options="{}"):
    return str("""
    <a class="btn btn-success btn-lg btn-wide" href="javascript:void(0);" 
     onclick="ShowForm(this,'""" + Actions.Add.code + """','""" + str(object_name) + """'
     ,null,null,""" + options + """)">
      <i class='fas fa-plus'></i>""" + Lang.phrase("link_add") + """</a>
    """) if Security.check_permission(object_name, Actions.Add.code) is True else ""

def submit_add_link(object_name,options = "{}"):
    return str("""
            <button id='submit_form_""" + object_name + """_""" + Actions.Add.code + """' 
          onclick="SubmitForm(this,'""" + Actions.SubmitAdd.code + """','""" + object_name \
                     + """',null,""" + options + """)" 
                     class="btn btn-info">""" + Lang.phrase("btn_add") + """</button>
            """)


def edit_link(object_name, object_id, options="{}"):
    return str("""
        <a class="btn btn-info btn-sm" href="javascript:void(0);" 
        onclick="ShowForm(this,'""" + Actions.Edit.code + """','""" + str(
        object_name) + """','""" + str(
        object_id) + """',null,""" + options + """)">
          <i class='fas fa-pencil-alt'></i>""" + Lang.phrase("link_edit") + """
      </a>
        """) if Security.check_permission(object_name, Actions.Edit.code) is True else ""

def submit_edit_link(object_name,options = "{}"):
    return str("""
            <button id='submit_form_""" + object_name + """_""" + Actions.Edit.code + """' 
          onclick="SubmitForm(this,'""" + Actions.SubmitEdit.code + """','""" + object_name \
                     + """',null,""" + options + """)" 
                     class="btn btn-info">""" + Lang.phrase("btn_save") + """</button>
            """)


def delete_link(object_name, object_id,options = "{}", message="This record will be deleted, you will not be able to reverse this!"):
    return str("""
            <a class="btn btn-danger btn-sm" href="javascript:void(0);" 
            onclick="ConfirmDelete(this,'""" + str(
        object_name) + """','""" + str(object_id) + """','""" + str(message) + """',""" + options + """)">
              <i class='fas fa-trash'></i>""" + Lang.phrase("link_delete") + """
          </a>
            """) if Security.check_permission(object_name, Actions.Delete.code) is True else ""

def view_link(object_name, object_id, options="{}"):
    return str("""
        <a class="btn btn-secondary btn-sm" href="javascript:void(0);" 
        onclick="ShowForm(this,'""" + Actions.View.code + """','""" + str(
        object_name) + """','""" + str(
        object_id) + """',null,""" + options + """)">
          <i class='fas fa-eye'></i>""" + Lang.phrase("link_view") + """
      </a>
        """) if Security.check_permission(object_name, Actions.View.code) is True else ""


def ex_filter_link(object_name):
    return str("""
    <a class="btn btn-primary btn-md" href="javascript:void(0);" 
    id='submit_search_""" + object_name + """_""" + Actions.List.code + """'
     onclick="ShowForm(this,EW.action.List,'""" + object_name + """',null,1);" >
      <i class='fas fa-search'></i>""" + Lang.phrase("link_ex_filter") + """
  </a>
    """)

def confirm_submit_action_link(object_name,action_name, object_id, caption,
                message="This record will do the action, you will not be able to reverse this!", options="{}"):
    return """
            <a class="mb-2 mr-2 btn-icon btn-pill btn btn-outline-success icon-anim-pulse" href="javascript:void(0);" 
            onclick="ConfirmCustomAction(this,'""" + str(
        object_name) + """','""" + str(action_name) + """','""" + str(object_id) + """','""" + str(message) + """',""" + options + """)">
              <i class='fas fa-envelope'></i>""" + str(caption) + """
          </a>
            """

def export_excel_link(object_name, object_id = ""):
    return str("""
    <div role="group" class="btn-group-sm btn-group btn-group-toggle" data-toggle="buttons" hidden>
        <a class="btn-icon btn btn-light" href="javascript:void(0);" style="padding: .2rem .3rem;"  
         onclick="SubmitForm(this,EW.action.ExcelExport,'""" + object_name + """','""" + object_id + """');" >
          <i class='fas fa-file-excel fa-2x'></i>""" + Lang.phrase("link_export_excel") + """
        </a>
        <button hidden type="button" class="btn btn-info" style="padding: .2rem .3rem;" 
        onclick="SubmitForm(this,EW.action.ExcelExport,'""" + object_name + """','""" + object_id + """',{params:{email_export:true}});">
        <i class='fas fa-envelope fa-2x'></i>
        </button>
    </div>
    """) if Security.check_permission(object_name, Actions.ExcelExport.code) is True else ""

def export_pdf_link(object_name, object_id = ""):
    return str("""
    <div role="group" class="btn-group-sm btn-group btn-group-toggle" data-toggle="buttons"hidden >
        <a class="btn-icon btn btn-light" href="javascript:void(0);" style="padding: .2rem .3rem;" 
         onclick="SubmitForm(this,EW.action.PdfExport,'""" + object_name + """','""" + object_id + """');" >
          <i class='fas fa-file-pdf fa-2x'></i>""" + Lang.phrase("link_export_pdf") + """
        </a>
        <button hidden type="button" class="btn btn-info" style="padding: .2rem .3rem;" 
        onclick="SubmitForm(this,EW.action.PdfExport,'""" + object_name + """','""" + object_id + """',{params:{email_export:true}});">
        <i class='fas fa-envelope fa-2x'></i>
        </button>
    </div>
    
    """) if Security.check_permission(object_name, Actions.PdfExport.code) is True else ""


def email_a_file(file_name,file_url):
    from JailuApp.models import UserAccount
    obj = UserAccount.objects.get(id=current_user_id())
    # send email notification
    email_subject = file_name

    email_full_names = str(obj.full_name)
    email_to_address = [str(obj.primary_email)]
    email_body_content = """
                        Please find attached <strong>""" + file_name + """</strong> file.
                         <br/>
                        """
    email_body_plain_text = """
                        <div style="margin-bottom:14pt; margin-top:14pt">
                        Dear """ + email_full_names + """,</div>
                        <div style="margin-bottom:14pt; margin-top:14pt">
                        """ + email_body_content + """<br />
                        Best regards!<br />""" + Lang.phrase("site_title") + """ Team
                        </div>
                        </div>
                        """

    email_body_html = template_email()
    # fill in blanks
    email_body_html = email_body_html.replace("[[email_subject]]", email_subject)
    email_body_html = email_body_html.replace("[[email_full_names]]", email_full_names)
    email_body_html = email_body_html.replace("[[email_body_content]]", email_body_content)

    ret = smtp_send_email(email_to_address, email_subject, email_body_plain_text, email_body_html, [file_url])
    return ret

def pagination(object_name, total_records, current_page, records_per_page):
    from math import ceil
    total_pages = ceil(total_records / records_per_page)
    html = """<ul class='pagination pagination-md' >"""
    # draw page size
    html += """<li class="page-item">
                   <select id="page_size" class="form-control" style="padding-right: 5px;" 
                   onchange="ShowForm(
                   this,EW.action.List,'""" + object_name + """',null,1
                   ,{records_per_page: this.value,});">
                   """
    for x in PageSizes:
        html += """
               <option   
               value='""" + str(x) + """' """ + str(
            'selected' if str(x) == str(records_per_page) else '') + """ >""" + str(x) + """</option>
               """

    # set page size for diff pages
    size_options = """{
                                        records_per_page: """ + str(records_per_page) + """,
                                    }"""
    html += """</select></li>"""
    # only show if not first page
    if current_page != 1:
        html += """
        <li class="page-item"><a class="page-link" href='javascript:void(0);' 
        onclick="ShowForm(this,EW.action.List,'""" + object_name + """',null,1,""" + size_options + """);" >""" + Lang.phrase("pagination_first") + """</a></li>
        """
    start = (current_page - 4) if (current_page - 4) > 0 else 1
    end = (current_page + 4) if ((current_page + 4) < total_pages) else total_pages
    for i in range(start, end):
        if current_page == i:
            html += """<li class="page-item active"><a class='page-link' href='javascript:void(0);' 
            onclick="ShowForm(this,EW.action.List,'""" + object_name + """',null,""" + str(i) + """,""" + size_options + """);" >""" + str(
                i) + """</a></li>"""
        else:
            html += """<li class="page-item"><a class='page-link active' href='javascript:void(0);' 
            onclick="ShowForm(this,EW.action.List,'""" + object_name + """',null,""" + str(i) + """,""" + size_options + """)" >""" + str(
                i) + """</a></li>"""
        i += 1
    # only show if not on the last page
    if current_page != total_pages:
        html += """
        <li class="page-item"><a class="page-link" href='javascript:void(0);' 
        onclick="ShowForm(this,EW.action.List,'""" + object_name + """',null,""" + str(
            total_pages) + """,""" + size_options + """);" >""" + Lang.phrase("pagination_last") + """</a></li>
        """
    html += """<li class="page-item">
                   <label class="btn btn-md bg-info">Showing """ + str((current_page - 1) * records_per_page) \
            + """ to """ + str(current_page * records_per_page) + """ of """ + str(total_records) + """ </label>
                   """
    html += "</ul>"
    return html


def is_empty(x):
    try:
        if x is None or str(x) == "":
            return True
        else:
            return False
    except:
        return True


def is_integer(x):
    try:
        return float(x).is_integer()
    except:
        return False


def is_float(x):
    try:
        float(x)
        return True
    except:
        return False


def is_datetime(x):
    try:
        from datetime import datetime
        datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False

def is_date(x):
    try:
        from datetime import datetime
        datetime.strptime(str(x), '%Y-%m-%d')
        return True
    except:
        return False


def is_email( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( str(email) )
        return True
    except ValidationError:
        return False

def contains_a_number(string):
    for x in ["0","1","2","3","4","5","6","7","8","9"]:
        if x in str(string):
            return True
    return False


def is_phone_number(string):
    try:
        if str(string).__len__() == 10 and is_integer(str(string)) is True:
            return True
        else:
            return False
    except:
        return False



def convert_to_bool(value):
    if str(value).lower() in ["yes", "true", "t", "1"]:
        return True
    elif str(value).lower() in ["no", "false", "f", "0"]:
        return False
    else:
        return None

def convert_to_int(value):
    if is_integer(value)is True:
        return int(float(value))
    else:
        return None

def convert_to_float(value):
    if is_float(value)is True:
        return float(value)
    else:
        return None

def convert_to_datetime(value,date_format = ""):
    try:
        import datetime
        import re
        # if its already a datetime format
        if type(value) is datetime.date or type(value) is datetime.datetime:
            return value
        #  if a desired format is provided then use it
        elif type(value) is str and is_empty(date_format) is False:
            return datetime.datetime.strptime(value, date_format)
        # if not format passed then try default known formats
        elif type(value) is str and re.compile('.*-.*-.* .*:.*:.*').match(value) is not None:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif type(value) is str and re.compile('.*-.*-.*').match(value) is not None:
            return datetime.datetime.strptime(value, '%Y-%m-%d')
    except:
        return None

def strip_accents(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def clean_file_name(file_name):
    file_name = str(file_name)
    # remove extra spaces
    file_name = str(file_name).strip()
    # remove french characters
    translationTable = str.maketrans("éàèùâêîôûç", "eaeuaeiouc")
    file_name = file_name.translate(translationTable)
    # remove special characters
    import re
    file_name = re.sub(r'[\\/*?:"<>|]', "", file_name)
    # remove percentage sign
    file_name = file_name.replace("%", "")
    # remove quotes coz of intefernace with JS
    file_name = file_name.replace("'", "")
    file_name = file_name.replace("`", "")
    file_name = file_name.replace('"', '')
    #remove accent chaarcters
    file_name = strip_accents(file_name)
    return file_name


def excel_export(data, file_name='excel_export.xls'):
    import pyexcel
    # data = [{'name': 'shem', 'Age': 30, 'Sex': 'Male'}, {'name': 'James', 'Age': 40, 'Sex': 'Female'}]
    from django_jailuapp.settings import MEDIA_ROOT
    import os
    # clean file name
    file_name = clean_file_name(file_name)
    filename = os.path.join(MEDIA_ROOT, 'temp', file_name)
    #  filename = BASE_DIR + '/JailuApp/uploads/temp/' + file_name
    pyexcel.save_as(array=data, dest_file_name=filename)
    return file_name

def delete_file(source_file_url):
    response = {"error": True, "error_msg": "Failed to delete"}
    try:
        from django.core.files.storage import FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.delete(source_file_url)
        response["error"] = False
        response["error_msg"] = "Success"
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to save file eroor:"+str(x)
    return response

def copy_file(source_file_url, destination_file_url):
    response = {"error": True, "error_msg": "Failed to upload"}
    try:
        from django.core.files.storage import FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(destination_file_url, fs.open(source_file_url))
        uploaded_file_url = fs.url(filename)
        # from shutil import copy
        # uploaded_file_url = copy(source_file_url, destination_file_url)
        response["error"] = False
        response["error_msg"] = "Success"
        response["uploaded_file_url"] = filename
        response["uploaded_file_name"] = filename[filename.rfind("/")+1:]
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to save file eroor:"+str(x)
    return response


def generate_pdf(html_text,destination_file_url, options = {'quiet': ''}):
    response = {"error": True, "error_msg": "Failed to upload"}
    try:
        import os
        #This application failed to start because it could not find or load the Qt platform plugin "localhost".
        #Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, xcb.
        # set the display variable avoid QXcbConnection: Could not connect to display
        os.environ['QT_QPA_PLATFORM'] = 'linuxfb'
        import pdfkit

        pdfkit.from_string(html_text, destination_file_url,options)
        response["error"] = False
        response["error_msg"] = "Success"
        #response["uploaded_file_url"] = destination_file_url
        #response["uploaded_file_name"] = destination_file_url[destination_file_url.rfind("/") + 1:]
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to create pdf file eroor:" + str(x)
    return response


def upload_temp_file(myfile, suggested_file_name):
    response = {"error": True, "error_msg": "Failed to upload"}
    try:
        # clean file name
        suggested_file_name = clean_file_name(suggested_file_name)
        from django_jailuapp.settings import MEDIA_ROOT
        import os
        saved_filename = os.path.join(MEDIA_ROOT, 'temp', suggested_file_name)
        from django.core.files.storage import FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(saved_filename, myfile)
        uploaded_file_url = fs.url(filename)
        response["error"] = False
        response["error_msg"] = "Success"
        response["uploaded_file_url"] = filename
        response["uploaded_file_name"] = filename[filename.rfind("/")+1:]
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to save file eroor:"+str(x)
    return response


def open_cvs_file(source_file_url):
    response = {"error": True, "error_msg": "Failed to upload", "headers":None, "data":None}
    try:
        import csv
        file = open(source_file_url, "r")
        csv_reader = csv.DictReader(file)
        headers = csv_reader.fieldnames
        data = list()
        for row in csv_reader:
            # collect actual data as a dicionary of the heading
            data.append(dict(row))
        #compile response
        response["error"] = False
        response["headers"] = headers
        response["data"] = data
        response["error_msg"] = "Success"
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to open file error:"+str(x)
    return response


def current_datetime():
    from datetime import datetime
    #return datetime.today()
    import pytz
    return datetime.now(pytz.timezone(EW.default_timezone))


def current_user_id():
    return Security.user_account_id


def get_short_month(monthinteger):
    try:
        import datetime
        return datetime.date(1900, int(monthinteger), 1).strftime("%b")
    except:
        return monthinteger


def get_date_only_str(value):
    try:
        import datetime
        #datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')
        if type(value) is datetime.date or type(value) is datetime.datetime:
            return value.strftime("%a-%d-%b")
        elif type(value) is str:
            date = datetime.datetime.strptime(value, '%Y-%m-%d')
            return date.strftime("%a-%d-%b")
    except:
        return str(value)


def time_elapsed_str(past_time,full = True,current_time = None):
    try:
        import datetime
        # auto set now_time  to now if not specified
        if current_time is None:
            current_time = datetime.datetime.now()
        # convert to datetime if string
        import re
        if type(past_time) is str and re.compile('.*-.*-.* .*:.*:.*').match(past_time) is not None:
            past_time = datetime.datetime.strptime(past_time, '%Y-%m-%d %H:%M:%S')
        elif type(past_time) is str and re.compile('.*-.*-.*').match(past_time) is not None:
            past_time = datetime.datetime.strptime(past_time, '%Y-%m-%d')

        ela = (current_time - past_time)
        total_seconds = ela.total_seconds()
        elapsed_str = ""
        if total_seconds >= (60 * 60 * 24) and (full is False or (full is True and elapsed_str == "")):
            elapsed_str += " "+ str(int(total_seconds // (60 * 60 * 24))) + "Days"
            total_seconds -= ((total_seconds // (60 * 60 * 24)) * (60 * 60 * 24))
        if total_seconds >= (60 * 60) and (full is False or (full is True and elapsed_str == "")):
            elapsed_str += " "+ str(int(total_seconds // (60 * 60))) + "Hrs"
            total_seconds -= ((total_seconds // (60 * 60)) * (60 * 60))
        if total_seconds >= (60) and (full is False or (full is True and elapsed_str == "")):
            elapsed_str += " "+ str(int(total_seconds // (60))) + "mins"
            total_seconds -= ((total_seconds // (60)) * (60))
        if total_seconds >= 0 and (full is False or (full is True and elapsed_str == "")):
            elapsed_str += " "+ str(int(total_seconds)) + "secs"
        return str(elapsed_str)
    except:
        return "Unknown"

def record_system_log(table_name,record_id,operation_type,operation_summary,full_description):
    from JailuApp.models import SystemLog
    SystemLog(id=new_guid()
                , entry_date=current_datetime()
                , table_name=table_name
                , record_id=record_id
                , operation_type=operation_type
                , operation_summary=operation_summary
                , full_description=full_description
                , user_id=current_user_id()
                , account_name=Security.user_full_names()
                ).save()


def generate_tour_data():
    steps = []

    steps.append({
        "intro": "Hello " + Security.user_full_names() + ",<br> Welcome to " +Lang.phrase("site_title") + " System. Let us go through a few things to help u familiarise yourself with the system.",
         "position": 'center',
        })



    return {"steps": steps}



def smtp_send_email(to_emails,subject,body_plain_text, body_html,attachments = None):
    response = {"error": True, "error_msg": "Failed to send email"}
    try:
        from django.core.mail import send_mail, EmailMessage
        from django_jailuapp.settings import EMAIL_HOST_USER
        #decide what to use if has attachments
        if attachments == None:
            send_mail(subject, body_plain_text, EMAIL_HOST_USER, to_emails,fail_silently=False,
                  auth_user=None, auth_password=None, connection=None, html_message=body_html)
        else:
            #obj_mail = EmailMessage(subject, body_html, EMAIL_HOST_USER, to_emails)
            obj_mail = EmailMessage(subject, body_html, EMAIL_HOST_USER, to_emails)
            obj_mail.content_subtype = "html"
            # add atachments
            for x in attachments:
               obj_mail.attach_file(x)
            obj_mail.send(False)
        response["error"] = False
        response["error_msg"] = "Success"
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to send email error:" + str(x)
    return response


def template_email():
    html = """ 
         <table border="1" cellspacing="0" style="background-color:white; border-collapse:collapse; border-spacing:0; border:1px solid #d2d2d2; margin:20px; text-align:justify; width:600px">
            <tbody>
                <tr>
                    <td>
                    <table style="border-bottom:6px solid green; width:100%">
                        <tbody>
                            <tr>
                                <td>
                                <table align="left" border="0">
                                    <tbody>
                                        <tr>
                                            <td>
                                            <div style="margin-bottom:10px"><span style="color:green">&nbsp;</span></div>
                                            [[email_subject]]
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                                </td>
                                <td>
                                <table border="0" style="height:30px; width:49px">
                                    <tbody>
                                        <tr>
                                            <td style="vertical-align:middle">
                                            <div><img src='[[email_site_logo]]' style="border-width:0px; height:57px; width:144px" /></div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                        </tbody>
                    </table>
        
                    <table style="width:100%">
                        <tbody>
                            <tr>
                                <td>
                                <div>
                                <div style="margin-bottom:14pt; margin-top:14pt">Dear [[email_full_names]],</div>
        
                                <div style="margin-bottom:14pt; margin-top:14pt">
                                [[email_body_content]]
                                <br />
                                Best regards!<br />
                                """ + Lang.phrase("site_title") + """ Team</div>
                                </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <img src='[[email_site_logo]]' style="border-width:0px; height:57px; width:144px" />
                    <table style="height:45px; width:242px">
                        <tbody>
                            <tr>
                                <td style="vertical-align:middle">
                                <div><strong>Do Not Reply to this email</strong></div>
        
                                <div><span style="color:#6f6f6f; font-size:x-small"><span style="font-size:11px">This email is sent to [[email_full_names]].</span></span></div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    </td>
                </tr>
            </tbody>
        </table>

         """
    # deal with logo
    email_site_logo = EW.notification_click_url + "/static/images/app_logo.png"
    html = html.replace("[[email_site_logo]]", email_site_logo)
    return html


def number_to_word(num):
    try:
        from num2words import num2words
        return num2words(num)
    except Exception as x:
        return str(num)


def add_thousand_separator(num):
    try:
        return f"{num:,}"
    except Exception as x:
        return str(num)


def custom_round(value, ndigits):
    try:
        # round off and mantain trailing zeros if neccessary
        rounded_str = format(value, "." + str(ndigits) + "f")
        from decimal import Decimal
        rounded_num = Decimal(rounded_str)
        return rounded_num
    except Exception as x:
        return None







