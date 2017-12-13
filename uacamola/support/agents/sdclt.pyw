from agent import Agent

sdclt_ag = Agent('sdclt.exe', 'localhost', 5555, 'uacamola')
sdclt_ag.send_forbidden("Software\\Classes\\exefile\\Shell\\Open\\command")

