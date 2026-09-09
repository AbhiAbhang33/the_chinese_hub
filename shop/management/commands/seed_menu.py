import re
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from shop.models import Category, FoodItem


# Format:
# "Category": [
#     (name, half_price, full_price, is_veg),
#     ...
# ]
MENU = {
    "Soups": [
        ("Veg Manchow Soup", None, 40, True),
        ("Chicken Manchow Soup", None, 40, False),
    ],

    "Manchurian": [
        ("Veg Manchurian (Dry)", 70, 140, True),
        ("Veg Manchurian (Gravy)", 100, 160, True),
        ("Veg Crispy Manchurian", 80, 140, True),
        ("Chicken Manchurian (Dry)", 130, 210, False),
    ],

    "Chicken Specials": [
        ("Chicken Masala Lollipop", 120, 220, False),
        ("Chicken Oil Fry Lollipop", 100, 200, False),
        ("Chicken 65 Boneless", 100, 200, False),
        ("Chicken Bel Crispy", 100, 200, False),
    ],

    "Noodles": [
        ("Veg Manchurian Noodles", 70, 140, True),
        ("Veg Triple Noodles", 100, 200, True),
        ("Veg Combination Noodles", 70, 140, True),
        ("Chicken Noodles", 80, 160, False),
        ("Chicken Triple Noodles", 100, 200, False),
        ("Chicken Combination Noodles", 80, 160, False),
    ],

    "Rice": [
        ("Veg Manchurian Rice", 70, 140, True),
        ("Veg Triple Rice", 100, 200, True),
        ("Veg Combination Rice", 70, 140, True),
        ("Chicken Fried Rice", 80, 160, False),
        ("Chicken Triple Rice", 100, 200, False),
        ("Chicken Combination Rice", 80, 160, False),
    ],

    "Beverages": [
        ("Sting", None, 25, True),
        ("Coke Cola", None, None, True),
    ],
}


class Command(BaseCommand):
    help = "Seed the database with a sample Chinese Hub menu (safe to re-run)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--images-dir",
            type=str,
            default=None,
            help=(
                "Folder of photos named after each dish, e.g. "
                "chicken_lollipop.jpg "
                "(spaces/case/extension don't matter - "
                "'Chicken Lollipop.PNG' also matches)."
            ),
        )

    def _slug(self, name):
        """
        Convert a food name into a normalized slug.

        Example:
            Chicken Lollipop -> chicken_lollipop
            Chicken 65 Boneless -> chicken_65_boneless
        """
        return re.sub(
            r"[^a-z0-9]+",
            "_",
            name.lower()
        ).strip("_")

    def handle(self, *args, **options):
        images_dir = options.get("images_dir")

        # ---------------------------------------------------------
        # Build image lookup
        # ---------------------------------------------------------
        image_lookup = {}

        if images_dir:
            folder = Path(images_dir)

            if folder.is_dir():
                for image_file in folder.iterdir():

                    if image_file.suffix.lower() in (
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".webp",
                    ):
                        image_lookup[
                            self._slug(image_file.stem)
                        ] = image_file

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Images dir not found: {images_dir}"
                    )
                )

        # ---------------------------------------------------------
        # Seed categories and food items
        # ---------------------------------------------------------
        for order_index, (category_name, items) in enumerate(
            MENU.items()
        ):

            category, category_created = (
                Category.objects.get_or_create(
                    name=category_name,
                    defaults={
                        "order": order_index
                    },
                )
            )

            # If category already exists, make sure its order is correct
            if not category_created and category.order != order_index:
                category.order = order_index
                category.save(update_fields=["order"])

            # -----------------------------------------------------
            # Seed food items
            # -----------------------------------------------------
            for name, half, full, is_veg in items:

                food_item, created = (
                    FoodItem.objects.get_or_create(
                        category=category,
                        name=name,
                        defaults={
                            "half_price": half,
                            "full_price": full,
                            "is_veg": is_veg,
                        },
                    )
                )

                # -------------------------------------------------
                # Update existing items too
                # -------------------------------------------------
                if not created:

                    food_item.half_price = half
                    food_item.full_price = full
                    food_item.is_veg = is_veg

                    food_item.save(
                        update_fields=[
                            "half_price",
                            "full_price",
                            "is_veg",
                        ]
                    )

                # -------------------------------------------------
                # Attach image if available
                # -------------------------------------------------
                if image_lookup:

                    match = image_lookup.get(
                        self._slug(name)
                    )

                    if match and not food_item.image:

                        with open(match, "rb") as fh:

                            food_item.image.save(
                                match.name,
                                File(fh),
                                save=True,
                            )

                        self.stdout.write(
                            f"  Attached image for {name}"
                        )

                # -------------------------------------------------
                # Display result
                # -------------------------------------------------
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Added: {name}"
                        )
                    )
                else:
                    self.stdout.write(
                        f"  Updated: {name}"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Sample menu seeded successfully."
            )
        )