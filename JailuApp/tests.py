from django.test import TestCase
from JailuApp.classes.base_structures import *
from JailuApp.classes.system_checkers import *



# Test basic functions
class BasicFunctionsTestCase(TestCase):

    def test_is_empty(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_empty(None), True, msg="None should be empty")
        self.assertEqual(is_empty(""), True, msg='"" should be empty')
        self.assertEqual(is_empty(''), True, msg="'' should be empty")
        self.assertEqual(is_empty("a"), False, msg='"a" should not be empty')
        self.assertEqual(is_empty(5), False, msg="5 should not be empty")
        self.assertEqual(is_empty(20.55), False, msg="20.55 should not be empty")

    def test_is_integer(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_integer(5), True, msg='5 is a valid integer')
        self.assertEqual(is_integer(-5745), True, msg='-5745 is a valid integer')
        self.assertEqual(is_integer(50.36), False, msg="50.36 is not a valid integer")
        self.assertEqual(is_integer(-200.36), False, msg="-200.36 is not a valid integer")
        self.assertEqual(is_integer(None), False, msg="None is not a valid integer")
        self.assertEqual(is_integer(''), False, msg="'' is not a valid integer")
        self.assertEqual(is_integer('value'), False, msg="'value' is not a valid integer")

    def test_is_float(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_float(5), True, msg='5 is a valid float')
        self.assertEqual(is_float(-5745), True, msg='-5745 is a valid float')
        self.assertEqual(is_float(50.36), True, msg="50.36 is a valid float")
        self.assertEqual(is_float(-200.36), True, msg="-200.36 is a valid float")
        self.assertEqual(is_float(None), False, msg="None is not a valid float")
        self.assertEqual(is_float(''), False, msg="'' is not a valid float")
        self.assertEqual(is_float('value'), False, msg="'value' is not a valid float")

    def test_is_datetime(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_datetime('2020-03-07 15:20:46'), True, msg='2020-03-07 15:20:46 is a valid datetime in format %Y-%m-%d %H:%M:%S')
        self.assertEqual(is_datetime('2020-20-07 15:20:46'), False, msg='months should not be out of range')
        self.assertEqual(is_datetime('2020-07-40 15:20:46'), False, msg='days should not be out of range')
        self.assertEqual(is_datetime(50.36), False, msg="numbers is not a valid datetime")
        self.assertEqual(is_datetime('value'), False, msg="strings is not a valid datetime")
        self.assertEqual(is_datetime('2020-03-07'), False, msg="Date only is not a valid datetime")
        self.assertEqual(is_datetime('2020-03-07 03:20:46 PM'), False, msg="Datetime should be in 24 hour format")

    def test_is_date(self):
        self.assertEqual(is_date('2020-03-07'), True, msg='2020-03-07 is a valid date in format %Y-%m-%d')
        self.assertEqual(is_date('2020-20-07'), False, msg='months should not be out of range')
        self.assertEqual(is_date('2020-07-40'), False, msg='days should not be out of range')
        self.assertEqual(is_date(50.36), False, msg="numbers is not a valid date")
        self.assertEqual(is_date('value'), False, msg="strings is not a valid date")
        self.assertEqual(is_date('2020-03-07 03:20:46'), False, msg="DateTime only is not a valid date")

    def test_excel_export(self):
        # """To correctly identify empty values"""
        self.assertEqual(excel_export([{'name': 'shem', 'Age': 30, 'Sex': 'Male'}
        , {'name': 'James', 'Age': 40, 'Sex': 'Female'}], 'test_export_excel.xls')
        , 'test_export_excel.xls', msg='Serer should be able to write excel files for download')

    def test_get_date_only_str(self):
        # """To correctly identify empty values"""
        import datetime
        self.assertEqual(get_date_only_str(None), None, msg="None should return None")
        self.assertEqual(get_date_only_str(""), "", msg='"" should be ""')
        self.assertEqual(get_date_only_str(datetime.date(2020, 1, 1)), "Wed-01-Jan", msg="Date object of 2020-01-01 should return Wed-01-Jan")
        self.assertEqual(get_date_only_str("2020-01-01"), "Wed-01-Jan", msg="string 2020-01-01 should return Wed-01-Jan")
        self.assertEqual(get_date_only_str("nothing"), "nothing", msg="Improper date or propoer date string should return itself")

    def test_get_short_month(self):
        # """To correctly identify empty values"""
        self.assertEqual(get_short_month(None), None, msg="None should be None")
        self.assertEqual(get_short_month(1), "Jan", msg='1 should be Jan')
        self.assertEqual(get_short_month(12), "Dec", msg='12 should be Dec')
        self.assertEqual(get_short_month("01"), "Jan", msg='string int 01 should be Jan')
        self.assertEqual(get_short_month('kl'), "kl", msg="invalid value should be themselves")


# test language functionality
class LanguageTestCase(TestCase):

    def setUp(self):
        self.en = Language("en")

    def test_english(self):
        self.assertEqual(self.en.phrase("btn_add"), "Save", msg="English btn_add should equal to Save")
        self.assertEqual(self.en.tbl_phrase("user_group"), "User Group"
                         , msg="English user_group caption should equal to User Group")
        self.assertEqual(self.en.fld_phrase("user_group","name"), "Group Name"
                         , msg="English user_group, name caption should equal to Group Name")
        self.assertEqual(self.en.phrase("12234"), "12234", msg="Unknown phrases should default to id")
        self.assertEqual(self.en.tbl_phrase("5451534"), "5451534"
                         , msg="Unknown table caption should default to ids")
        self.assertEqual(self.en.fld_phrase("5451534", "8562413"), "8562413"
                         , msg="Unknown field caption should default to id")
        self.assertEqual(self.en.men_phrase("mi_user_group"), "User Groups"
                         , msg="Unknown table caption should default to ids")
        self.assertEqual(self.en.men_phrase("5451534"), "5451534"
                         , msg="Unknown menu caption should default to ids")


# Test file operations
class FileOperationsTestCase(TestCase):

    def test_upload_into_possible_folders(self):
        from django_jailuapp.settings import MEDIA_ROOT
        import os
        sample_file = None # open sample file
        try:

            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()

            sample_file = fs.open(os.path.join(MEDIA_ROOT, 'sample_file.fileext'))
        except Exception as x:
            error = str(x)

        self.assertEqual(upload_temp_file(sample_file,'sample_file.fileext')["error"], False, msg="should be able to upload a file into media temp folder")
        self.assertEqual(copy_file(os.path.join(MEDIA_ROOT, 'temp', 'sample_file.fileext'), os.path.join(MEDIA_ROOT, 'some_folder', 'sample_file.fileext'))["error"], False, msg='"" should be able to upload into some_folder media folder')
        self.assertEqual(delete_file(os.path.join(MEDIA_ROOT, 'temp', 'sample_file.fileext'))["error"], False, msg='should be able to delete file from temp media folder')
        self.assertEqual(delete_file(os.path.join(MEDIA_ROOT, 'some_folder', 'sample_file.fileext'))["error"],False, msg='"" should be able to delete from some_folder media folder')
        self.assertEqual(delete_file(os.path.join(MEDIA_ROOT, 'temp', '1436271839.fileext1'))["error"], False,msg='delete should succedd even for non existing file')

    def test_open_cvs_file(self):
        from django_jailuapp.settings import MEDIA_ROOT
        import os

        self.assertEqual(open_cvs_file(os.path.join(MEDIA_ROOT, 'sample csv file.csv'))["error"], False, msg='"" should be able to read a csv file successfully')
        self.assertEqual(open_cvs_file(os.path.join(MEDIA_ROOT, 'empty csv file.csv'))["error"], False, msg='shouold be able to successfully read an empty csv file')
        self.assertEqual(open_cvs_file(os.path.join(MEDIA_ROOT, 'sample_file.fileext'))["error"], True,
                         msg='should fail if file is non csv format')

    def test_generate_pdf(self):
        sample_html = """
            <html>
              <head>
                <meta name="pdfkit-page-size" content="Legal"/>
                <meta name="pdfkit-orientation" content="Portrait"/>
              </head>
              <body style='width:100%;'>
              <table style='width:100%;'>
              <tr>
              <td style='color:red'>Red the shshs text</td>
              <td style='color:blue;'>blue text</td>
              <td style='color:black'>Red text</td>
              </tr>
              <tr>
              <td style='background-color:red'>Red the shshs back</td>
              <td style='background-color:red:blue;'>blue back</td>
              <td style='background-color:red:black'>Red back</td>
              </tr>
              </table>
              </body>
              </html>
            """
        from django_jailuapp.settings import MEDIA_ROOT
        import os
        pdf_export = generate_pdf(sample_html,os.path.join(MEDIA_ROOT, 'temp','sample_pdf.pdf'))
        self.assertEqual(pdf_export["error"], False, msg= pdf_export["error_msg"])


    def test_is_integer(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_integer(5), True, msg='5 is a valid integer')
        self.assertEqual(is_integer(-5745), True, msg='-5745 is a valid integer')
        self.assertEqual(is_integer(50.36), False, msg="50.36 is not a valid integer")
        self.assertEqual(is_integer(-200.36), False, msg="-200.36 is not a valid integer")
        self.assertEqual(is_integer(None), False, msg="None is not a valid integer")
        self.assertEqual(is_integer(''), False, msg="'' is not a valid integer")
        self.assertEqual(is_integer('value'), False, msg="'value' is not a valid integer")

    def test_is_float(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_float(5), True, msg='5 is a valid float')
        self.assertEqual(is_float(-5745), True, msg='-5745 is a valid float')
        self.assertEqual(is_float(50.36), True, msg="50.36 is a valid float")
        self.assertEqual(is_float(-200.36), True, msg="-200.36 is a valid float")
        self.assertEqual(is_float(None), False, msg="None is not a valid float")
        self.assertEqual(is_float(''), False, msg="'' is not a valid float")
        self.assertEqual(is_float('value'), False, msg="'value' is not a valid float")

    def test_is_datetime(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_datetime('2020-03-07 15:20:46'), True, msg='2020-03-07 15:20:46 is a valid datetime in format %Y-%m-%d %H:%M:%S')
        self.assertEqual(is_datetime('2020-20-07 15:20:46'), False, msg='months should not be out of range')
        self.assertEqual(is_datetime('2020-07-40 15:20:46'), False, msg='days should not be out of range')
        self.assertEqual(is_datetime(50.36), False, msg="numbers is not a valid datetime")
        self.assertEqual(is_datetime('value'), False, msg="strings is not a valid datetime")
        self.assertEqual(is_datetime('2020-03-07'), False, msg="Date only is not a valid datetime")
        self.assertEqual(is_datetime('2020-03-07 03:20:46 PM'), False, msg="Datetime should be in 24 hour format")

    def test_is_email(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_email(5), False, msg='numbers are a not an email')
        self.assertEqual(is_email(""), False, msg='empty strings are a not an email')
        self.assertEqual(is_email("first.last"), False, msg="first.last is not an email")
        self.assertEqual(is_email("first.last@mail"), False, msg="first.last@mail is not an email")
        self.assertEqual(is_email(' first.last@mail.com '), False, msg="gaps are not allowed in am email")
        self.assertEqual(is_email('first.last@mail.com'), True, msg="'first.last@mail.com' is an email")

    def test_contains_a_number(self):
        # """To correctly identify empty values"""
        self.assertEqual(contains_a_number(5), True, msg='numbers contains numbers')
        self.assertEqual(contains_a_number("5"), True, msg='number strings contains numbers')
        self.assertEqual(contains_a_number("testing"), False, msg='testing does not contains numbers')
        self.assertEqual(contains_a_number("testing 123"), True, msg='testing 123 contains numbers')
        self.assertEqual(contains_a_number("123 test"), True, msg='123 test contains numbers')

    def test_is_phone_number(self):
        # """To correctly identify empty values"""
        self.assertEqual(is_phone_number(5444), False, msg='5444 not a valid phone number')
        self.assertEqual(is_phone_number(1111111111), True, msg='1111111111 is a valid phone number')
        self.assertEqual(is_phone_number("0785047212"), True, msg='0785047212 is a valid phone number')
        self.assertEqual(is_phone_number("abcdefghik"), False, msg='1111111111 not a valid phone number')
        self.assertEqual(is_phone_number("078504721A"), False, msg='078504721A is not a valid phone number')
        self.assertEqual(is_phone_number("B785047212"), False, msg='078504721A is not a valid phone number')


    def test_convert_to_datetime(self):
        # """To correctly identify empty values"""
        import datetime
        self.assertNotEqual(convert_to_datetime('2020-03-07 15:20:46'), None, msg='dates of format %Y-%m-%d %H:%M:%S are convertable by default')
        self.assertNotEqual(convert_to_datetime('2020-03-07'), None,
                            msg='dates of format %Y-%m-%d are convertable by default')
        self.assertNotEqual(convert_to_datetime(datetime.datetime.now()), None,
                            msg='datetime objects are valid')
        self.assertNotEqual(convert_to_datetime('2020-03-07 15:20:46',"%Y-%m-%d %H:%M:%S"), None,
                            msg='converting using format %Y-%m-%d %H:%M:%S should work')
        self.assertNotEqual(convert_to_datetime('2020-03-07', "%Y-%m-%d"), None,
                            msg='converting using format %Y-%m-%d %H:%M:%S should work')
        self.assertEqual(convert_to_datetime('2020-03-07 15:20:46', "%Y-%m-%d"), None,
                            msg='converting using wrong format should NOT work')
        self.assertEqual(convert_to_datetime('2020-03-07', "%Y-%m-%d %H:%M:%S"), None,
                            msg='converting using wrong format should NOT work')
        self.assertNotEqual(convert_to_datetime('2020/03/07 15:20:46', "%Y/%m/%d %H:%M:%S"), None,
                            msg='converting using format %Y/%m/%d %H:%M:%S should work')
        self.assertNotEqual(convert_to_datetime('2020/03/07', "%Y/%m/%d"), None,
                            msg='converting using format %Y/%m/%d should work')
        self.assertNotEqual(convert_to_datetime('2020/03/07 15/20/46', "%Y/%m/%d %H/%M/%S"), None,
                            msg='converting using format %Y/%m/%d %H/%M/%S should work')
        self.assertNotEqual(convert_to_datetime('03/07/2020', "%m/%d/%Y"), None,
                            msg='converting using format %m/%d/%Y should work')
        self.assertEqual(convert_to_datetime(15105151), None, msg='intergers values should fail')
        self.assertEqual(convert_to_datetime(""), None, msg='empty string values should fail')
        self.assertEqual(convert_to_datetime(None), None, msg='empty values should fail')

    def test_clean_file_name(self):
        # """To correctly identify empty values"""
        self.assertEqual(clean_file_name("fileéàèùâêîôûçname.extension")
        , "fileeaeuaeioucname.extension", msg='should be able to remove french characters from file names')
        self.assertEqual(clean_file_name(" filename.extension ")
                         , "filename.extension", msg='should be able to remove extra spaces from file names')
        self.assertEqual(clean_file_name("""file\\/*?:"<>|name.extension""")
         , "filename.extension", msg='should be able to remove forbiden special characters characters from file names')
        self.assertEqual(clean_file_name("filename's`s name.extension")
                         , "filenamess name.extension", msg='should be able to remove quotes spaces from file names')



    def test_excel_export(self):
        # """To correctly identify empty values"""
        self.assertEqual(excel_export([{'name': 'shem', 'Age': 30, 'Sex': 'Male'}
        , {'name': 'James', 'Age': 40, 'Sex': 'Female'}], 'test_export_excel.xls')
        , 'test_export_excel.xls', msg='Serer should be able to write excel files for download')

    def test_make_imap_connection(self):
        gmail_test = make_imap_connection("imap.gmail.com", "smtpemailtestserver@gmail.com","smtp_email_test_server")
        nft_test = make_imap_connection("webmail.nftconsult.com", "shem.kironde@nftconsult.com","Passw0rd")
        server_off_test = make_imap_connection("imap.gmail.comm", "smtpemailtestserver@gmail.com", "smtp_email_test_server")
        invalid_login_test = make_imap_connection("imap.gmail.comm", "smtpemailtestserver@gmail.com", "wrong_password")
        self.assertEqual(gmail_test["error"], False, msg="gmail should be accessble. Error"+gmail_test["error_msg"])
        self.assertEqual(nft_test["error"], False, msg="nft should be accessible. Error" + nft_test["error_msg"])
        self.assertEqual(server_off_test["error"], True,
                         msg="Non existing server should fail" + server_off_test["error_msg"])
        self.assertEqual(invalid_login_test["error"], True,
                         msg="Invalid Logins should fail" + invalid_login_test["error_msg"])

    def test_smtp_send_email(self):
        gmail_test = smtp_send_email(['kirondedshem@gmail.com'], "SMTP test","testing SMTP email from python project","testing SMTP email from python project")
        nft_test = smtp_send_email(['shem.kironde@nftconsult.com'], "SMTP test","testing SMTP email from python project","testing SMTP email from python project")
        from django_jailuapp.settings import MEDIA_ROOT
        import os
        files = [os.path.join(MEDIA_ROOT, "sample_file.fileext")
                 , os.path.join(MEDIA_ROOT, "sample csv file.csv")]
        attachment_gmail_test = smtp_send_email(['kirondedshem@gmail.com'], "SMTP send file test", "testing SMTP email attaching files from python project",
                                     "testing SMTP email attching files from python project", files)
        attachment_nft_test = smtp_send_email(['shem.kironde@nftconsult.com'], "SMTP send file test",
                                   "testing SMTP email attching files from python project", "testing SMTP email attching files from python project", files)

        self.assertEqual(gmail_test["error"], False, msg="should be able to send to gmail. Error"+gmail_test["error_msg"])
        self.assertEqual(nft_test["error"], False, msg="should be able to send to nft email. Error" + nft_test["error_msg"])
        self.assertEqual(attachment_gmail_test["error"], False,
                         msg="should be able to send email attachments to gmail. Error" + attachment_gmail_test["error_msg"])
        self.assertEqual(attachment_nft_test["error"], False,
                         msg="should be able to send email attachments to nft email. Error" + attachment_nft_test["error_msg"])

    def test_number_to_word(self):
        # """To correctly identify empty values"""
        self.assertEqual(number_to_word(557), "five hundred and fifty-seven", msg='557 should be five hundred and fifty-seven')
        self.assertEqual(number_to_word(400.26), "four hundred point two six", msg='400.26 should be four hundred point two six')
        self.assertEqual(number_to_word(-58.23), "minus fifty-eight point two three", msg="-58.23  should be minus fifty-eight point two three")
        self.assertEqual(number_to_word("557"), "five hundred and fifty-seven", msg="numbers as string should still work")
        self.assertEqual(number_to_word(None), "None", msg="None should return string for None")
        self.assertEqual(number_to_word(""), "", msg="'' should return empty string")
        self.assertEqual(number_to_word("fff57657"), "fff57657", msg="invalid numbers like should return equivalent string formats")

    def test_add_thousand_separator(self):
        # """To correctly identify empty values"""
        self.assertEqual(add_thousand_separator(123), "123", msg='123 should be 123')
        self.assertEqual(add_thousand_separator(974.123), "974.123", msg='974.123 should be 974.123')
        self.assertEqual(add_thousand_separator(1000000), "1,000,000", msg='1000000 should be 1,000,000')
        self.assertEqual(add_thousand_separator(150000.23), "150,000.23", msg='150000.23 150,000.23')
        self.assertEqual(add_thousand_separator(-25000), "-25,000", msg="-25000  should be -25,000")
        self.assertEqual(add_thousand_separator("1000000"), "1000000", msg="numbers as string should not work")
        self.assertEqual(add_thousand_separator(None), "None", msg="None should return string for None")
        self.assertEqual(add_thousand_separator(""), "", msg="'' should return empty string")
        self.assertEqual(add_thousand_separator("fff57657"), "fff57657", msg="invalid numbers like should return equivalent string formats")

    def test_custom_round(self):
        # convert value to float for proper comparison between decimal anf flot values
        self.assertEqual(float(custom_round(123,0)), 123, msg='123 should be 123')
        self.assertEqual(float(custom_round(123, 2)), 123.00, msg='123 should be 123.00')
        self.assertEqual(float(custom_round(974.123,0)), 974, msg='974.123 should be 974')
        self.assertEqual(float(custom_round(974.123, 1)), 974.1, msg='974.123 should be 974.1')
        self.assertEqual(float(custom_round(974.123, 2)), 974.12, msg='974.123 should be 974.12')
        self.assertEqual(float(custom_round(974.564, 0)), 975, msg='974.564 should be 975')
        self.assertEqual(float(custom_round(974.564, 1)), 974.6, msg='974.564 should be 974.6')
        self.assertEqual(float(custom_round(974.564, 5)), 974.56400, msg='974.564 should be 974.56400')
        self.assertAlmostEqual(custom_round(None,None), None, msg="None should return string for None")
        self.assertAlmostEqual(custom_round(200, None), None, msg="None should return string for None")
        self.assertAlmostEqual(custom_round(None, 5), None, msg="None should return string for None")





