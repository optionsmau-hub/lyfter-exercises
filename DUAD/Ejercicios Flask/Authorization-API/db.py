from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Float, Date, DateTime, ForeignKey

DB_URI = "sqlite:///app.db"
engine = create_engine(DB_URI)

metadata_obj = MetaData()

user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("role", String(10), nullable=False, default="user"),
)

product_table = Table(
    "products",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("price", Float, nullable=False),
    Column("entry_date", Date, nullable=False),
    Column("quantity", Integer, nullable=False),
)

invoice_table = Table(
    "invoices",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Float, nullable=False),
    Column("total", Float, nullable=False),
    Column("created_at", DateTime, nullable=False),
)

metadata_obj.create_all(engine)
