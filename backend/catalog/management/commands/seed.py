from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from catalog.models import Category, Business, Service
from transactions.models import Booking, Payment
from engagement.models import Review, Message


class Command(BaseCommand):
    help = "Seed the database with demo data for GroomBuzz."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing seeded data before inserting new data.",
        )
        parser.add_argument(
            "--services",
            type=int,
            default=20,
            help="Number of services to create (default: 20).",
        )
        parser.add_argument(
            "--bookings",
            type=int,
            default=10,
            help="Number of bookings to create (default: 10).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        reset = options["reset"]
        num_services = options["services"]
        num_bookings = options["bookings"]

        User = get_user_model()

        if reset:
            self.stdout.write(self.style.WARNING("Resetting data..."))
            Review.objects.all().delete()
            Message.objects.all().delete()
            Payment.objects.all().delete()
            Booking.objects.all().delete()
            Service.objects.all().delete()
            Business.objects.all().delete()
            Category.objects.all().delete()
            # Note: We do NOT delete users by default (safer).
            self.stdout.write(self.style.SUCCESS("Data reset complete."))

        # ---- Users ----
        # Owners
        owner1, _ = User.objects.get_or_create(
            username="owner1",
            defaults={"email": "owner1@groombuzz.test"},
        )
        owner1.set_password("Pass1234!")
        owner1.save()

        owner2, _ = User.objects.get_or_create(
            username="owner2",
            defaults={"email": "owner2@groombuzz.test"},
        )
        owner2.set_password("Pass1234!")
        owner2.save()

        # Clients
        client1, _ = User.objects.get_or_create(
            username="client1",
            defaults={"email": "client1@groombuzz.test"},
        )
        client1.set_password("Pass1234!")
        client1.save()

        client2, _ = User.objects.get_or_create(
            username="client2",
            defaults={"email": "client2@groombuzz.test"},
        )
        client2.set_password("Pass1234!")
        client2.save()

        owners = [owner1, owner2]
        clients = [client1, client2]

        # ---- Categories ----
        categories_data = [
            ("Barbershop", "barbershop"),
            ("Hair Salon", "hair-salon"),
            ("Nail Salon", "nail-salon"),
            ("Skincare", "skincare"),
            ("Massage", "massage"),
            ("Makeup", "makeup"),
        ]

        categories = []
        for name, slug in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": f"{name} services"},
            )
            categories.append(cat)

        # ---- Businesses ----
        businesses_data = [
            ("Kings Barber Lounge", "Top-tier fades and grooming", "Pretoria", "Hatfield"),
            ("GlowUp Nails Studio", "Nails, lashes & brows", "Pretoria", "Brooklyn"),
            ("Smooth Skin Clinic", "Facials and skincare treatments", "Johannesburg", "Sandton"),
            ("Relax & Restore Spa", "Massage therapy and recovery", "Johannesburg", "Rosebank"),
        ]

        businesses = []
        for i, (name, desc, city, area) in enumerate(businesses_data):
            owner = owners[i % len(owners)]
            biz, _ = Business.objects.get_or_create(
                name=name,
                defaults={
                    "owner": owner,
                    "description": desc,
                    "city": city,
                    "area": area,
                    "address": f"{random.randint(1, 99)} Main Road",
                    "phone_number": f"+27 6{random.randint(10000000, 99999999)}",
                    "is_active": True,
                },
            )
            # If business existed but owner differs, keep existing owner (just to avoid surprises).
            businesses.append(biz)

        # ---- Services ----
        service_names = [
            "Fade Haircut",
            "Beard Trim",
            "Classic Shave",
            "Wash & Blow",
            "Braids",
            "Gel Nails",
            "Manicure",
            "Pedicure",
            "Deep Cleansing Facial",
            "Hydrating Facial",
            "Swedish Massage",
            "Deep Tissue Massage",
            "Lash Extensions",
            "Brow Shaping",
            "Makeup Session",
        ]

        created_services = []
        # Distribute services across businesses
        for n in range(num_services):
            business = random.choice(businesses)
            category = random.choice(categories)
            name = random.choice(service_names)
            price = random.choice([80, 120, 150, 200, 250, 300, 450, 600])

            svc = Service.objects.create(
                business=business,
                category=category,
                name=f"{name} #{n+1}",
                description=f"{name} at {business.name}",
                price=price,
                currency="ZAR",
                duration_minutes=random.choice([30, 45, 60, 90]),
                is_available=True,
            )
            created_services.append(svc)

        # ---- Bookings ----
        created_bookings = []
        now = timezone.now()
        for i in range(num_bookings):
            client = random.choice(clients)
            service = random.choice(created_services)

            scheduled_at = now + timedelta(days=random.randint(1, 14), hours=random.randint(1, 8))
            status = random.choice(
                [Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.COMPLETED]
            )

            booking = Booking.objects.create(
                client=client,
                service=service,
                scheduled_at=scheduled_at,
                status=status,
            )
            created_bookings.append(booking)

        # ---- Payments ----
        for booking in created_bookings:
            # Payment amount = service price for now (simple MVP)
            paid_status = random.choice([Payment.Status.PENDING, Payment.Status.COMPLETED])

            payment_date = timezone.now() if paid_status == Payment.Status.COMPLETED else None

            Payment.objects.create(
                booking=booking,
                amount=booking.service.price,
                payment_method=random.choice(
                    [Payment.Method.CARD, Payment.Method.MOBILE_MONEY, Payment.Method.CASH]
                ),
                payment_status=paid_status,
                payment_date=payment_date,
            )

        # ---- Messages ----
        for _ in range(10):
            client = random.choice(clients)
            business = random.choice(businesses)
            owner = business.owner

            # Alternate sender
            if random.choice([True, False]):
                sender, recipient = client, owner
                body = f"Hi, I’d like to book a service at {business.name}. Do you have availability?"
            else:
                sender, recipient = owner, client
                body = f"Hello! Yes, we’re available. Please select a time and confirm your booking."

            Message.objects.create(
                sender=sender,
                recipient=recipient,
                business=business,
                message_body=body,
            )

        # ---- Reviews ----
        # Only for COMPLETED bookings 
        completed_bookings = [b for b in created_bookings if b.status == Booking.Status.COMPLETED]
        for booking in completed_bookings[: min(5, len(completed_bookings))]:
            Review.objects.create(
                booking=booking,
                business=booking.service.business,
                client=booking.client,
                rating=random.randint(3, 5),
                comment=random.choice(
                    [
                        "Great service, very professional!",
                        "Loved the experience. Will come again.",
                        "Clean, fast, and friendly.",
                        "Excellent attention to detail!",
                    ]
                ),
            )

        # ---- Output summary ----
        self.stdout.write(self.style.SUCCESS("✅ GroomBuzz seed completed!"))
        self.stdout.write(f"Users: owners (owner1/owner2), clients (client1/client2) [Pass1234!]")
        self.stdout.write(f"Categories: {Category.objects.count()}")
        self.stdout.write(f"Businesses: {Business.objects.count()}")
        self.stdout.write(f"Services: {Service.objects.count()}")
        self.stdout.write(f"Bookings: {Booking.objects.count()}")
        self.stdout.write(f"Payments: {Payment.objects.count()}")
        self.stdout.write(f"Messages: {Message.objects.count()}")
        self.stdout.write(f"Reviews: {Review.objects.count()}")
