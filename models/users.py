from sqlalchemy.orm import mapped_column, Mapped
import uuid
from core.database import Base


class UsersModel(Base):
    """User model."""
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )    
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
