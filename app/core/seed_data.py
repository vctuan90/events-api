#!/usr/bin/env python3
"""
Seed data script for STRAUMANN Event API
Creates sample data for development and testing
"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.event import Event
from app.models.speaker import Speaker, SessionSpeaker
from app.models.session import Session, SessionTypeEnum, UserSession
from app.models.common import (
    Favorite, FavoritableTypeEnum,
    Notification, NotificationTypeEnum,
    Gallery, NeodentProduct, Badge, UserBadge,
    NetworkingConnection, ConnectionStatusEnum,
    StaticPage, DigitalCertificate
)
from app.models.survey import Survey, SurveyQuestion, SurveyResponse
from app.models.session import SessionQuestion, SessionFeedback


async def create_users(db: AsyncSession):
    """Create admin and regular users"""
    print("Creating users...")
    
    # Admin user
    admin_user = User(
        email="admin@straumann.com",
        password_hash=get_password_hash("admin123"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
        company="Straumann",
        position="System Administrator"
    )
    db.add(admin_user)
    
    # Regular users
    users_data = [
        {
            "email": "john.doe@example.com",
            "password": "user123",
            "full_name": "John Doe",
            "role": UserRole.ATTENDEE,
            "company": "Dental Clinic ABC",
            "position": "Dentist"
        },
        {
            "email": "jane.smith@example.com", 
            "password": "user123",
            "full_name": "Jane Smith",
            "role": UserRole.ATTENDEE,
            "company": "Smile Center",
            "position": "Oral Surgeon"
        },
        {
            "email": "mike.wilson@example.com",
            "password": "user123", 
            "full_name": "Mike Wilson",
            "role": UserRole.SPEAKER,
            "company": "Dental University",
            "position": "Professor"
        },
        {
            "email": "sarah.johnson@example.com",
            "password": "user123",
            "full_name": "Sarah Johnson", 
            "role": UserRole.ORGANIZER,
            "company": "Event Management Co",
            "position": "Event Coordinator"
        },
        {
            "email": "david.brown@example.com",
            "password": "user123",
            "full_name": "David Brown",
            "role": UserRole.ATTENDEE,
            "company": "Modern Dentistry",
            "position": "Dental Technician"
        }
    ]
    
    for user_data in users_data:
        user = User(
            email=user_data["email"],
            password_hash=get_password_hash(user_data["password"]),
            full_name=user_data["full_name"],
            role=user_data["role"],
            is_active=True,
            company=user_data["company"],
            position=user_data["position"]
        )
        db.add(user)
    
    await db.commit()
    print("✅ Users created")


async def create_events(db: AsyncSession):
    """Create sample events"""
    print("Creating events...")
    
    events_data = [
        {
            "title": "STRAUMANN Digital Dentistry Summit 2024",
            "description": "Join us for the premier digital dentistry event featuring the latest innovations in implant technology, digital workflows, and patient care solutions.",
            "start_date": datetime.now() + timedelta(days=30),
            "end_date": datetime.now() + timedelta(days=32),
            "location": "Basel, Switzerland",
            "banner_image": "https://example.com/banner1.jpg",
            "is_active": True
        },
        {
            "title": "Neodent Innovation Workshop",
            "description": "Hands-on workshop exploring the latest Neodent implant systems and digital solutions for modern dental practices.",
            "start_date": datetime.now() + timedelta(days=60),
            "end_date": datetime.now() + timedelta(days=61),
            "location": "São Paulo, Brazil",
            "banner_image": "https://example.com/banner2.jpg",
            "is_active": True
        },
        {
            "title": "Digital Workflow Masterclass",
            "description": "Master the complete digital workflow from scanning to final restoration with expert guidance and hands-on practice.",
            "start_date": datetime.now() + timedelta(days=90),
            "end_date": datetime.now() + timedelta(days=90),
            "location": "Virtual Event",
            "banner_image": "https://example.com/banner3.jpg",
            "is_active": True
        }
    ]
    
    for event_data in events_data:
        event = Event(**event_data)
        db.add(event)
    
    await db.commit()
    print("✅ Events created")


async def create_speakers(db: AsyncSession):
    """Create sample speakers"""
    print("Creating speakers...")
    
    speakers_data = [
        {
            "first_name": "Dr. Maria",
            "last_name": "Rodriguez",
            "title": "DDS, PhD",
            "company": "University of Barcelona",
            "bio": "Leading expert in digital implantology with over 15 years of experience in research and clinical practice.",
            "email": "maria.rodriguez@ub.edu",
            "linkedin": "https://linkedin.com/in/maria-rodriguez-dds"
        },
        {
            "first_name": "Prof. Thomas",
            "last_name": "Mueller",
            "title": "MD, DDS",
            "company": "Charité Berlin",
            "bio": "Renowned oral surgeon and researcher specializing in complex implant cases and bone regeneration.",
            "email": "thomas.mueller@charite.de",
            "linkedin": "https://linkedin.com/in/thomas-mueller-md"
        },
        {
            "first_name": "Dr. Lisa",
            "last_name": "Chen",
            "title": "DDS, MS",
            "company": "Digital Dentistry Institute",
            "bio": "Pioneer in CAD/CAM technology and digital workflow optimization for dental practices.",
            "email": "lisa.chen@ddi.com",
            "linkedin": "https://linkedin.com/in/lisa-chen-dds"
        },
        {
            "first_name": "Dr. Roberto",
            "last_name": "Silva",
            "title": "DDS, MSc",
            "company": "Neodent Research Center",
            "bio": "Clinical researcher focused on implant surface technology and osseointegration studies.",
            "email": "roberto.silva@neodent.com",
            "linkedin": "https://linkedin.com/in/roberto-silva-dds"
        }
    ]
    
    for speaker_data in speakers_data:
        speaker = Speaker(**speaker_data)
        db.add(speaker)
    
    await db.commit()
    print("✅ Speakers created")


async def create_sessions(db: AsyncSession):
    """Create sample sessions"""
    print("Creating sessions...")
    
    # Get events and speakers
    from sqlalchemy import select
    events_result = await db.execute(select(Event).order_by(Event.id))
    events = events_result.scalars().all()
    
    speakers_result = await db.execute(select(Speaker).order_by(Speaker.id))
    speakers = speakers_result.scalars().all()
    
    sessions_data = [
                 {
             "event_id": events[0].id,  # First event
             "title": "Digital Implant Planning: From Scan to Surgery",
             "description": "Learn the complete digital workflow for implant planning using advanced 3D imaging and surgical guides.",
             "start_time": datetime.now() + timedelta(days=30, hours=9),
             "end_time": datetime.now() + timedelta(days=30, hours=10, minutes=30),
             "location": "Main Auditorium",
             "session_type": SessionTypeEnum.scheduled,
             "max_participants": 200
         },
         {
             "event_id": events[0].id,
             "title": "Live Surgery Demonstration",
             "description": "Watch a live implant surgery with real-time commentary and Q&A session.",
             "start_time": datetime.now() + timedelta(days=30, hours=11),
             "end_time": datetime.now() + timedelta(days=30, hours=12),
             "location": "Surgery Theater",
             "session_type": SessionTypeEnum.live,
             "is_live": True,
             "max_participants": 100
         },
         {
             "event_id": events[0].id,
             "title": "Hands-on Workshop: CAD/CAM Restorations",
             "description": "Practical workshop on designing and milling custom restorations.",
             "start_time": datetime.now() + timedelta(days=30, hours=14),
             "end_time": datetime.now() + timedelta(days=30, hours=17),
             "location": "Workshop Room A",
             "session_type": SessionTypeEnum.workshop,
             "max_participants": 30
         },
         {
             "event_id": events[1].id,  # Second event
             "title": "Neodent Implant Systems Overview",
             "description": "Comprehensive overview of Neodent implant portfolio and clinical applications.",
             "start_time": datetime.now() + timedelta(days=60, hours=10),
             "end_time": datetime.now() + timedelta(days=60, hours=11, minutes=30),
             "location": "Conference Hall",
             "session_type": SessionTypeEnum.scheduled,
             "max_participants": 150
         },
         {
             "event_id": events[2].id,  # Third event (virtual)
             "title": "Virtual Reality in Dental Education",
             "description": "Exploring the use of VR technology for dental training and patient education.",
             "start_time": datetime.now() + timedelta(days=90, hours=15),
             "end_time": datetime.now() + timedelta(days=90, hours=16),
             "location": "Virtual Platform",
             "session_type": SessionTypeEnum.scheduled,
             "max_participants": 500
         }
    ]
    
    for session_data in sessions_data:
        session = Session(**session_data)
        db.add(session)
    
    await db.commit()
    print("✅ Sessions created")


async def create_neodent_products(db: AsyncSession):
    """Create sample Neodent products"""
    print("Creating Neodent products...")
    
    products_data = [
        {
            "name": "Neodent Grand Morse Implant",
            "description": "Premium implant system with Morse taper connection for superior stability and aesthetics.",
            "category": "Implants",
            "product_code": "GM-4.3x10",
            "image_url": "https://example.com/products/grand-morse.jpg",
            "brochure_url": "https://example.com/brochures/grand-morse.pdf"
        },
        {
            "name": "Neodent Drive Implant",
            "description": "Versatile implant system designed for immediate loading protocols.",
            "category": "Implants", 
            "product_code": "DR-3.75x11",
            "image_url": "https://example.com/products/drive.jpg",
            "brochure_url": "https://example.com/brochures/drive.pdf"
        },
        {
            "name": "Neodent Surgical Kit",
            "description": "Complete surgical kit with all necessary instruments for implant placement.",
            "category": "Instruments",
            "product_code": "SK-COMPLETE",
            "image_url": "https://example.com/products/surgical-kit.jpg",
            "brochure_url": "https://example.com/brochures/surgical-kit.pdf"
        },
        {
            "name": "Neodent Abutment Selection",
            "description": "Wide range of abutments for different clinical situations and restoration types.",
            "category": "Abutments",
            "product_code": "AB-SELECTION",
            "image_url": "https://example.com/products/abutments.jpg",
            "brochure_url": "https://example.com/brochures/abutments.pdf"
        }
    ]
    
    for product_data in products_data:
        product = NeodentProduct(**product_data)
        db.add(product)
    
    await db.commit()
    print("✅ Neodent products created")


async def create_badges(db: AsyncSession):
    """Create sample badges"""
    print("Creating badges...")
    
    badges_data = [
        {
            "name": "Event Attendee",
            "description": "Attended at least one STRAUMANN event",
            "icon_url": "https://example.com/badges/attendee.png",
            "criteria": {"events_attended": 1}
        },
        {
            "name": "Active Participant",
            "description": "Participated in 5 or more sessions",
            "icon_url": "https://example.com/badges/participant.png", 
            "criteria": {"sessions_attended": 5}
        },
        {
            "name": "Knowledge Seeker",
            "description": "Completed 3 surveys",
            "icon_url": "https://example.com/badges/knowledge.png",
            "criteria": {"surveys_completed": 3}
        },
        {
            "name": "Networking Pro",
            "description": "Connected with 10 other attendees",
            "icon_url": "https://example.com/badges/networking.png",
            "criteria": {"connections_made": 10}
        }
    ]
    
    for badge_data in badges_data:
        badge = Badge(**badge_data)
        db.add(badge)
    
    await db.commit()
    print("✅ Badges created")


async def create_static_pages(db: AsyncSession):
    """Create sample static pages"""
    print("Creating static pages...")
    
    pages_data = [
        {
            "slug": "about",
            "title": "About STRAUMANN",
            "content": """
            <h1>About STRAUMANN</h1>
            <p>The Straumann Group is a global leader in tooth replacement and orthodontic solutions that restore smiles and confidence. It unites global and international brands that stand for excellence, innovation and quality in replacement, corrective and digital dentistry.</p>
            <p>Our mission is to provide innovative, evidence-based solutions for dental professionals and their patients.</p>
            """,
            "language": "en"
        },
        {
            "slug": "privacy-policy",
            "title": "Privacy Policy",
            "content": """
            <h1>Privacy Policy</h1>
            <p>This privacy policy explains how we collect, use, and protect your personal information when you use our event platform.</p>
            <h2>Information We Collect</h2>
            <p>We collect information you provide directly to us, such as when you register for events or create an account.</p>
            """,
            "language": "en"
        },
        {
            "slug": "terms-of-service",
            "title": "Terms of Service", 
            "content": """
            <h1>Terms of Service</h1>
            <p>By using this platform, you agree to comply with and be bound by the following terms and conditions.</p>
            <h2>Use of the Platform</h2>
            <p>You may use this platform only for lawful purposes and in accordance with these terms.</p>
            """,
            "language": "en"
        }
    ]
    
    for page_data in pages_data:
        page = StaticPage(**page_data)
        db.add(page)
    
    await db.commit()
    print("✅ Static pages created")


async def create_sample_interactions(db: AsyncSession):
    """Create sample user interactions (favorites, registrations, etc.)"""
    print("Creating sample interactions...")
    
    # Get users, events, sessions, speakers
    from sqlalchemy import select
    users_result = await db.execute(select(User).where(User.role != UserRole.ADMIN).order_by(User.id).limit(3))
    users = users_result.scalars().all()
    
    events_result = await db.execute(select(Event).order_by(Event.id).limit(2))
    events = events_result.scalars().all()
    
    sessions_result = await db.execute(select(Session).order_by(Session.id).limit(3))
    sessions = sessions_result.scalars().all()
    
    speakers_result = await db.execute(select(Speaker).order_by(Speaker.id).limit(2))
    speakers = speakers_result.scalars().all()
    
    # Create session registrations
    for i, user in enumerate(users):
        for j, session in enumerate(sessions[:2]):  # Each user registers for 2 sessions
            user_session = UserSession(
                user_id=user.id,
                session_id=session.id,
                attended=j == 0  # First session attended, second not yet
            )
            db.add(user_session)
    
    # Create favorites
    favorites_data = [
        # User 1 favorites
        {"user_id": users[0].id, "favoritable_type": FavoritableTypeEnum.session, "favoritable_id": sessions[0].id},
        {"user_id": users[0].id, "favoritable_type": FavoritableTypeEnum.speaker, "favoritable_id": speakers[0].id},
        
        # User 2 favorites
        {"user_id": users[1].id, "favoritable_type": FavoritableTypeEnum.session, "favoritable_id": sessions[1].id},
        {"user_id": users[1].id, "favoritable_type": FavoritableTypeEnum.speaker, "favoritable_id": speakers[1].id},
        
        # User 3 favorites
        {"user_id": users[2].id, "favoritable_type": FavoritableTypeEnum.session, "favoritable_id": sessions[0].id},
        {"user_id": users[2].id, "favoritable_type": FavoritableTypeEnum.session, "favoritable_id": sessions[2].id},
    ]
    
    for fav_data in favorites_data:
        favorite = Favorite(**fav_data)
        db.add(favorite)
    
    # Create notifications
    for user in users:
        notification = Notification(
            user_id=user.id,
            title="Welcome to STRAUMANN Events!",
            message="Thank you for joining our event platform. Don't miss upcoming sessions!",
            notification_type=NotificationTypeEnum.general,
            is_read=False
        )
        db.add(notification)
        
        # Session reminder
        notification2 = Notification(
            user_id=user.id,
            title="Session Starting Soon",
            message="Your registered session 'Digital Implant Planning' starts in 30 minutes.",
            notification_type=NotificationTypeEnum.session_reminder,
            is_read=True,
            scheduled_for=datetime.now() + timedelta(days=29, hours=23, minutes=30)
        )
        db.add(notification2)
    
    await db.commit()
    print("✅ Sample interactions created")


async def main():
    """Main function to seed all data"""
    print("🌱 Starting data seeding...")
    
    async with AsyncSessionLocal() as db:
        try:
            await create_users(db)
            await create_events(db)
            await create_speakers(db)
            await create_sessions(db)
            await create_neodent_products(db)
            await create_badges(db)
            await create_static_pages(db)
            await create_sample_interactions(db)
            
            print("\n🎉 Data seeding completed successfully!")
            print("\n📋 Login Credentials:")
            print("👨‍💼 Admin: admin@straumann.com / admin123")
            print("👤 User 1: john.doe@example.com / user123")
            print("👤 User 2: jane.smith@example.com / user123")
            print("👤 User 3: mike.wilson@example.com / user123")
            print("👤 User 4: sarah.johnson@example.com / user123")
            print("👤 User 5: david.brown@example.com / user123")
            
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())