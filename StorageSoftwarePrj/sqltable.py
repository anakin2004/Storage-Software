import sqlite3
from typing import Any


def create_database():
    available_goods_database = sqlite3.connect("storage_items.db")
    goods_cursor = available_goods_database.cursor()
    goods_cursor.execute("Create table if not exists available_goods("
                         "photo BLOB, serial_number text type unique,"
                         " name text,color text, available integer, price real, minbre integer, wholesale real)")
    available_goods_database.commit()
    available_goods_database.close()


def conv_img_to_blob(chosen_filename: str):
    with open(chosen_filename, "rb") as file:
        particular_photo = file.read()
    return particular_photo


def insert_values_into_database(serial_number: str, name: str, color: str, available: int, price: float,
                                minbre: int, wholesale: float, filename='default_image.png'):
    available_goods_database = sqlite3.connect("storage_items.db")
    goods_cursor = available_goods_database.cursor()

    image_photo = conv_img_to_blob(filename)
    try:
        goods_cursor.execute(
            "Insert into available_goods(photo,serial_number,name,color,available,price,minbre,wholesale) "
            "Values(?,?,?,?,?,?,?,?)", (image_photo, serial_number, name, color, available, price, minbre, wholesale))
    except sqlite3.IntegrityError:
        goods_cursor.execute("Update available_goods set available=("
                             "(Select available from available_goods where serial_number=?)+?)"
                             " where serial_number=?", (serial_number, available, serial_number))

    available_goods_database.commit()
    available_goods_database.close()


# read data from server
def read_data_from_server():
    available_goods_database = sqlite3.connect("storage_items.db")
    goods_cursor = available_goods_database.cursor()
    read_server_data: dict[str, list[Any]] = {}
    for photo, serial_number, name, color, available, price, minbre, wholesale in \
            goods_cursor.execute("Select * from available_goods"):
        read_server_data[serial_number] = [name, color, available, price, minbre, wholesale, photo]
        # print(serial_number, f"; {name} ({color})")
        # with open("default_image.png", "wb") as image_file:
        #     image_file.write(photo)

    available_goods_database.close()
    return read_server_data


def read_data_from_server_by_id(serial_number_list: list[str]):
    available_goods_database = sqlite3.connect("storage_items.db")
    goods_cursor = available_goods_database.cursor()

    read_server_data = {}

    for serial_number in serial_number_list:
        item = goods_cursor.execute('Select name, color, available, price,'
                                    'minbre, wholesale from available_goods where serial_number=?', (serial_number,))
        info = item.fetchone()
        read_server_data[serial_number] = info

    available_goods_database.close()
    return read_server_data


# drop certain record from table
def drop_record_from_database(serial_number: str):
    available_goods_database = sqlite3.connect("storage_items.db")
    goods_cursor = available_goods_database.cursor()

    goods_cursor.execute("Delete from available_goods where serial_number=?", (serial_number,))
    available_goods_database.commit()
    available_goods_database.close()


if __name__ == "__main__":
    # create_database()
    # insert_values_into_database("3796937754", "Стол", "черен", 10, 12.5, 4, 2.0, 'black_chair.jpg')
    # insert_values_into_database("4553330779", "Маса", "кафява", 18, 22.2, 3, 3.4, 'brown_table.jpg')
    # insert_values_into_database("0595334256", "Стол", "зелен", 30, 7.3, 4, 2.0, 'green_chair.jpg')
    # insert_values_into_database("1716168217", "Нощно шкафче", "бяло", 8, 20.4, 2, 1.75, 'white_night_stand.jpg')
    # insert_values_into_database("3668255920", "Шкаф", "бял", 5, 86, 2, 3.5, 'white_closet.png')
    # insert_values_into_database("1712517971", "Легло", "черено", 7, 53, 3, 1.78, 'black_bed_frame.jpg')
    # insert_values_into_database("4722395101", "Стъклена маса", "черна", 14, 18.4, 3, 3.6, 'black_glass_table.jpg')
    # drop_record_from_database(37969377545)

    print(read_data_from_server())
