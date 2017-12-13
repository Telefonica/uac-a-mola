from agent import Agent

fodhelper_ag = Agent('fodhelper.exe', 'localhost', 5555, 'uacamola')
fodhelper_ag.send_forbidden("Software\\Classes\\ms-settings\\Shell\\Open\\command")

