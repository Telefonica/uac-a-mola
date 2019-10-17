![Supported Python versions](https://img.shields.io/badge/python-2/3-blue.svg?style=flat-square&logo=python)
![License](https://img.shields.io/badge/license-GNU-green.svg?style=flat-square&logo=gnu)

# uacamola-meterpreter

This is a lite version of uac-a-mola for the Python meterpreter.


## Built With

* [Python](https://www.python.org/download/releases/3.0/) - Programming language used
* [Ruby](https://www.ruby-lang.org/es/) - Programming language used

## Code Paths

Based on the Ubuntu installation for Metasploit 5, the paths where the files go are as follows:

* COMMAND DISPATCHER: /opt/metasploit-framework/embedded/framework/lib/rex/post/meterpreter/ui/console/command_dispatcher
* EXTENSION: /opt/metasploit-framework/embedded/framework/lib/rex/post/meterpreter/extensions
* PYTHON CODE: /opt/metasploit-framework/embedded/lib/ruby/gems/2.5.0/gems/metasploit-payloads-1.3.70/data/meterpreter/

### Prerequisites to use this version

To use this extension you need to have Metasploit and a python meterpreter running.


### How to load uac-a-mola

```
meterpreter > load uacamola 
Loading extension uacamola...
uac-a-mola - UAC Bypass!
Extension developed by @josueencinar
Ideas Locas (CDO Telefonica)
Client running on Windows 10 (Build 17763)
Success.
meterpreter > start_uacamola 
uac-a-mola> 
```

## Authors

The uac-a-mola extension for the meterpreter has been created by the Ideas Locas team (CDO Telefonica). Developed by:

* **Pablo Gonzázlez Perez** - [@pablogonzalezpe](https://twitter.com/pablogonzalezpe)
* **Josué Encinar García** - [@JosueEncinar](https://twitter.com/JosueEncinar)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
