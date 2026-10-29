from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class FavoritableTypeEnum(str, enum.Enum):
    session = "session"
    speaker = "speaker"
    product = "product" 
    gallery_item = "gallery_item"


class NotificationTypeEnum(str, enum.Enum):
    session_reminder = "session_reminder"
    general = "general"
    system = "system"


class ConnectionStatusEnum(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"


class QuestionTypeEnum(str, enum.Enum):
    multiple_choice = "multiple_choice"
    text = "text"
    rating = "rating"
    yes_no = "yes_no"


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    favoritable_type = Column(Enum(FavoritableTypeEnum), nullable=False)
    favoritable_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite {self.user_id} - {self.favoritable_type}:{self.favoritable_id}>"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationTypeEnum), nullable=False)
    is_read = Column(Boolean, default=False)
    scheduled_for = Column(DateTime(timezone=True))
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.title}>"


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    description = Column(Text)
    image_url = Column(Text, nullable=False)
    thumbnail_url = Column(Text)
    is_featured = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    event = relationship("Event", back_populates="gallery_items")
    user = relationship("User", back_populates="gallery_items")

    def __repr__(self):
        return f"<Gallery {self.title or self.id}>"


class NeodentProduct(Base):
    __tablename__ = "neodent_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    product_code = Column(String(50))
    image_url = Column(Text)
    brochure_url = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<NeodentProduct {self.name}>"


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    icon_url = Column(Text)
    criteria = Column(JSONB)  # Conditions to earn the badge
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")

    def __repr__(self):
        return f"<Badge {self.name}>"


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")

    def __repr__(self):
        return f"<UserBadge {self.user_id} - {self.badge_id}>"


class NetworkingConnection(Base):
    __tablename__ = "networking_connections"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    requestee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ConnectionStatusEnum), default=ConnectionStatusEnum.pending)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], back_populates="sent_connections")
    requestee = relationship("User", foreign_keys=[requestee_id], back_populates="received_connections")

    def __repr__(self):
        return f"<NetworkingConnection {self.requester_id} -> {self.requestee_id}>"


class StaticPage(Base):
    __tablename__ = "static_pages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(5), default="en")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<StaticPage {self.slug}>"


class DigitalCertificate(Base):
    __tablename__ = "digital_certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    certificate_type = Column(String(100))
    certificate_url = Column(Text)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="digital_certificates")
    event = relationship("Event", back_populates="digital_certificates")

    def __repr__(self):
        return f"<DigitalCertificate {self.user_id} - {self.event_id}>" 