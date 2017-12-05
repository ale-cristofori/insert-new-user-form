import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
sys.path.append(r"C:\WinPython-64bit-3.4.4.5Qt5\QtPythonFiles")
# print("the sys path is {0}".format(sys.path))
from UiComponents import LocalViewNewUser_Ui

""""
This is a Qt 5 based application I created to insert automatically new users
and their details into some Postgres tables. The credentials are then used
by a webGIS application to let user access the different application websites
"""

class LocalViewNewUser:
    """
    class that holds together all the back end functions
    of the insert new user form, event handling and
    DB communication
    """
    def __init__(self):
        # initialising radio buttons initial status
        self.host_id_model = None
        self.site_id_model = None
        self.selected_host_id = None
        self.selected_site_id = None
        self.user_roles_dict = {'adminRadioButton': 'A', 'userRadioButton': 'U'}
        self.user_group_dict = {'groupFalseRadioButton': 'F', 'groupTrueRadioButton': 'T'}
        # set up window layout
        app = QtWidgets.QApplication(sys.argv)
        win = QtWidgets.QMainWindow()
        self.new_user_win = LocalViewNewUser_Ui.Ui_MainWindow()
        self.new_user_win.setupUi(win)
        # set up user interaction signals
        self.setup_navigation_model()
        # initialise database - in this case Postgres
        self.db = QtSql.QSqlDatabase('QPSQL')
        if not self.setup_db():
            db_error_msg = self.db.lastError().text()
            no_text_alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "DB Error",
                                                  db_error_msg, QtWidgets.QMessageBox.Ok)
            no_text_alert.exec_()
        else:
            # initialise list view
            self.populate_host_id()
            win.show()
            sys.exit(app.exec_())

    def setup_navigation_model(self):
        # connecting signals from buttons and list to events
        self.new_user_win.addUserPushButton.clicked.connect(self.add_user)
        self.new_user_win.hostIdListView.clicked.connect(self.populate_site_id)
        self.new_user_win.siteIdListView.clicked.connect(self.get_site_id)

    def setup_db(self):
        # live host
        self.db.setHostName('dbhost')
        # port
        self.db.setPort(5432)
        # live db
        self.db.setDatabaseName('dbname')
        self.db.setUserName('dbuser')
        # live password
        self.db.setPassword('dbpassword')
        # internet password
        db_open = self.db.open()
        return db_open

    def populate_host_id(self):
        """
        initial host id list population
        :return: void
        """
        # initialisation of the query model
        self.host_id_model = QtSql.QSqlQueryModel()
        # select all host ids
        self.host_id_model.setQuery("SELECT host_desc, host_id FROM lv_hosts WHERE is_active = 'Y'", self.db)
        if self.host_id_model is None:
            self.null_id_error("Cannot find host_ids from lv_host table")
            raise TypeError
        # set query model to host id query
        self.new_user_win.hostIdListView.setModel(self.host_id_model)

    def populate_site_id(self):
        """
        this function is fired up when the user selects an item
        from the host id list view
        site id list population, passing the host id to the
        query only those sites within a certain host
        :return: void
        """
        self.selected_site_id = None
        site_id_sql = "SELECT site_title, site_id FROM lv_sites WHERE is_active = 'Y' AND host_id = '{0}'"
        # queries the DB to select the site ids linked to the selected host id
        self.site_id_model = self.get_model(site_id_sql, self.new_user_win.hostIdListView)
        if self.site_id_model is None:
            self.null_id_error("Cannot find site_ids from lv_sites table")
            raise TypeError
        # set the site id model to the site id list view
        self.new_user_win.siteIdListView.setModel(self.site_id_model)

    def get_model(self, id_sql, list_view):
        """
        this functions gets the selected host id index to retrieve all
        site ids linked to a particular host id. The index id from the
        selected item in the host id list and the query is
        :return: [Qsql.QueryModel] the selected site id queried model
        according to the selected host id
        """
        # get the selected host id index
        id_selected_row = list_view.selectedIndexes()[0].row()
        # get the host id associated with the selected index
        self.selected_host_id = self.host_id_model.index(id_selected_row, 1).data()
        # attach the host id to the query
        id_sql = id_sql.format(self.selected_host_id)
        # queries the DB and returns the site id model
        id_query = QtSql.QSqlQuery(id_sql, self.db)
        id_model = QtSql.QSqlQueryModel()
        id_model.setQuery(id_query)
        return id_model

    def get_site_id(self):
        """
        this function is fired up when the user selects
        an item from the site id listview.
        gets the selected site id from the site id listview/model when the user
        :return:
        """
        # gets the index
        site_selected_row = self.new_user_win.siteIdListView.selectedIndexes()[0].row()
        # gets the data associated with the selected index
        self.selected_site_id = self.site_id_model.index(site_selected_row, 1).data()
        if self.selected_site_id is None:
            self.null_id_error("Cannot find site_id for selected site")
            raise TypeError

    def add_user(self):
        """
        function that is fired up when the user clicks on the "Add User" button
        this functions gets all the relevant data from the form and attaches
        other information, and format the INSERT query for a new user
        :return: void
        """
        # get user name from text box
        new_user = self.new_user_win.newUserLineEdit.text()
        # check that is not empty
        if new_user == "":
            self.null_id_error("User Name cannot be empty")
            return
        # check that at least host_id or site_id are selected
        if self.selected_host_id is None or self.selected_site_id is None:
            self.null_id_error("No host_id or site_id found for selected record, check database")
            return
        # get the latest changeset value from DB
        change_set = self.get_change_set()
        # check that change set exists
        if change_set is None:
            self.null_id_error("No change_set found on db, please check database")
            return
        # gets the selected radio button to get if user is admin or user
        user_role = self.get_role_group(self.new_user_win.userRoleGroupBox.children(), self.user_roles_dict)
        # throws error is no role radio button is selected
        if user_role is None:
            self.null_id_error("Please select a user role")
            return
        # gets the selected radio button to get if user is group True or group False
        is_group = self.get_role_group(self.new_user_win.isGroupGroupBox.children(), self.user_group_dict)
        # throws error is no group radio button is selected
        if is_group is None:
            self.null_id_error("Please select a user group")
            return
        # sends the relevant information to the function that insert the data in the DB
        self.compose_insert(host_id=self.selected_host_id,
                            site_id=self.selected_site_id,
                            user_identity=new_user,
                            changeset=change_set,
                            is_group=is_group,
                            user_role=user_role)

    def compose_insert(self, **kwargs):
        """
        attach the relevant information the INSERT sql query to
        the live DB
        :param kwargs: information got from the widgets as dictionary
        :return: void
        """
        # sends the user name formatting to validation
        user_id = self.validate_user_name(kwargs["user_identity"])
        # add default values to the arguments
        kwargs["source_repository"] = 'AD'
        kwargs["is_active"] = 'Y'
        # if the user id is valid proceed with insert
        if user_id:
            insert_message = ""
            # iterates through all arguments to get the values to insert
            for key, value in kwargs.items():
                item = "{0} : {1} \n".format(key, value)
                insert_message += item
            # composes the pre-insert warning message with all found arguments, and
            # shows the alert regards
            alert_result = self.warning_alert("You are about to insert the following user "
                                              "details into the live DB \n\n{0} \n"
                                              "Double check the details before continuing".format(insert_message))
            # if the user confirms the insert then proceed
            if alert_result == QtWidgets.QMessageBox.Yes:
                # formats the INSERT query
                sql_insert = "INSERT INTO lv_site_users " \
                             "(host_id, site_id, source_repository, is_group, user_identity, " \
                             "type_of_user, changeset, is_active) " \
                             "VALUES ('{0}', '{1}', '{2}', '{3}', E'{4}', '{5}', {6}, '{7}');"\
                             .format(kwargs['host_id'],
                                     kwargs['site_id'],
                                     kwargs['source_repository'],
                                     kwargs['is_group'],
                                     user_id,
                                     kwargs['user_role'],
                                     kwargs['changeset'],
                                     kwargs['is_active'])
                # sends the query string to the DB
                self.execute_insert(sql_insert)
        # if the user id is not valid end the process
        else:
            return

    def execute_insert(self, sql_insert):
        # queries the database and gets the insert result
        insert_user_query = QtSql.QSqlQuery(self.db)
        query_result = insert_user_query.exec_(sql_insert)
        # if the record has been inserted warn the user
        if query_result:
            self.info_alert("New User successfully inserted")
            return
        else:
            # if not inserted throws an error
            error_message = insert_user_query.lastError().text()
            self.null_id_error("ERROR: {0}".format(error_message))
            return

    def get_change_set(self):
        # gets the latest change set from the database
        change_set_sql = "SELECT changeset FROM lv_site_users WHERE is_active = 'Y' " \
                         "AND site_id = '{0}'  AND host_id = '{1}' " \
                         "ORDER BY changeset DESC LIMIT 1".format(self.selected_site_id,
                                                                  self.selected_host_id)
        change_set_query = QtSql.QSqlQuery(change_set_sql, self.db)
        if change_set_query.first():
            change_set_number = change_set_query.value(0)
            return change_set_number
        else:
            return None

    def validate_user_name(self, user_id):
        """
        Get the user name inserted into the text box and check if it may be
        a possible insert (format is ADDM\\username). If the insert seems to
        be incorrect, not adherent to the format, warns the user to confirm
        the user name they are about to insert.
        :param user_id: the user id passed is from the user id text box
        :return: [string] regex_result, final_name the validated user name
        """
        # escapes backslash
        final_name = user_id.replace('\\', '\\\\')
        # test if the format inserted is ADDM\xxxxx
        re_pattern = r'ADDM\\[a-zA-Z]+'
        user_id_regex = re.compile(re_pattern)
        # match the inserted id with the regex
        regex_match = user_id_regex.match(user_id)
        # if the user name is valid then re-format with escaping backslashes
        if regex_match:
            regex_result = regex_match.string.replace('\\', '\\\\')
            return regex_result
        else:
            # if the user name contains a forward slash (by mistake) stops the insertion
            if '/' in final_name:
                self.null_id_error("The user name contains non-allowed characters. \n"
                                   "Please amend")
                return
            # if the user name is different from the validation mask (ADDM\xxxxx) asks to confirm the username
            alert_result = self.warning_alert("Are you sure that you want to insert the user {0} ?".format(user_id))
            if alert_result == QtWidgets.QMessageBox.Yes:
                return final_name
            else:
                return

    """
    Below there are the classes to show the alert messages
    """

    """ error alert messagebox """
    @staticmethod
    def null_id_error(message):
        null_id_alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, " ",
                                              message, QtWidgets.QMessageBox.Ok)
        null_id_alert.exec_()

    """ warning alert messagebox """
    @staticmethod
    def warning_alert(message):
        warning_alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, " ",
                                              message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        alert_result = warning_alert.exec_()
        return alert_result

    """ info alert messagebox """
    @staticmethod
    def info_alert(message):
        info_alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, " ",
                                           message, QtWidgets.QMessageBox.Ok)
        info_alert.exec_()

    @staticmethod
    def get_role_group(obj_children, widget_dict):
        """
        get the associated value of the radio button for group and role
        :param obj_children: the Qt RadioButton instance
        :param widget_dict: the dictionary that links the selected
        radio button to the DB value (see self.role_dict, self.group_id)
        :return: [string] the radio button associated string to insert into the DB
        """
        widgets = {}
        # get the radio button in the selected group
        for radio_button in obj_children:
            if isinstance(radio_button, QtWidgets.QRadioButton):
                # creates a dictionary of the current radio button selection
                widgets[radio_button.objectName()] = radio_button.isChecked()
        # if there is a selected radio button proceed
        if True in widgets.values():
            for key, value in widgets.items():
                if value is True:
                    # return the value of the selected radio
                    # button in DB format ('A', 'U' for role - 'F', 'T' for group)
                    return widget_dict[key]
        # else stop the insertion
        else:
            return None

if __name__ == "__main__":
    LocalViewNewUser()
