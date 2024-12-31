import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import datetime

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Management")
        self.conn = self.connect_db()
        self.create_gui()
        self.fetch_items()

    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  
                password="",  
                database="inventory_produk"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            self.root.destroy()

    def create_gui(self):
        frame_input = tk.Frame(self.root, padx=10, pady=10)
        frame_input.pack()

        tk.Label(frame_input, text="Name Product:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(frame_input, width=30, font=("Arial", 12))
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Harga Product:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.entry_harga = tk.Entry(frame_input, width=30, font=("Arial", 12))
        self.entry_harga.grid(row=1, column=1, padx=5, pady=5)

        frame_buttons = tk.Frame(self.root, padx=10, pady=10)
        frame_buttons.pack()

        btn_add_product = tk.Button(frame_buttons, text="Add Product", command=self.add_product, width=15, font=("Arial", 12))
        btn_add_product.grid(row=0, column=0, padx=5, pady=5)

        btn_update_product = tk.Button(frame_buttons, text="Update Product", command=self.update_product, width=15, font=("Arial", 12))
        btn_update_product.grid(row=0, column=1, padx=5, pady=5)

        btn_delete_product = tk.Button(frame_buttons, text="Delete Product", command=self.delete_product, width=15, font=("Arial", 12))
        btn_delete_product.grid(row=0, column=2, padx=5, pady=5)

        btn_back = tk.Button(frame_buttons, text="Menu Utama", command=self.go_back_to_main, width=15, font=("Arial", 12))
        btn_back.grid(row=1, column=1, pady=10)

        frame_table = tk.Frame(self.root, padx=10, pady=10)
        frame_table.pack()

        columns = ("ID", "Name", "Harga")
        self.table = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)
        self.table.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(frame_table, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT)

        self.footer = tk.Label(self.root, text="Total Products: 0", padx=10, pady=10)
        self.footer.pack()

    # Bind row selection event di dalam __init__ method
        self.table.bind("<ButtonRelease-1>", self.select_product)

# Fungsi untuk menampilkan produk yang dipilih ke dalam input fields
    def select_product(self, event):
        selected = self.table.focus()
        if selected:
            values = self.table.item(selected, "values")
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, values[1])  # Product name
            self.entry_harga.delete(0, tk.END)
            self.entry_harga.insert(0, values[2])  # Product price

        

    def fetch_items(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            for row in self.table.get_children():
                self.table.delete(row)
            for row in rows:
                self.table.insert("", "end", values=row)
            self.footer.config(text=f"Total Products: {len(rows)}")
        except Exception as e:
            messagebox.showerror("Product Error", f"Kesalahan pengambilan produk: {e}")

    def add_product(self):
        try:
            name = self.entry_name.get()
            harga = float(self.entry_harga.get())
        except ValueError:
            messagebox.showwarning("Product Error", "Harga harus berupa angka yang valid!")
            return

        if not name:
            messagebox.showwarning("Product Error", "Name produk tidak boleh kosong!")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO products (Name, harga) VALUES (%s, %s)", 
                           (name, harga))
            self.conn.commit()
            self.clear_inputs()
            self.fetch_items()
            messagebox.showinfo("Product Success", "Produk berhasil ditambahkan!")
        except Exception as e:
            messagebox.showerror("Product Error", f"Kesalahan menambahkan produk: {e}")

    def update_product(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Pilih produk yang akan diperbarui!")
            return
        values = self.table.item(selected, "values")
        id_ = values[0]
        try:
            name = self.entry_name.get()
            harga = float(self.entry_harga.get())
        except ValueError:
            messagebox.showwarning("Product Error", "Harga harus berupa angka yang valid!")
            return

        if not name:
            messagebox.showwarning("Product Error", "Name produk tidak boleh kosong!")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE products SET name=%s, harga=%s WHERE id=%s", 
                           (name, harga, id_))
            self.conn.commit()
            self.clear_inputs()
            self.fetch_items()
            messagebox.showinfo("Product Success", "Produk berhasil diperbarui!")
        except Exception as e:
            messagebox.showerror("Product Error", f"Kesalahan memperbarui produk: {e}")

    def delete_product(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Pilih produk yang akan dihapus!")
            return
        values = self.table.item(selected, "values")
        id_ = values[0]
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=%s", (id_,))
            self.conn.commit()
            self.fetch_items()
            messagebox.showinfo("Product Success", "Produk berhasil dihapus!")
        except Exception as e:
            messagebox.showerror("Product Error", f"Kesalahan menghapus produk: {e}")

    def clear_inputs(self):
        self.entry_name.delete(0, tk.END)
        self.entry_harga.delete(0, tk.END)

    def go_back_to_main(self):
        self.root.destroy()
        show_main_menu()


class TransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction Management")
        self.conn = self.connect_db()
        self.create_gui()
        self.fetch_items()
        self.fetch_transactions()

    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  
                password="",  
                database="inventory_produk"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            self.root.destroy()

    def create_gui(self):
        frame_transaction = tk.Frame(self.root, padx=10, pady=10)
        frame_transaction.pack()

        tk.Label(frame_transaction, text="Product:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.product_dropdown = ttk.Combobox(frame_transaction, width=30, font=("Arial", 12))
        self.product_dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_transaction, text="Jumlah:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.entry_jumlah_product = tk.Entry(frame_transaction, width=30, font=("Arial", 12))
        self.entry_jumlah_product.grid(row=1, column=1, padx=5, pady=5)

        frame_buttons_transaction = tk.Frame(self.root, padx=10, pady=10)
        frame_buttons_transaction.pack()

        btn_add_transaction = tk.Button(frame_buttons_transaction, text="Add Transaction", command=self.add_transaction, width=15, font=("Arial", 12))
        btn_add_transaction.grid(row=0, column=0, padx=5)

        btn_back = tk.Button(frame_buttons_transaction, text="Menu Utama", command=self.go_back_to_main, width=15, font=("Arial", 12))
        btn_back.grid(row=1, column=0, padx=5)

        frame_table_transaction = tk.Frame(self.root, padx=10, pady=10)
        frame_table_transaction.pack()

        columns = ("ID Transaks", "ID Produk", "Product", "Jumlah Produk", "Total Harga", "Tanggal Transaksi")
        self.table_transaction = ttk.Treeview(frame_table_transaction, columns=columns, show="headings", height=8)
        for col in columns:
            self.table_transaction.heading(col, text=col)
            self.table_transaction.column(col, width=100)
        self.table_transaction.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(frame_table_transaction, orient="vertical", command=self.table_transaction.yview)
        self.table_transaction.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT)

        self.footer = tk.Label(self.root, text="Total Transaksi: 0", padx=10, pady=10)
        self.footer.pack()

    def fetch_items(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            self.product_dropdown['values'] = [row[1] for row in rows]

        except Exception as e:
            messagebox.showerror("Transaction Error", f"Kesalahan pengambilan produk: {e}")

    def fetch_transactions(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT t.id, t.product_id, p.name, t.jumlah_product, t.total_harga, t.tanggal_transaksi "
                           "FROM transactions t "
                           "JOIN products p ON t.product_id = p.id")
            rows = cursor.fetchall()
            for row in self.table_transaction.get_children():
                self.table_transaction.delete(row)
            for row in rows:
                self.table_transaction.insert("", "end", values=row)
            self.footer.config(text=f"Total Transaksi: {len(rows)}")
        except Exception as e:
            messagebox.showerror("Transaction Error", f"Kesalahan pengambilan produk: {e}")

    def add_transaction(self):
        try:
            product_name = self.product_dropdown.get()
            jumlah_product = int(self.entry_jumlah_product.get())

            if not product_name:
                messagebox.showwarning("Transaction Error", "Silakan pilih produk!")
                return
            if jumlah_product <= 0:
                messagebox.showwarning("Transaction Error", "Jumlah harus berupa bilangan bulat positif!")
                return

            cursor = self.conn.cursor()
            cursor.execute("SELECT id, harga FROM products WHERE Name = %s", (product_name,))
            product = cursor.fetchone()
            product_id = product[0]
            harga = product[1]
            total_harga = harga * jumlah_product

            tanggal_transaksi = datetime.date.today()

            cursor.execute("INSERT INTO transactions (product_id, jumlah_product, total_harga, tanggal_transaksi) "
                           "VALUES (%s, %s, %s, %s)", 
                           (product_id, jumlah_product, total_harga, tanggal_transaksi))
            self.conn.commit()

            self.clear_inputs()
            self.fetch_transactions()
            messagebox.showinfo("Transaction Success", "Transaksi berhasil ditambahkan!")

        except Exception as e:
            messagebox.showerror("Transaction Error", f"Kesalahan penambahan transaksi: {e}")

    def clear_inputs(self):
        self.product_dropdown.set('')
        self.entry_jumlah_product.delete(0, tk.END)

    def go_back_to_main(self):
        self.root.destroy()
        show_main_menu()

def show_main_menu():
    window = tk.Tk()
    window.title("Menu Utama")
    window.geometry("400x300")

    title_label = tk.Label(window, text="Welcome to Inventory and Transaction Management", font=("Arial", 16), pady=20)
    title_label.pack()

    manage_products_button = tk.Button(window, text="Manage Products", command=lambda: open_product_window(window), font=("Arial", 12), width=20)
    manage_products_button.pack(pady=10)

    manage_transactions_button = tk.Button(window, text="Manage Transactions", command=lambda: open_transaction_window(window), font=("Arial", 12), width=20)
    manage_transactions_button.pack(pady=10)

    window.mainloop()

def open_product_window(window):
    window.destroy()
    product_window = tk.Tk()
    app = ProductApp(product_window)
    product_window.mainloop()

def open_transaction_window(window):
    window.destroy()
    transaction_window = tk.Tk()
    app = TransactionApp(transaction_window)
    transaction_window.mainloop()


if __name__ == "__main__":
    show_main_menu()
