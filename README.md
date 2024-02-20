# ilias_php_ini_replacements
## replacing php.ini settings for better ilias functionality

### use-cases:
the standard php.ini of apache has some bad settings for working with the learning platform ILIAS
this python-scripts rewrites the settings in the code 
to the php.ini file which MUST BE in the SAME directory as the script

### preconditions:
**!USE SUDO/ROOT**, cause php.ini belongs to root!

### description of scripts:
replace_content_php_ini.py: script has a main so just execute the file
gui: build with tkinter, change button only active if gui is called with root-rights

### building a standalone/binary/executable:
**when adding pyinstaller to system or pip environment:**
python3 -m venv name_of_venv_folder_name
source name_of_venv_folder_name/bin/activate
pip(3) install pyinstaller
it is possible to generate a 
