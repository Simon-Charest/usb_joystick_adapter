from usb_joystick_adapter.common.constant import constant
from usb_joystick_adapter.common.io_ import io
from usb_joystick_adapter.common.usb import usb
from tkinter import *

# Constants
LABEL_COLUMN = 0
CONTROL_COLUMN = 1
BUTTON_COLUMN = 2
OPTION_MENU_WIDTH = 35


def execute():
    # Display application
    root = Tk()
    root.geometry('400x300')
    root.resizable(0, 0)  # Prevent resizing and disable maximize button
    root.title(constant.__project__)
    root.tk.call('wm', 'iconphoto', root.w, PhotoImage(file=constant.ICON))

    """ First row """

    # Display label
    devices_label = Label(root, text='Configuration:')
    devices_label.grid(row=0, column=LABEL_COLUMN, sticky=NW)

    # Manage option menu
    files = io.get_files(constant.FIRMWARE)
    file_names = io.get_file_names(files)

    # Display option menu
    file_name = StringVar(root)

    if file_names:
        file_option_menu = OptionMenu(root, file_name, *file_names)

    else:
        file_option_menu = OptionMenu(root, file_name, file_names)

    file_option_menu.config(width=OPTION_MENU_WIDTH)
    file_option_menu.grid(row=0, column=CONTROL_COLUMN, sticky=NW)

    # Display button
    about_button = Button(root, text='About', command=lambda: show_about(root.winfo_rootx(), root.winfo_rooty()))
    about_button.grid(row=0, column=BUTTON_COLUMN, sticky=NW)

    """ Second row """

    # Display label
    devices_label = Label(root, text='Device:')
    devices_label.grid(row=1, column=LABEL_COLUMN, sticky=NW)

    # Manage option menu
    modes = constant.ADAPTER.keys()
    vendor_ids = list()
    product_ids = list()

    for mode in modes:
        vendor_ids.append(constant.ADAPTER[mode]['vendor_id'])
        product_ids.append(constant.ADAPTER[mode]['product_id'])

    devices = usb.get_devices(vendor_ids, product_ids)
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

    device_option_menu.config(width=OPTION_MENU_WIDTH)
    device_option_menu.grid(row=1, column=CONTROL_COLUMN, sticky=NW)

    """ Third row """

    # Display label
    status_label = Label(root, text='Action:')
    status_label.grid(row=2, column=LABEL_COLUMN, sticky=NW)

    # Create frame to pack radio buttons inside a single grid cell
    action_frame = Frame(root)
    action_frame.grid(row=2, column=CONTROL_COLUMN, sticky=NW)

    # Display radio button
    action = StringVar()
    action.set('l')
    load_hid_boot_radiobutton = Radiobutton(action_frame, text='Load HID Boot', variable=action, value='l')
    load_hid_boot_radiobutton.pack(side=LEFT)

    # TODO: Fix these options
    # read_radiobutton = Radiobutton(action_frame, text='Read', variable=action, value='r')
    # read_radiobutton.pack(side=LEFT)
    # test_radiobutton = Radiobutton(action_frame, text='Test', variable=action, value='t')
    # test_radiobutton.pack(side=LEFT)
    # write_radiobutton = Radiobutton(action_frame, text='Write', variable=action, value='w')
    # write_radiobutton.pack(side=LEFT)

    # Display button
    ok_button = Button(root, text='OK',
                       command=lambda: select(action.get(), files, file_name.get(), devices, device_name.get(),
                                              data_label))
    ok_button.grid(row=2, column=BUTTON_COLUMN, sticky=NW)

    """ Fourth row """

    # Display label
    status_label = Label(root, text='Status:')
    status_label.grid(row=3, column=LABEL_COLUMN, sticky=NW)

    # Display label
    data_label = Label(root, text='', borderwidth='1', relief='ridge')
    data_label.grid(row=3, column=CONTROL_COLUMN, columnspan=3, sticky=NSEW)

    # Redraw
    root.mainloop()


def select(action, files, file_name, devices, device_name, data_label):
    if action == 'l':
        usb.load_hid_boot(files, file_name, data_label)

    elif action == 'r':
        usb.read(devices, device_name, data_label)

    elif action == 't':
        usb.test(devices, device_name, data_label)

    elif action == 'w':
        usb.write(files, file_name, devices, device_name, data_label)


def show_about(x=0, y=0):
    # Display form
    top_level = Toplevel()
    top_level.grab_set()
    top_level.resizable(0, 0)  # Prevent resizability and disable maximize button
    top_level.wm_title(f'About {constant.__project__}')
    top_level.geometry(f'+{x}+{y}')

    # Display label
    about_label = Label(top_level, text=constant.ABOUT)
    about_label.grid()

    # Display button
    ok_button = Button(top_level, text='OK', command=top_level.destroy)
    ok_button.grid(row=1, column=LABEL_COLUMN)
