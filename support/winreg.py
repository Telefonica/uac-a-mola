import _winreg as winreg


class Registry(object):

    def __init__(self):
        self.last_created = {'key': None,
                             'new_sk': None,
                             'existing_sk': None}
        self.no_restore = False

    def create_key(self, key, subkey):
        """ Creates a key THAT DOESN'T EXIST, we need
        to keep track of the keys that we are creating
        """
        self.no_restore = False
        self.non_existent_path(key, subkey)
        try:
            return winreg.CreateKey(key, subkey)

        except WindowsError as error:
            print "Error al crear clave"
            self.no_restore = True

    def restore(self, key, value=''):
        """ Restore to the last registry known state
        """
        if self.no_restore is False:
            new_sk = self.last_created['new_sk']
            k = self.last_created['key']
            exist_sk = self.last_created['existing_sk']

            self.del_value(key, value)

            if new_sk is not None:
                for i in range(len(new_sk)):
                    if i == 0:
                        try:
                            winreg.DeleteKey(k, "\\".join(exist_sk + new_sk))
                        except WindowsError as error:
                            pass
                    else:
                        try:
                            winreg.DeleteKey(k, "\\".join(
                                exist_sk + new_sk[:-i]))
                        except WindowsError as error:
                            pass

                self.last_created['new_sk'] = None
                self.last_created['existing_sk'] = None
                self.last_created['key'] = None

    def non_existent_path(self, key, subkey):
        """ In a path of a key, returns the portion of
        the path that doesn't exist
        """
        s = subkey.split('\\')
        for i in xrange(1, len(s) + 1):
            try:
                winreg.OpenKey(key, "\\".join(s[:i]))
            except WindowsError:
                self.last_created['key'] = key
                self.last_created['new_sk'] = s[i - 1:]
                self.last_created['existing_sk'] = s[:i - 1]
                return "\\".join(s[i - 1:])

    def set_value(self, key, subkey, value):
        try:
            return winreg.SetValue(key, subkey, winreg.REG_SZ, value)
        except WindowsError as error:
            print "Error al crear un valor"
            self.no_restore = True

    def del_value(self, key, value=''):
        if self.no_restore is False:
            try:
                return winreg.DeleteValue(key, value)
            except WindowsError as error:
                print "Error al eliminar el valor"

    def create_value(self, key, value_name, value):
        """ Creates a value THAT DOESN'T EXIST, we need
        to keep track of the keys that we are creating
        """
        self.no_restore = False
        try:
            return winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)
        except WindowsError as error:
            print "Error al crear clave"
            self.no_restore = True
