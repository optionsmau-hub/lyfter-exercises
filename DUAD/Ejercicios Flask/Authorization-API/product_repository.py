from sqlalchemy import insert, select, update, delete

from db import engine, product_table


class ProductRepository:
    def __init__(self, engine):
        self.engine = engine

    def create(self, name, price, entry_date, quantity):
        stmt = (
            insert(product_table)
            .values(name=name, price=price, entry_date=entry_date, quantity=quantity)
            .returning(product_table)
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            row = result.first()
            conn.commit()
            return row

    def get_all(self):
        stmt = select(product_table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    def get_by_id(self, product_id):
        stmt = select(product_table).where(product_table.c.id == product_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.first()

    def update(self, product_id, **fields):
        stmt = (
            update(product_table)
            .where(product_table.c.id == product_id)
            .values(**fields)
            .returning(product_table)
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            row = result.first()
            conn.commit()
            return row

    def decrease_stock(self, product_id, amount):
        # The quantity >= amount check runs inside the same atomic UPDATE,
        # so two concurrent purchases can't both pass a separate pre-check
        # and oversell the stock.
        stmt = (
            update(product_table)
            .where(product_table.c.id == product_id, product_table.c.quantity >= amount)
            .values(quantity=product_table.c.quantity - amount)
            .returning(product_table.c.id)
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            row = result.first()
            conn.commit()
            return row

    def delete(self, product_id):
        stmt = (
            delete(product_table)
            .where(product_table.c.id == product_id)
            .returning(product_table.c.id)
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            row = result.first()
            conn.commit()
            return row


product_repository = ProductRepository(engine)
