# utilities/DB.py
import os
import sys
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def choose_db_path():
    """
    Pilih lokasi file DB:
    1) ProjectRoot/instance/store.db (prefer)
    2) Jika gagal, fallback ke user's home directory ~/ProjectBasisData_store.db
    """
    this_file = Path(__file__).resolve()
    project_root = this_file.parent.parent  # dua level: utilities/ -> ProjectBasisData/
    prefer_dir = project_root / "instance"
    prefer_dir_exists = False

    try:
        prefer_dir.mkdir(parents=True, exist_ok=True)
        # test write to ensure we can create file here
        test_file = prefer_dir / ".writetest"
        with open(test_file, "w") as f:
            f.write("ok")
        test_file.unlink()  # remove
        prefer_dir_exists = True
    except Exception as e:
        # tidak bisa tulis di instance/
        prefer_dir_exists = False

    if prefer_dir_exists:
        db_file = prefer_dir / "store.db"
        return db_file, project_root
    else:
        # fallback ke home dir
        home = Path.home()
        db_file = home / "ProjectBasisData_store.db"
        try:
            # test write
            with open(db_file, "a") as f:
                pass
            return db_file, project_root
        except Exception as e:
            # kalau masih gagal, raise supaya user tahu
            raise RuntimeError(
                f"Cannot create database file in project instance ({prefer_dir}) "
                f"nor in home directory ({db_file}).\n"
                f"Error: {e}"
            )

# ===== konfigurasi Flask & SQLAlchemy =====
try:
    db_path, project_root = choose_db_path()
except Exception as e:
    print("FATAL: gagal menentukan lokasi database:", e)
    sys.exit(1)

# Pastikan folder tempat db ada
db_folder = db_path.parent
db_folder.mkdir(parents=True, exist_ok=True)

# gunakan posix path agar sqlite URI konsisten
db_uri = f"sqlite:///{db_path.as_posix()}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# debug info singkat
print("Working directory :", os.getcwd())
print("Project root      :", project_root)
print("Database file     :", db_path)
print("Database URI      :", app.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(app)

# ============ MODELS ============
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    customer = db.relationship("Customer", backref="orders")
    product = db.relationship("Product", backref="orders")

# ============ CRUD helper ============
def add_product(name, price, stock):
    p = Product(name=name, price=price, stock=stock)
    db.session.add(p)
    db.session.commit()
    return p

def get_all_products():
    return Product.query.all()

def add_customer(name, email):
    c = Customer(name=name, email=email)
    db.session.add(c)
    db.session.commit()
    return c

def add_order(customer_id, product_id, quantity):
    product = Product.query.get(product_id)
    if not product:
        return None, "Product not found"
    if product.stock < quantity:
        return None, "Not enough stock"
    order = Order(customer_id=customer_id, product_id=product_id, quantity=quantity)
    db.session.add(order)
    product.stock -= quantity
    db.session.commit()
    return order, None

def get_all_orders():
    return Order.query.all()

# ============ MAIN (run & test) ============
if __name__ == "__main__":
    try:
        with app.app_context():
            print("\nMencoba membuat tabel di database...")
            db.create_all()
            print("Tabel berhasil dibuat / sudah ada.")
            # contoh insert minimal bila kosong
            if not Product.query.first():
                add_product("Laptop", 7500000, 10)
                add_product("Mouse", 150000, 50)
                print("Menambahkan contoh produk.")
            if not Customer.query.first():
                add_customer("Budi", "budi@example.com")
                print("Menambahkan contoh customer.")
            print("\n== Daftar Produk ==")
            for p in get_all_products():
                print(f"{p.id}. {p.name} - Rp{p.price} (stok: {p.stock})")
            print("\n== Selesai ==")
    except Exception as exc:
        print("ERROR saat membuat/akses database:")
        print(str(exc))
        # tambahan: jika ini sqlite OperationalError, beri tips
        if "unable to open database file" in str(exc).lower():
            print("\nTIPS:")
            print("- Pastikan tidak ada file DB yang sedang terkunci (misal dibuka oleh aplikasi lain).")
            print("- Cek permission folder (read/write).")
            print("- Jika path mengandung karakter spesial atau spasi, coba pindahkan project ke folder sederhana, misal C:/ProjectBasisData/")
            print("- Coba jalankan terminal sebagai Administrator untuk test.")
        sys.exit(1)
