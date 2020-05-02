from src.constant import constant
from src.io_ import io
from src.usb import usb
from tkinter import *


def execute():
    # Display application
    root = Tk()
    root.geometry('500x300')
    root.resizable(0, 0)  # Prevent resizability and disable maximize button
    root.title(constant.__project__)
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=constant.ICON))

    """ First row """

    # Display label
    devices_label = Label(root, text='Configuration:')
    devices_label.grid(row=0, column=0, sticky=W)

    # Manage option menu
    files = io.get_files(constant.FIRMWARE)
    file_names = io.get_file_names(files)

    # Display option menu
    file_name = StringVar(root)

    if file_names:
        file_option_menu = OptionMenu(root, file_name, *file_names)

    else:
        file_option_menu = OptionMenu(root, file_name, file_names)

    file_option_menu.config(width=35)
    file_option_menu.grid(row=0, column=1, sticky=W)

    # Display button
    about_button = Button(root, text='About', command=lambda: show_about(root.winfo_rootx(), root.winfo_rooty()))
    about_button.grid(row=0, column=3, sticky=W)

    """ Second row """

    # Display label
    devices_label = Label(root, text='Device:')
    devices_label.grid(row=1, column=0, sticky=W)

    # Manage option menu
    devices = usb.get_devices([constant.VENDOR_ID, constant.BOOT_VENDOR_ID],
                                 [constant.PRODUCT_ID, constant.BOOT_PRODUCT_ID])
    device_names = usb.get_device_names(devices)

    # Display option menu
    device_name = StringVar(root)

    if constant.DEBUG:
        print(f'Devices: {devices}')
        print(f'Device Names: {device_names}')
        print(f'Device Name: {device_name}')

    if device_names:
        device_option_menu = OptionMenu(root, device_name, *device_names)

    else:
        device_option_menu = OptionMenu(root, device_name, device_names)

    device_option_menu.config(width=35)
    device_option_menu.grid(row=1, column=1, sticky=W)

    """ Third row """
    action = StringVar()
    action.set('r')

    # Display radio button
    Radiobutton(root, text='Read', variable=action, value='r').grid(row=2, column=0)
    Radiobutton(root, text='Test', variable=action, value='t').grid(row=2, column=1)
    Radiobutton(root, text='Write', variable=action, value='w').grid(row=2, column=2)

    # Display button
    ok_button = Button(root, text='OK',
                       command=lambda: select(action.get(), files, file_name.get(), devices, device_name.get(),
                                              data_label))
    ok_button.grid(row=2, column=3, sticky=W)

    """ Fourth row """

    # Display label
    data_label = Label(root, text='')
    data_label.grid(row=3, column=0, columnspan=3, sticky=W)

    # Redraw
    root.mainloop()


def select(action, files, file_name, devices, device_name, data_label):
    if action == 'r':
        usb.read(devices, device_name, data_label)

    elif action == 't':
        usb.test(devices, device_name, data_label)

    elif action == 'w':
        usb.write(files, file_name, devices, device_name)


def show_about(x=0, y=0):
    # Display form
    top_level = Toplevel()
    top_level.grab_set()
    top_level.resizable(0, 0)  # Prevent resizability and disable maximize button
    top_level.wm_title(f'About {constant.__project__}')
    top_level.geometry(f'+{x}+{y}')

    # Display label
    about_label = Label(top_level, text=f'{constant.__project__}\n'
                                        f'Version {constant.__version__}\n'
                                        f'{constant.__copyright__}\n'
                                        f'\n'
                                        f'The {constant.__project__} and its software are the propriety of '
                                        f'{constant.__author__}.\n'
                                        f'The hardware is sold without any warranty. The software is open-source and '
                                        f'provided free of charge.\n'
                                        f'Both are to be used with specific devices with DB9 connectors.\n'
                                        f'\n'
                                        f'This product is license under the {constant.__license__} License Terms.')
    about_label.grid()

    # Display button
    ok_button = Button(top_level, text='OK', command=top_level.destroy)
    ok_button.grid(row=1, column=0)
