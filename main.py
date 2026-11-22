import psycopg2
import tkinter as tk
from tkinter import ttk as Ttk
import tkinter.font as tkFont
from order_states import allowed, can_move
from tkinter import messagebox
import config

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
            """SELECT orders.*, totals.total
            FROM orders
            JOIN (
                SELECT order_items.order_id, SUM(menu_items.price * order_items.quantity) AS total
                FROM order_items
                JOIN menu_items ON order_items.item_id = menu_items.item_id
                GROUP BY order_items.order_id
            ) AS totals ON orders.order_id = totals.order_id
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
                    JOIN (
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
        label = tk.Label(menu_scrollable_frame, text=f"{row[1]} | £{row[2]} | {row[3]}", bg=BG_COLOUR)
        label.pack(anchor="w")



def show_customers():

    for widget in customers_scrollable_frame.winfo_children():
        widget.destroy()

    results = get_customers()

    for row in results:
        label = tk.Label(customers_scrollable_frame, text=f"{row[1]} | {row[2]} | {row[3]}", bg=BG_COLOUR)
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


def set_row_colour(frame, label, colour):
    frame.config(bg=colour)
    label.config(bg=colour)


def toggle_details(frame, details):

    if details.winfo_ismapped() == True:
        shrink_details(details, 60)
    
    else:
        details.pack(fill="x", padx=10, after=frame)
        details.config(height=1)
        grow_details(details, 1)

def grow_details(details, height):
    details.config(height=height)
    if height < 60:
        details.after(10, lambda: grow_details(details, height + 6))

def shrink_details(details, height):
    details.config(height=height)
    if height > 1:
        details.after(10, lambda: shrink_details(details, height - 6))
    else:
        details.pack_forget()

def show_orders():

    for widget in orders_scrollable_frame.winfo_children():
        widget.destroy()

    results = get_active_orders()

    for row in results:
        frame = tk.Frame(orders_scrollable_frame, bg=ROW_COLOUR, cursor="hand2")
        frame.pack(fill="x", padx=10, pady=4)
        order_options = tk.Frame(orders_scrollable_frame, bg=HOVER_COLOUR, height=60)
        order_options.pack_propagate(False)
        options_label = tk.Label(order_options, text=f"{'Delivery' if row[3] else 'Pickup'} | {row[4]} | Total: £{row[5]}", bg=HOVER_COLOUR)
        options_label.pack()

        order_text = f"Order #{row[0]:04d} | Customer {row[1]} | {row[2]} | {'Delivery' if row[3] else 'Pickup'} | {row[4]}"

        label = tk.Label(frame, 
                              text = order_text, 
                              bg=ROW_COLOUR, 
                              padx=10, 
                              pady=8, 
                              fg="white", 
                              cursor="hand2")
    

        label.pack(anchor="w", fill="x")
        label.bind("<Button-1>", lambda event, f=frame, d=order_options: toggle_details(f, d))
        for widget in (frame, label):
            widget.bind("<Enter>", lambda event, f=frame, l=label: set_row_colour(f, l, HOVER_COLOUR))
            widget.bind("<Leave>", lambda event, f=frame, l=label: set_row_colour(f, l, ROW_COLOUR))
      


        button = tk.Button(order_options, 
                           text=">> Progress order status >>", 
                           command=lambda order_id = row[0], order_status = row[4], is_delivery = row[3]: 
                           advance_order(order_id, order_status, is_delivery),
                           )
        
        button.pack(anchor="center")


def show_completed():

    for widget in completed_scrollable_frame.winfo_children():
        widget.destroy()

    results = get_completed_orders()

    

    for row in results:
            label = tk.Label(completed_scrollable_frame, text=f"Order #{row[0]:04d} | Customer {row[1]} | {row[2]} | {'Delivery' if row[3] else 'Pickup'} | {row[4]} | Total: £{row[5]}", bg=BG_COLOUR)
            label.pack(anchor="w")

####################################################################
window = tk.Tk()
window.title("Restaurant Manager Alpha")
window.geometry("1920x1080")
window.minsize(1920, 1080)
window.maxsize(1920, 1080)
window.state("zoomed")
####################################################################

BG_COLOUR = "#346f77"
ROW_COLOUR = "#1C4F79"
HOVER_COLOUR = "#7CA0BD"
custom_font = tkFont.Font(family="Lexend", weight="normal", size="50")

style = Ttk.Style()
style.theme_use("default") #REQUIRED FOR COLOUR CUSTOMISATION
style.configure("TNotebook.Tab",
                background="#FFFFFF",
                foreground="#000000",
                padding=[10, 5]
)
style.map("TNotebook.Tab",
          background=[("selected", "#555555")])

####################################################################

title = tk.Label(text="Restaurant Manager ALPHA", font=custom_font)
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