import tkinter as tk
import replace_content_php_ini as rcpi
import os

def do_php_ini_change(php_ini_path: str, php_var: int, apc_var: int):
    php_change = rcpi.PhpIniChange()
    php_change.execute_changes_in_php_ini(php_ini_path, php_var, apc_var)
    output_msgs = ', \n'.join(php_change.get_msgs())
    output_msgs += '\n----- Error Messages -----\n'
    output_msgs += ', \n'.join(php_change.get_errors())
    txt_area_msgs.insert(tk.INSERT, output_msgs)


is_root = bool(os.geteuid() == 0)

window = tk.Tk()
window.geometry('550x200')

grid_row = 0
php_set = tk.IntVar()
apc_set = tk.IntVar()
root_bool = tk.BooleanVar()

label_path = tk.Label(window, text='Path to PHP.ini: ')
edit_path = tk.Entry(window, width=32)
if is_root:
    edit_path.insert(0, '/etc/php/7.4/apache2/php.ini')
else:
    edit_path.insert(0, 'Please execute the program as root')
label_path.grid(row=grid_row, sticky='W')
grid_row += 1
edit_path.grid(row=grid_row, sticky='W')
grid_row += 1
check_root = tk.Checkbutton(window, text='Root', variable=root_bool, state=tk.DISABLED)
check_root.grid(row=grid_row, sticky='W')
if is_root:
    check_root.select()
grid_row += 1
check_php = tk.Checkbutton(window, text='Change PHP-Settings', variable=php_set, onvalue=1, offvalue=0)
check_php.grid(row=grid_row, sticky='W')
check_php.select()
grid_row += 1
check_apc = tk.Checkbutton(window, text='Insert APC-Settings', variable=apc_set, onvalue=1, offvalue=0)
check_apc.grid(row=grid_row, sticky='W')
check_apc.select()
grid_row += 1
txt_area_msgs = tk.Text(window, height=10, width=35)
txt_area_msgs.grid(row=1, column=1, rowspan=7, sticky='N')
btn_Change = tk.Button(window, text='Change php.ini', command=lambda: do_php_ini_change(edit_path.get(), php_set.get(), apc_set.get()))
btn_Change.grid(row=grid_row, sticky='W')
if not is_root:
    btn_Change.config(state=tk.DISABLED)
grid_row += 1
btn_quit = tk.Button(window, text='Quit', command=window.quit).grid(row=grid_row, pady=4, sticky='W')
grid_row += 1
label_output = tk.Label(window, text = 'Ausgabe')
label_output.grid(row=0, column=1, sticky='W')

#scrollbar_txt_area = tk.Scrollbar(txt_area_msgs, command=txt_area_msgs.yview)
#scrollbar_txt_area.grid()
#scrollbar_txt_area.config()



window.mainloop()
