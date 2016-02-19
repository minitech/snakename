from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

suggestions = Table(
    "suggestions", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(80), nullable=False, unique=True),
)

votes = Table(
    "votes", metadata,
    Column("suggestion", Integer, ForeignKey("suggestions.id"), index=True),
    Column("ip", String(47), nullable=False),
)
