import io
import tkinter.messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from receipt_window import rcpt_window
from sqltable import *

# main window set up
buy_window_frame = tk.Tk()
buy_window_frame.title("Storage software")
storage_icon_photo = tk.PhotoImage(file='storage_icon.png')
buy_window_frame.iconphoto(False, storage_icon_photo)

max_window_width = buy_window_frame.winfo_screenwidth()
max_window_height = buy_window_frame.winfo_screenheight()
buy_window_frame.state("zoomed")
print(max_window_width, max_window_height)  # 1280, 720 tuk

# TODO: da se napravi taka che da moje da se smalqva prozoreca do 1280x840
# buy_window_frame.geometry("%dx%d+0+0" % (max_window_width, max_window_height))
# buy_window_frame.geometry("1920x1080+0+0")
# buy_window_frame.minsize(1280, 840)

buy_window_frame.minsize(max_window_width // 6 * 5,
                         max_window_height // 3 * 2)  # da se pogledne na golemiq laptop kak izglejda
buy_window_frame.maxsize(max_window_width, max_window_height)

buy_window_frame.config(bg="lightblue")

for i in range(9):
    buy_window_frame.rowconfigure(i, weight=1)
for i in range(7):
    buy_window_frame.columnconfigure(i, weight=1)

# declaring useful variables
waiting_items_counter = 0
_waiting_items = {}

# buy/sell button set up
buy_sell_button = tk.Button(buy_window_frame, text="Sell / Buy")
buy_sell_button.grid(column=2, row=1, columnspan=2, sticky="we")

# logo set up
logo_image = tk.PhotoImage(file="logo_test_photo.png")
logo_label = tk.Label(buy_window_frame, image=logo_image)
logo_label.grid(column=8, row=1, rowspan=3, padx=100, sticky='new')

# table 'available' set up
table_available = ttk.Treeview(buy_window_frame)
table_available.grid(row=3, column=0, columnspan=7, rowspan=6, sticky='nsew', padx=50)
table_available['columns'] = ('item_serial_number', 'item_name', 'item_amount', 'item_prize',
                              'item_minbre', 'item_wholesale')
table_available.column("#0", width=90, anchor='center', stretch=False)
table_available.column("item_serial_number", anchor='center', width=90, minwidth=10)
table_available.column("item_name", anchor='center', width=100, minwidth=10)
table_available.column("item_amount", anchor='center', width=60, minwidth=10)
table_available.column("item_prize", anchor='center', width=60, minwidth=10)
table_available.column("item_minbre", anchor='center', width=60, minwidth=10)
table_available.column("item_wholesale", anchor='center', width=100, minwidth=10)

table_available.heading("#0", text="Photo", anchor='center')
table_available.heading("item_serial_number", text="Serial Number", anchor='center')
table_available.heading("item_name", text="Name", anchor='center')
table_available.heading("item_amount", text="Amount", anchor='center')
table_available.heading("item_prize", text="Prize", anchor='center')
table_available.heading("item_minbre", text="Min BRE", anchor='center')
table_available.heading("item_wholesale", text="Wholesale (%)", anchor='center')

style = ttk.Style()
style.configure("Treeview", rowheight=60)
table_available.configure(style="Treeview")

# scrollbar for table
table_scroll = ttk.Scrollbar(table_available, orient="vertical", command=table_available.yview)
table_available.configure(yscrollcommand=table_scroll.set)
table_scroll.pack(side="right", fill="y")

# input amount label
amount_label = tk.Label(buy_window_frame, text="Amount?")
amount_label.grid(row=4, column=7, sticky='new')

# input amount text field
input_amount_textfield = tk.Entry(buy_window_frame)
input_amount_textfield.grid(row=4, column=7, sticky='ew')

# table orders waiting approval
table_waiting_orders = ttk.Treeview(buy_window_frame)
table_waiting_orders.grid(row=4, column=8, columnspan=2, rowspan=5, sticky='ns')
table_waiting_orders['columns'] = ('waiting_item_name', 'waiting_item_amount')

table_waiting_orders.column("#0", width=0, anchor='center', stretch=False)
table_waiting_orders.column("waiting_item_name", anchor='center', width=120, minwidth=10)
table_waiting_orders.column("waiting_item_amount", anchor='center', width=80, minwidth=10)

# table_waiting_orders.heading("#0", text="Serial Number", anchor='center')
table_waiting_orders.heading("waiting_item_name", text="Name", anchor='center')
table_waiting_orders.heading("waiting_item_amount", text="Amount", anchor='center')


# makes wanted item with the precise amount go into table waiting approval
def mark_as_wanted():
    global waiting_items_counter
    global _waiting_items
    if table_available.focus():
        try:
            # check if the input is proper
            entered_amount = int(input_amount_textfield.get())
            if isinstance(entered_amount, int) and entered_amount > 0:
                current_selected_item = table_available.item(table_available.focus(), 'values')
                focused_amount = current_selected_item[2]

                # check if the entered amount is lower or equal to what is in storage
                if entered_amount <= int(focused_amount):
                    waiting_item_serial_number = str(current_selected_item[0])

                    # check if the item has been added before in the list
                    if waiting_item_serial_number in _waiting_items.keys():
                        expected_amount = _waiting_items[waiting_item_serial_number] + entered_amount

                        # if it has been, check if (entered value + the already existing value) <= stockpile
                        if expected_amount > int(current_selected_item[2]):
                            tk.messagebox.showinfo("Can't do the current action",
                                                   "The wanted amount exceeds what is in stockpile!")
                        else:
                            _waiting_items[waiting_item_serial_number] = expected_amount
                            table_waiting_orders.set(waiting_item_serial_number, column="waiting_item_amount",
                                                     value=expected_amount)

                    # if the item has not been added before
                    else:
                        _waiting_items[waiting_item_serial_number] = entered_amount

                        waiting_items_counter += 1

                        # check if the items count won't exceed the allowed
                        if waiting_items_counter <= 6:
                            waiting_item_name = current_selected_item[1]
                            table_waiting_orders.insert("", 'end', iid=waiting_item_serial_number, values=(
                                waiting_item_name, entered_amount))

                        else:
                            waiting_items_counter -= 1
                            tk.messagebox.showinfo(
                                "Can't do the current action",
                                "You have already selected 6 items, which is the maximum for a single transaction!")
                else:
                    tk.messagebox.showinfo("Can't do the current action", "Input is too big!")
            else:
                tk.messagebox.showinfo("Can't do the current action",
                                       "Incorrect input! It must be whole positive number!")
        except ValueError:
            tk.messagebox.showinfo("Can't do the current action", "Improper input!")


# input amount button
input_amount_button = tk.Button(buy_window_frame, text="Input", command=mark_as_wanted)
input_amount_button.grid(row=4, column=7, sticky='sew')


# retrieve item from table_waiting_orders
def retrieve_back():
    global _waiting_items
    global waiting_items_counter
    if table_waiting_orders.focus():
        selected_item_iid = table_waiting_orders.focus()
        table_waiting_orders.delete(selected_item_iid)
        waiting_items_counter -= 1
        del _waiting_items[str(selected_item_iid)]
        print(_waiting_items)
    else:
        tk.messagebox.showinfo("Can't do the current action", "First choose an item from the table on the right!")


# retrieve back button for table_waiting_orders
retrieve_back_button = tk.Button(buy_window_frame, text="Retrieve", command=retrieve_back)
retrieve_back_button.grid(row=5, column=7, sticky="ew")


def sell_waiting_items():
    rcpt_window(_waiting_items, buy_window_frame)


# sell button
sell_button = tk.Button(buy_window_frame, text="Sell", bg="#d62d20", command=sell_waiting_items)
sell_button.grid(row=6, column=7, rowspan=3, sticky="nsew")


# TODO: after everything make it directly to populate the table due to possibility of memory overflow
# populate main table with records from the database
def load_main_table():
    available_photos_list = []
    read_server_data = read_data_from_server()
    for serial_number in read_server_data.keys():
        name, color, amount, price, minbre, wholesale, photo = read_server_data[serial_number]
        full_item_name = f"{name} ({color})"
        item_img = Image.open(io.BytesIO(photo))
        item_img = item_img.resize((50, 50))
        item_photo_image = ImageTk.PhotoImage(item_img)
        table_available.insert(parent="", index="end", iid=serial_number,
                               values=(serial_number, full_item_name, amount, price, minbre, wholesale),
                               image=item_photo_image)
        available_photos_list.append(item_photo_image)
    return available_photos_list


prevent_photo_garbage_collector_variable = load_main_table()

buy_window_frame.mainloop()
