# database/seed.py
from database.database import Base, engine, SessionLocal
from database.models import AlertModel

# Create database tables
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    if db.query(AlertModel).count() == 0:
        sample_alerts = [
            AlertModel(
                title="Wayanad Pass Sector 4",
                level="CRITICAL",
                message="High landslide risk detected due to heavy continuous rainfall.",
                risk_score=0.85,
                latitude=11.6050,
                longitude=76.0830
            ),
            AlertModel(
                title="Kalpetta North Slope",
                level="WARNING",
                message="Moderate risk of soil movement on steep gradients.",
                risk_score=0.62,
                latitude=11.6080,
                longitude=76.0780
            )
        ]
        db.add_all(sample_alerts)
        db.commit()
        print("Database tables created and sample alerts seeded successfully!")
    else:
        print("Database and tables created successfully! (Alerts already exist)")

    db.close()

if __name__ == "__main__":
    seed_data()