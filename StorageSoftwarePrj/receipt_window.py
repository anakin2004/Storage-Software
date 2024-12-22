import tkinter as tk
from sqltable import read_data_from_server_by_id


# rcp_window declaration
def rcpt_window(_waiting_items, buy_window_frame):
    rcp_window = tk.Toplevel(buy_window_frame)
    rcp_window.title("Receipt")
    rcp_window.geometry("550x350+320+100")
    rcp_window.maxsize(550, 350)
    rcp_window.minsize(550, 350)
    rcp_window.config(bg="lightblue")
    bill_icon_photo = tk.PhotoImage(file='bill_icon.png', master=rcp_window)
    rcp_window.iconphoto(False, bill_icon_photo)

    # lock buy_window_frame while rcp_window is open
    rcp_window.grab_set()

    # grid configuration
    for j in range(13):
        rcp_window.rowconfigure(j, weight=1)

    rcp_window.columnconfigure(0, weight=3)
    rcp_window.columnconfigure(1, weight=2)

    # populate the window with content
    populate_with_content(_waiting_items, rcp_window)

    rcp_window.mainloop()


def populate_with_content(_waiting_items, rcp_window):
    # heading text label
    heading_text_label = tk.Label(rcp_window, text="В момента извършвате поръчка за:", bg='black', fg='white')
    heading_text_label.grid(row=0, column=0, sticky='new', columnspan=2)
    data_from_db_by_serial_number = read_data_from_server_by_id(_waiting_items.keys())
    print(data_from_db_by_serial_number)

    # create a list of labels, representing the bought products, based on the amount of items + wholesale
    row_position = 1
    for item in _waiting_items:
        lst = data_from_db_by_serial_number[item]
        product_name = lst[0] + ' (' + lst[1] + ')'
        product_amount = lst[2]
        product_price = lst[3]
        product_minbre = lst[4]
        product_wholesale = lst[5]

        purchased_amount = _waiting_items[item]
        item_price = '{:.2f}'.format(purchased_amount * product_price)
        print(item_price)

        label_name = tk.Label(rcp_window, text=("- " + product_name), bg='lightblue', font=("Arial", 12))
        label_name.grid(row=row_position, column=0, sticky="w")

        lable_price = tk.Label(rcp_window, text=(str(item_price) + " лв."), bg='lightblue',
                               font=("Arial", 12))
        lable_price.grid(row=row_position, column=0, sticky='e')

        if purchased_amount >= product_minbre:
            item_wholesale_prize = '{:.2f}'.format(purchased_amount*product_wholesale)
            row_position += 1

            label_sale_txt = tk.Label(rcp_window, text=("- отстъпка: " + str(item_wholesale_prize) + " лв."),
                                      bg='lightblue', font=("Arial", 10))
            label_sale_txt.grid(row=row_position, column=0, sticky="n")

        row_position += 1


    # confirm_sell button
    confirm_sell_button = tk.Button(rcp_window, text="Sell", bg="#d62d20", command=sell_items)
    confirm_sell_button.grid(row=1, column=1, rowspan=3, sticky="ns")

def sell_items():
    pass