import argparse
from getpass import getpass

from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import Organization, User, UserRole


def main():
    parser = argparse.ArgumentParser(description="Create the first HR administrator.")
    parser.add_argument("--organization", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--email", required=True)
    args = parser.parse_args()

    password = getpass("Initial admin password (12+ characters): ")
    confirmation = getpass("Confirm password: ")
    if password != confirmation:
        parser.error("Passwords do not match")
    if len(password) < 12:
        parser.error("Password must contain at least 12 characters")

    with SessionLocal() as db:
        organization = db.query(Organization).filter(
            Organization.name == args.organization
        ).first()
        if organization is None:
            organization = Organization(name=args.organization)
            db.add(organization)
            db.flush()

        existing = db.query(User).filter(
            User.organization_id == organization.id,
            User.username == args.username,
        ).first()
        if existing:
            parser.error("That username already exists in this organization")

        admin = User(
            organization_id=organization.id,
            username=args.username,
            email=args.email,
            password_hash=hash_password(password),
            role=UserRole.HR_ADMIN,
            is_active=True,
        )
        db.add(admin)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            parser.error("Could not create administrator; verify organization/email uniqueness")
        print(f"Created HR administrator for organization ID {organization.id}")


if __name__ == "__main__":
    main()
