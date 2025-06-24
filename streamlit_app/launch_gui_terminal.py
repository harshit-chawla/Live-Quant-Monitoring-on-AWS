import os, sys
import subprocess

code_name = 'Task Scheduler'
print(code_name)
if sys.platform == 'linux':
    print(f"\033]0;{code_name}\007")
elif sys.platform == 'win32':
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(code_name)

streamlit_script = os.path.expanduser('~/Desktop/cron_gui.py')
streamlit_cmd = '/home/ubuntu/.local/bin/streamlit'

# The actual command we want to run in bash
bash_command = f'cd "{os.path.dirname(streamlit_script)}" && "{streamlit_cmd}" run "{streamlit_script}"; exec bash'

# Launch terminal and run the command
subprocess.Popen([
    'xfce4-terminal',
    '--hold',
    '--command',
    'bash -c "{}"'.format(bash_command.replace('"', '\\"'))
])
