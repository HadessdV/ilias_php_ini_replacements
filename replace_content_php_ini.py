import argparse
import os

class PhpIniChange:
    def __init__(self):
        self.errors = []
        self.msgs = []

        self.settings_names = {
            'max_execution_time': '600',
            'max_input_vars': '10000',
            'memory_limit': '512M',
            'post_max_size': '512M',
            'upload_max_filesize:': '512M',
            'error_reporting': 'E_ALL & ~E_DEPRECATED & ~E_STRICT & ~E_NOTICE',
            'display_self.errors': 'On',
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

        self.apc_names = [
            'apc.enabled=1\n',
            'apc.shm_size=256M\n',
            'apc.ttl=7200\n',
            'apc.enable_cli=1\n',
            'apc.gc_ttl=3600\n',
            'apc.entries_hint=4096\n',
            'apc.slam_defense=1\n',
            'apc.serializer=igbinary\n'
        ]

    def __add_error(self, error_msg: str):
        self.errors.append(error_msg)

    def __add_msgs(self, msg: str):
        self.msgs.append(msg)

    def __add_lines_at_end(self, php_ini_lines: list) -> list:
        """add lines at the end of the php.ini

        Args:
            php_ini_lines (list): php.ini lines as list

        Returns:
            list: php.ini files lines with added lines
        """
        for line in php_ini_lines:
            if self.apc_names[0] in line:
                self.__add_error('APC Settings already in php.ini')
                return php_ini_lines
        return php_ini_lines.extend(self.apc_names)


    def __replace_php_setting(self, settings: dict, line: str) -> str : 
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

    def execute_changes_in_php_ini(self, php_ini_path: str, php_arg: int = 0, apc_arg: int = 0, ) -> bool:
        """replace settings in php.ini with key_value_settings in local dictionarys

        Returns:
            bool: did the code got through till return true?
        """
        if php_arg == 0 and apc_arg == 0:
            self.__add_error('Arguments where both 0, please add arguments like "-php=1" or "-apc=1" to change values in php.ini for these settings\n')
            return False

        if os.path.exists(php_ini_path):
            self.__add_msgs('php.ini datei existiert')
        else:
            self.__add_error('php.ini not at directory')
            return False

        #check if you got read/write access
        if os.access(php_ini_path, os.R_OK):
            self.__add_msgs('read access is given')
        else:
            self.__add_error('read access is NOT given')
        if os.access(php_ini_path, os.W_OK):
            self.__add_msgs('write access is given')
        else:
            self.__add_error('write access is NOT given') 
            return False       

        with open(php_ini_path, 'r') as file:
            if php_arg == 1:
                self.__add_msgs('I will update the php-settings')
            file_data = file.readlines()
            for counter, line in enumerate(file_data):
                if self.__replace_php_setting(self.settings_names, line):
                    file_data[counter] = self.__replace_php_setting(self.settings_names, line)
            if apc_arg == 1:
                self.__add_msgs('I will add apc-settings at the end of the php.ini')        
                self.__add_lines_at_end(file_data)                

        size_file_data = len(file_data)

        if size_file_data > 0:
            with open(php_ini_path, 'w+') as file_write:
                file_write.writelines(file_data)
                pass

        return True

    def get_msgs(self) -> list:
        return self.msgs

    def get_errors(self) -> list:
        return self.errors

if __name__ == "__main__":  
    worked = False
    parser = argparse.ArgumentParser(description='Do it')
    parser.add_argument("-apc", type=int, default=1)
    parser.add_argument("-php", type=int, default=1)
    args = parser.parse_args()
    arg_values = vars(args)
    php_change = PhpIniChange()
    worked = php_change.execute_changes_in_php_ini('/etc/php/7.4/apache2/php.ini', arg_values['php'], arg_values['apc'])
    if worked:
        print('Changes for php.ini completed')
        print('Meldungen: ')
        print(php_change.get_msgs())
        print('Errors: ')
        print(php_change.get_errors())
    else:
        print('Errors which lead to problems:')
        print(php_change.get_errors())        