from datetime import datetime, timezone

from sqlalchemy import insert, select

from db import engine, invoice_table


class InvoiceRepository:
    def __init__(self, engine):
        self.engine = engine

    def create(self, user_id, product_id, quantity, unit_price, total):
        stmt = (
            insert(invoice_table)
            .values(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price,
                total=total,
                created_at=datetime.now(timezone.utc),
            )
            .returning(invoice_table)
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            row = result.first()
            conn.commit()
            return row

    def get_by_user_id(self, user_id):
        stmt = select(invoice_table).where(invoice_table.c.user_id == user_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()


invoice_repository = InvoiceRepository(engine)
