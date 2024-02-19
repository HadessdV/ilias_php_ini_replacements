import argparse
import os

settings_names = {
    'max_execution_time': '600',
    'max_input_vars': '10000',
    'memory_limit': '512M',
    'post_max_size': '512M',
    'upload_max_filesize:': '512M',
    'error_reporting': 'E_ALL & ~E_DEPRECATED & ~E_STRICT & ~E_NOTICE',
    'display_errors': 'On',
    'session.gc_probability' : '1',
    'session.gc_divisor' : '100',
    'session.gc_maxlifetime' : '14400',
    'session.hash_function' : '0',
    'session.cookie_httponly' : 'On',
    'session.save_handler' : 'files',
    'session.cookie_secure' : 'On',
    'allow_url_fopen': 'On', 
    'opcache.enable':'1',
    'opcache.enable_cli':'1',
    'opcache.interned_strings_buffer':'8',
    'opcache.max_accelerated_files':'10000',
    'opcache.memory_consumption':'128',
    'opcache.save_comments':'1',
    'opcache.revalidate_freq':'1'
}

apc_names = [
    'apc.enabled=1\n',
    'apc.shm_size=256M\n',
    'apc.ttl=7200\n',
    'apc.enable_cli=1\n',
    'apc.gc_ttl=3600\n',
    'apc.entries_hint=4096\n',
    'apc.slam_defense=1\n',
    'apc.serializer=igbinary\n'
]

def add_lines_at_end(php_ini_lines: list) -> list:
    """add lines at the end of the php.ini

    Args:
        php_ini_lines (list): php.ini lines as list

    Returns:
        list: php.ini files lines with added lines
    """
    for line in php_ini_lines:
        if apc_names[0] in line:
            print('APC Settings already in php.ini')
            return php_ini_lines
    return php_ini_lines.extend(apc_names)


def replace_php_setting(settings: dict, line: str) -> str : 
    """replace php.ini setting if found in line

    Args:
        line (str): line of php.ini-file
        settings (dict): dicionary with settings key/values in it

    Returns:
        str: combined string parameter with value
    """
    for key in settings:
        if key in line:
            if '=' in line and not 'second' in line and 'cli' not in line:
                result = key + "=" + settings[key]
                return result

def execute_changes_in_php_ini(php_arg: int = 0, apc_arg: int = 0) -> bool:
    """replace settings in php.ini with key_value_settings in local dictionarys

    Returns:
        bool: did the code got through till return true?
    """
    if php_arg == 0 and apc_arg == 0:
        print('Arguments where both 0, please add arguments like "-php=1" or "-apc=1" to change values in php.ini for these settings\n')
        return False

    php_ini_path = ''
    php_ini_usual_path = '/etc/php/7.4/apache2/php.ini'
    if os.path.exists(php_ini_usual_path):
        print('php.ini datei existiert')
        php_ini_path = php_ini_usual_path

    else:
        print('php.ini-Datei existiert nicht, bitte geben Sie den richtigen Pfad ein:')
        php_ini_path = input()

    #check if you got read/write access
    if os.access(php_ini_path, os.R_OK):
        print('read access is given')
    else:
        print('read access is NOT given')
    if os.access(php_ini_path, os.W_OK):
        print('write access is given')
    else:
        print('write access is NOT given')        

    with open(php_ini_path, 'r') as file:
        if php_arg == 1:
            print('I will update the php-settings')
        file_data = file.readlines()
        for counter, line in enumerate(file_data):
            if replace_php_setting(settings_names, line):
                file_data[counter] = replace_php_setting(settings_names, line)
        if apc_arg == 1:
            print('I will add apc-settings at the end of the php.ini')        
            add_lines_at_end(file_data)                

    size_file_data = len(file_data)

    if size_file_data > 0:
        with open(php_ini_path, 'w+') as file_write:
            file_write.writelines(file_data)
            pass

    return True

if __name__ == "__main__":  
    worked = False
    parser = argparse.ArgumentParser(description='Do it')
    parser.add_argument("-apc", type=int, default=1)
    parser.add_argument("-php", type=int, default=1)
    args = parser.parse_args()
    arg_values = vars(args)
    worked = execute_changes_in_php_ini(arg_values['php'], arg_values['apc'])
    if worked:
        print('Changes for php.ini completed')
    else:
        print('Changes for php.ini didnt succeed or was not activated')