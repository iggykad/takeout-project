import psycopg2
import tkinter as tk
from tkinter import ttk as Ttk
import tkinter.font as tkFont
from order_states import allowed, can_move
from tkinter import messagebox
import config

ANIMATION_STEP = 30

def get_menu_items():
    try:
        connection = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM menu_items")
        results = cursor.fetchall()
        print("Database dialogue successful")

        return(results)

    except Exception as e:
        print(f"ERROR: {e}")


def get_customers():
    try:
        connection = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers")
        results = cursor.fetchall()
        print("Database dialogue successful")

        return(results)

    except Exception as e:
        print(f"ERROR: {e}")


def get_orders():
    try:
        connection = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY order_id")
        results = cursor.fetchall()
        print("Database dialogue successful")

        return(results)

    except Exception as e:
        print(f"ERROR: {e}")

def get_active_orders():
    try:
        connection = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT)

        cursor = connection.cursor()
        cursor.execute(
            """SELECT orders.*, totals.total, customers.customer_name
            FROM orders
            LEFT JOIN (
                SELECT order_items.order_id, SUM(menu_items.price * order_items.quantity) AS total
                FROM order_items
                JOIN menu_items ON order_items.item_id = menu_items.item_id
                GROUP BY order_items.order_id
            ) AS totals ON orders.order_id = totals.order_id
            JOIN customers ON orders.customer_id = customers.customer_id
            WHERE orders.status NOT IN ('delivered', 'picked_up')
            ORDER BY orders.order_id
            """)
        results = cursor.fetchall()
        print("Database dialogue successful")

        return(results)

    except Exception as e:
        print(f"ERROR: {e}")

def get_completed_orders():
    try:
        connection = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT)

        cursor = connection.cursor()
        cursor.execute(
                    """SELECT orders.*, totals.total
                    FROM orders
                    LEFT JOIN (
                        SELECT order_items.order_id, SUM(menu_items.price * order_items.quantity) AS total
                        FROM order_items
                        JOIN menu_items ON order_items.item_id = menu_items.item_id
                        GROUP BY order_items.order_id
                    ) AS totals ON orders.order_id = totals.order_id
                    WHERE orders.status IN ('delivered', 'picked_up')
                    ORDER BY orders.order_id
                    """)
        results = cursor.fetchall()
        print("Database dialogue successful")

        return(results)

    except Exception as e:
        print(f"ERROR: {e}")

def insert_order(customer_id, is_delivery):
    try:
        connection = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT)

        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO orders (order_id, customer_id, order_date, is_delivery)
            VALUES ((SELECT MAX(order_id) + 1 FROM orders), %s, CURRENT_DATE, %s) RETURNING order_id""",
            (customer_id, is_delivery))
        new_id = cursor.fetchone()[0]
        connection.commit()
        return new_id

    except Exception as e:
        print(f"ERROR: {e}")

def item_save(order_id, item_id, quantity):
    try:
        connection = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT)

        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)""",
            (order_id, item_id, quantity))

        connection.commit()

    except Exception as e:
        print(f"ERROR: {e}")




def update_order_status(order_id, new_status):
    try:
        connection = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT)
        
        cursor = connection.cursor()
        cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
        connection.commit()

    except Exception as e:
        print(f"ERROR: {e}")



####################################################################

def show_menu():

    for widget in menu_scrollable_frame.winfo_children():
            widget.destroy()

    results = get_menu_items()

    

    for row in results:
        label = tk.Label(menu_scrollable_frame, text=f"{row[1]} | £{row[2]} | {row[3]}", bg=BG_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY,)
        label.pack(anchor="w")



def show_customers():

    for widget in customers_scrollable_frame.winfo_children():
        widget.destroy()

    results = get_customers()

    for row in results:
        label = tk.Label(customers_scrollable_frame, text=f"{row[1]} | {row[2]} | {row[3]}", bg=BG_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY)
        label.pack(anchor="w")


def advance_order(order_id, order_status, is_delivery):

    if not allowed[order_status]:
        print("finished order")
        return
    
    new_status = allowed[order_status][0]

    if order_status == 'ready' and not is_delivery:
        new_status = 'picked_up'

    update_order_status(order_id, new_status)

    show_orders()
    window.update()
    if new_status in ('picked_up', 'delivered'):
        messagebox.showinfo("Order update", f"Order #{order_id:04d} complete")


def set_row_colour(frame, colour):
    frame.config(bg=colour)
    for child in frame.winfo_children():
        child.config(bg=colour)


def toggle_details(frame, details):

    if details.winfo_ismapped() == True:
        shrink_details(details, 90)
    
    else:
        details.pack(fill="x", padx=10, after=frame)
        details.config(height=1)
        grow_details(details, 1)

def grow_details(details, height):
    details.config(height=height)
    if height < 90:
        details.after(10, lambda: grow_details(details, height + ANIMATION_STEP))

def shrink_details(details, height):
    details.config(height=height)
    if height > 1:
        details.after(10, lambda: shrink_details(details, height - ANIMATION_STEP))
    else:
        details.pack_forget()

def add_button_hover(button):
    button.bind("<Enter>", lambda event: button.config(bg=ACCENT_COLOUR))
    button.bind("<Leave>", lambda event: button.config(bg=HOVER_COLOUR))

def open_new_order_form():
    form = tk.Toplevel(window)
    form.title("New order")
    form.config(bg=BG_COLOUR)
    form.geometry("400x400")
    tk.Label(form, text="NEW ORDER", bg=BG_COLOUR, fg=TEXT_COLOUR, font=FONT_HEADING).pack(pady=(15, 5))

    customers = get_customers()
    names = [row[1] for row in customers]
    picker = Ttk.Combobox(form, values=names, state="readonly")
    tk.Label(form, text="CUSTOMER", bg=BG_COLOUR, fg=ACCENT_COLOUR, font=FONT_BODY).pack(pady=(10, 0))
    picker.pack(pady=10)

    delivery_choice = tk.BooleanVar(value=True)
    tk.Label(form, text="TYPE", bg=BG_COLOUR, fg=ACCENT_COLOUR, font=FONT_BODY).pack(pady=(10, 0))
    tk.Radiobutton(form, text="Delivery", variable=delivery_choice, value=True, bg=BG_COLOUR, fg=TEXT_COLOUR, selectcolor=ROW_COLOUR, font=FONT_BODY).pack()
    tk.Radiobutton(form, text="Pickup", variable=delivery_choice, value=False, bg=BG_COLOUR, fg=TEXT_COLOUR, selectcolor=ROW_COLOUR, font=FONT_BODY).pack()

    menu = get_menu_items()
    dish_names = [row[1] for row in menu]
    tk.Label(form, text="DISH", bg=BG_COLOUR, fg=ACCENT_COLOUR, font=FONT_BODY).pack(pady=(10, 0))
    dish_picker = Ttk.Combobox(form, values=dish_names, state="readonly")
    dish_picker.pack(pady=5)

    tk.Label(form, text="QUANTITY", bg=BG_COLOUR, fg=ACCENT_COLOUR, font=FONT_BODY).pack(pady=(10, 0))
    quantity_box = tk.Spinbox(form, from_=1, to=10, width=5)
    quantity_box.pack(pady=5)

    create_button = tk.Button(form, text="Create order",
          command=lambda: create_order(picker, customers, delivery_choice, form, dish_picker, quantity_box, menu),
          bg=HOVER_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY, relief="flat",
          cursor="hand2", activebackground=HOVER_COLOUR)
    create_button.pack(pady=10)
    add_button_hover(create_button)

def create_order(picker, customers, delivery_choice, form, dish_picker, quantity_box, menu):

    position = picker.current()

    if position == -1:
        return
    
    customer_id = customers[position][0]
    new_id = insert_order(customer_id, delivery_choice.get())

    dish_position = dish_picker.current()
    quantity = int(quantity_box.get())

    if dish_position != -1:
        dish_id = menu[dish_position][0]
        item_save(new_id, dish_id, quantity)

    show_orders()
    form.destroy()

    messagebox.showinfo("Order created", f"Order #{new_id:04d} created")




def show_orders():

    for widget in orders_scrollable_frame.winfo_children():
        widget.destroy()

    results = get_active_orders()

    for row in results:
        frame = tk.Frame(orders_scrollable_frame, bg=ROW_COLOUR, cursor="hand2")
        frame.pack(fill="x", padx=10, pady=4)
        order_options = tk.Frame(orders_scrollable_frame, bg=HOVER_COLOUR, height=90)
        order_options.pack_propagate(False)
        total = row[5] or 0
        options_label = tk.Label(order_options, text=f"{'Delivery' if row[3] else 'Pickup'} | {row[4]} | Total: £{total}", bg=HOVER_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY)
        options_label.pack()

        values = [
            f"#{row[0]:04d}",
            row[6],
            row[2],
            'Delivery' if row[3] else 'Pickup',
            row[4],
            f"£{total}",
        ]

        cells = []
        for column, value in enumerate(values):
            cell = tk.Label(frame, text=value, bg=ROW_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY, anchor="w", padx=10, pady=8, cursor="hand2", width=COLUMN_WIDTHS[column])
            cell.grid(row=0, column=column, sticky="w")
            cells.append(cell)
    
        for widget in [frame] + cells:
            widget.bind("<Button-1>", lambda event, f=frame, d=order_options: toggle_details(f, d))
            widget.bind("<Enter>", lambda event, f=frame: set_row_colour(f, HOVER_COLOUR))
            widget.bind("<Leave>", lambda event, f=frame: set_row_colour(f, ROW_COLOUR))
      


        button = tk.Button(order_options, 
                           text=">> Progress order status >>", 
                           command=lambda order_id = row[0], order_status = row[4], is_delivery = row[3]: 
                           advance_order(order_id, order_status, is_delivery), bg=HOVER_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY, relief="flat", cursor="hand2", activebackground=HOVER_COLOUR
                           )
        
        button.pack(anchor="center")
        add_button_hover(button)


def show_completed():

    for widget in completed_scrollable_frame.winfo_children():
        widget.destroy()

    results = get_completed_orders()

    

    for row in results:
            label = tk.Label(completed_scrollable_frame, text=f"Order #{row[0]:04d} | {row[2]} | {'Delivery' if row[3] else 'Pickup'} | Total: £{row[5]}", bg=BG_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY)
            label.pack(anchor="w")

####################################################################
window = tk.Tk()
window.title("Restaurant Manager Alpha")
window.geometry("1920x1080")
window.minsize(1920, 1080)
window.maxsize(1920, 1080)
window.state("zoomed")
####################################################################

BG_COLOUR = "#1E1E1E"
ROW_COLOUR = "#2D2D2D"
HOVER_COLOUR = "#3A3A3A"
FONT_BODY = ("Roboto", 12)
FONT_HEADING = ("Consolas", 20, "bold")
TEXT_COLOUR = "#D8D8C0"
ACCENT_COLOUR = "#C8A24A"
COLUMN_WIDTHS = [8, 22, 14, 12, 18, 10]

style = Ttk.Style()
style.theme_use("default") #REQUIRED FOR COLOUR CUSTOMISATION
style.configure("TNotebook.Tab",
                background= ROW_COLOUR,
                foreground=TEXT_COLOUR,
                padding=[10, 5]
)
style.map("TNotebook.Tab",
          background=[("selected", HOVER_COLOUR)])

####################################################################

title = tk.Label(text="Restaurant Manager ALPHA", font=FONT_HEADING, bg=BG_COLOUR, fg=TEXT_COLOUR)
title.pack()

tabs = Ttk.Notebook(window)
tabs.pack(fill="both", expand="True")

####################################################################

menu_tab = tk.Frame(tabs)

customers_tab = tk.Frame(tabs)

orders_tab = tk.Frame(tabs)

completed_tab = tk.Frame(tabs)

tabs.add(menu_tab, text="MENU")
tabs.add(customers_tab, text="CUSTOMERS")
tabs.add(orders_tab, text="ORDERS")
tabs.add(completed_tab, text="COMPLETED ORDERS")

####################################################################

menu_canvas = tk.Canvas(menu_tab)
menu_scrollbar = tk.Scrollbar(menu_tab, width=20, command=menu_canvas.yview)
menu_canvas.configure(yscrollcommand=menu_scrollbar.set, bg=BG_COLOUR)

menu_scrollable_frame = tk.Frame(menu_canvas, bg=BG_COLOUR)
menu_canvas.create_window((0, 0), window=menu_scrollable_frame, anchor="nw")
menu_tab.configure(bg=BG_COLOUR)

menu_scrollable_frame.bind("<Configure>", lambda e: menu_canvas.configure(
    scrollregion=menu_canvas.bbox("all")
))

menu_scrollbar.pack(side="right", fill="y")
menu_canvas.pack(side="left", fill="both", expand="True")


customers_canvas = tk.Canvas(customers_tab)
customers_scrollbar = tk.Scrollbar(customers_tab, width=20, command=customers_canvas.yview)
customers_canvas.configure(yscrollcommand=customers_scrollbar.set, bg=BG_COLOUR)

customers_scrollable_frame = tk.Frame(customers_canvas, bg=BG_COLOUR)
customers_canvas.create_window((0, 0), window=customers_scrollable_frame, anchor="nw")
customers_tab.configure(bg=BG_COLOUR)

customers_scrollable_frame.bind("<Configure>", lambda e: customers_canvas.configure(
    scrollregion=customers_canvas.bbox("all")
))

customers_scrollbar.pack(side="right", fill="y")
customers_canvas.pack(side="left", fill="both", expand="True")


orders_canvas = tk.Canvas(orders_tab)
orders_scrollbar = tk.Scrollbar(orders_tab, width=20, command=orders_canvas.yview)
orders_canvas.configure(yscrollcommand=orders_scrollbar.set, bg=BG_COLOUR)

orders_scrollable_frame = tk.Frame(orders_canvas, bg=BG_COLOUR)
orders_canvas.create_window((0, 0), window=orders_scrollable_frame, anchor="nw")
orders_tab.configure(bg=BG_COLOUR)

new_order_button = tk.Button(orders_tab, text="+ New order", command=open_new_order_form, bg=HOVER_COLOUR, fg=TEXT_COLOUR, font=FONT_BODY, relief="flat", cursor="hand2",)
new_order_button.pack(side="top", anchor="w", padx=10, pady=10)
add_button_hover(new_order_button)

HEADERS = ["ORDER", "CUSTOMER", "DATE", "TYPE", "STATUS", "TOTAL"]

header_frame = tk.Frame(orders_tab, bg=BG_COLOUR)
header_frame.pack(side="top", fill="x", padx=10)

for column, name in enumerate(HEADERS):
    header_cell = tk.Label(header_frame, text=name, bg=BG_COLOUR, fg=ACCENT_COLOUR, font=FONT_BODY, anchor="w", padx=10, width=COLUMN_WIDTHS[column])
    header_cell.grid(row=0, column=column, sticky="w")

orders_scrollable_frame.bind("<Configure>", lambda e: orders_canvas.configure(
    scrollregion=orders_canvas.bbox("all")
))


orders_scrollbar.pack(side="right", fill="y")
orders_canvas.pack(side="left", fill="both", expand="True")

##########################################################################################

completed_canvas = tk.Canvas(completed_tab)
completed_scrollbar = tk.Scrollbar(completed_tab, width=20, command=completed_canvas.yview)
completed_canvas.configure(yscrollcommand=completed_scrollbar.set, bg=BG_COLOUR)

completed_scrollable_frame = tk.Frame(completed_canvas, bg=BG_COLOUR)
completed_canvas.create_window((0, 0), window=completed_scrollable_frame, anchor="nw")
completed_tab.configure(bg=BG_COLOUR)

completed_scrollable_frame.bind("<Configure>", lambda e: completed_canvas.configure(
    scrollregion=completed_canvas.bbox("all")
))

completed_scrollbar.pack(side="right", fill="y")
completed_canvas.pack(side="left", fill="both", expand="True")

####################################################################

tab_actions = {
    0: show_menu,
    1: show_customers,
    2: show_orders,
    3: show_completed
}

def on_tab_change(event):
    selected = tabs.index(tabs.select())
    tab_actions[selected]()

tabs.bind("<<NotebookTabChanged>>", on_tab_change)

window.mainloop()