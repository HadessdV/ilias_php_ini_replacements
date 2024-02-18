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
    'opcache.revalidate_freq':'1',
}

apc_names = {
    'apc.enabled':'1',
    'apc.shm_size':'256M',
    'apc.ttl':'7200',
    'apc.enable_cli':'1',
    'apc.gc_ttl':'3600',
    'apc.entries_hint':'4096',
    'apc.slam_defense':'1',
    'apc.serializer':'igbinary',
}

def replace_php_setting(line: str) -> str : 
    """replace php.ini setting if found in line

    Args:
        line (str): line of php.ini-file

    Returns:
        str: combined string parameter with value
    """
    for key in settings_names:
        if key in line:
            if '=' in line and not 'second' in line and 'cli' not in line:
                return key + "=" + settings_names[key]

def execute_replacements_in_php_ini() -> bool:
    with open('php.ini', 'r') as file:
        file_data = file.readlines()
        for counter, line in enumerate(file_data):
            if replace_php_setting(line):
                file_data[counter] = replace_php_setting(line) + "\n"

    size_file_data = len(file_data)

    if size_file_data > 0:
        with open('php.ini', 'w+') as file_write:
            file_write.writelines(file_data)
    return True

if __name__ == "__main__":
    worked = execute_replacements_in_php_ini()
    if worked:
        print('Replacement completed')