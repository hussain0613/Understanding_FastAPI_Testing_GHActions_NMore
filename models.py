from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Item(Base):
    __tablename__ = "items"
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]

