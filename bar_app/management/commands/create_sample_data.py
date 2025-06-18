from django.core.management.base import BaseCommand
from bar_app.models import Category, Beer, NyamaChoma, Table
from accommodation.models import RoomType, Room

class Command(BaseCommand):
    help = 'Create sample data for the bar website'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Local Beers', 'description': 'Locally brewed beers from Kenya'},
            {'name': 'Imported Beers', 'description': 'Premium imported beers'},
            {'name': 'Craft Beers', 'description': 'Artisanal craft beers'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample beers
        beers_data = [
            {
                'name': 'Tusker Lager', 'brand': 'Tusker', 'beer_type': 'lager',
                'alcohol_content': 4.2, 'price': 250, 'category': 'Local Beers',
                'description': 'Kenya\'s premium lager beer with a crisp, refreshing taste.'
            },
            {
                'name': 'White Cap', 'brand': 'White Cap', 'beer_type': 'lager',
                'alcohol_content': 4.0, 'price': 230, 'category': 'Local Beers',
                'description': 'A smooth, light lager perfect for any occasion.'
            },
            {
                'name': 'Guinness Stout', 'brand': 'Guinness', 'beer_type': 'stout',
                'alcohol_content': 4.2, 'price': 300, 'category': 'Imported Beers',
                'description': 'Rich, creamy stout with distinctive flavor.'
            },
            {
                'name': 'Heineken', 'brand': 'Heineken', 'beer_type': 'lager',
                'alcohol_content': 5.0, 'price': 350, 'category': 'Imported Beers',
                'description': 'Premium Dutch lager with a distinctive taste.'
            },
            {
                'name': 'Corona Extra', 'brand': 'Corona', 'beer_type': 'lager',
                'alcohol_content': 4.5, 'price': 400, 'category': 'Imported Beers',
                'description': 'Light, crisp Mexican beer perfect with lime.'
            },
            {
                'name': 'Pilsner Urquell', 'brand': 'Pilsner Urquell', 'beer_type': 'pilsner',
                'alcohol_content': 4.4, 'price': 450, 'category': 'Imported Beers',
                'description': 'Original Czech pilsner with a distinctive hoppy taste.'
            },
        ]

        for beer_data in beers_data:
            category = categories[beer_data.pop('category')]
            beer, created = Beer.objects.get_or_create(
                name=beer_data['name'],
                brand=beer_data['brand'],
                defaults={**beer_data, 'category': category}
            )
            if created:
                self.stdout.write(f'Created beer: {beer.brand} {beer.name}')

        # Create sample nyama choma
        nyama_data = [
            {
                'name': 'Beef Ribs', 'meat_type': 'beef', 'price_per_kg': 1200,
                'spice_level': 3, 'description': 'Tender beef ribs grilled to perfection with traditional spices.'
            },
            {
                'name': 'Goat Chops', 'meat_type': 'goat', 'price_per_kg': 1500,
                'spice_level': 4, 'description': 'Succulent goat meat chops with authentic Kenyan spices.'
            },
            {
                'name': 'Chicken Wings', 'meat_type': 'chicken', 'price_per_kg': 800,
                'spice_level': 2, 'description': 'Juicy chicken wings marinated and grilled to perfection.'
            },
            {
                'name': 'Fish Fillet', 'meat_type': 'fish', 'price_per_kg': 1000,
                'spice_level': 2, 'description': 'Fresh fish fillet grilled with herbs and spices.'
            },
            {
                'name': 'Pork Ribs', 'meat_type': 'pork', 'price_per_kg': 1100,
                'spice_level': 3, 'description': 'Smoky pork ribs with a perfect blend of spices.'
            },
            {
                'name': 'Mutton Chops', 'meat_type': 'mutton', 'price_per_kg': 1400,
                'spice_level': 4, 'description': 'Flavorful mutton chops with traditional seasonings.'
            },
        ]

        for nyama_item in nyama_data:
            nyama, created = NyamaChoma.objects.get_or_create(
                name=nyama_item['name'],
                defaults=nyama_item
            )
            if created:
                self.stdout.write(f'Created nyama choma: {nyama.name}')

        # Create sample tables
        table_data = [
            {'table_number': 1, 'capacity': 4, 'location': 'indoor'},
            {'table_number': 2, 'capacity': 6, 'location': 'indoor'},
            {'table_number': 3, 'capacity': 2, 'location': 'outdoor'},
            {'table_number': 4, 'capacity': 8, 'location': 'VIP'},
            {'table_number': 5, 'capacity': 4, 'location': 'outdoor'},
            {'table_number': 6, 'capacity': 6, 'location': 'outdoor'},
            {'table_number': 7, 'capacity': 2, 'location': 'indoor'},
            {'table_number': 8, 'capacity': 10, 'location': 'VIP'},
        ]

        for table_item in table_data:
            table, created = Table.objects.get_or_create(
                table_number=table_item['table_number'],
                defaults=table_item
            )
            if created:
                self.stdout.write(f'Created table: Table {table.table_number}')

        # Create room types and rooms
        room_types_data = [
            {
                'name': 'Standard Room', 'description': 'Comfortable room with basic amenities including WiFi, TV, and private bathroom',
                'base_price': 3500, 'max_occupancy': 2
            },
            {
                'name': 'Deluxe Room', 'description': 'Spacious room with premium amenities including mini bar and balcony',
                'base_price': 5000, 'max_occupancy': 3
            },
            {
                'name': 'Suite', 'description': 'Luxury suite with separate living area and kitchenette',
                'base_price': 8000, 'max_occupancy': 4
            },
            {
                'name': 'Family Room', 'description': 'Large room perfect for families with multiple beds',
                'base_price': 6500, 'max_occupancy': 6
            },
        ]

        room_types = {}
        for rt_data in room_types_data:
            room_type, created = RoomType.objects.get_or_create(
                name=rt_data['name'],
                defaults=rt_data
            )
            room_types[rt_data['name']] = room_type
            if created:
                self.stdout.write(f'Created room type: {room_type.name}')

        # Create sample rooms
        rooms_data = [
            {'room_number': '101', 'room_type': 'Standard Room', 'amenities': 'WiFi, TV, AC, Private Bathroom, Room Service'},
            {'room_number': '102', 'room_type': 'Standard Room', 'amenities': 'WiFi, TV, AC, Private Bathroom, Room Service'},
            {'room_number': '103', 'room_type': 'Standard Room', 'amenities': 'WiFi, TV, AC, Private Bathroom, Room Service'},
            {'room_number': '201', 'room_type': 'Deluxe Room', 'amenities': 'WiFi, TV, AC, Mini Bar, Balcony, Room Service, Safe'},
            {'room_number': '202', 'room_type': 'Deluxe Room', 'amenities': 'WiFi, TV, AC, Mini Bar, Balcony, Room Service, Safe'},
            {'room_number': '301', 'room_type': 'Suite', 'amenities': 'WiFi, TV, AC, Mini Bar, Living Area, Kitchenette, Balcony, Safe'},
            {'room_number': '302', 'room_type': 'Suite', 'amenities': 'WiFi, TV, AC, Mini Bar, Living Area, Kitchenette, Balcony, Safe'},
            {'room_number': '401', 'room_type': 'Family Room', 'amenities': 'WiFi, TV, AC, Multiple Beds, Private Bathroom, Mini Fridge'},
        ]

        for room_data in rooms_data:
            room_type = room_types[room_data.pop('room_type')]
            room, created = Room.objects.get_or_create(
                room_number=room_data['room_number'],
                defaults={**room_data, 'room_type': room_type}
            )
            if created:
                self.stdout.write(f'Created room: {room.room_number} - {room.room_type.name}')

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('✅ Successfully created sample data!')
        )
        self.stdout.write('')
        self.stdout.write('📊 Summary:')
        self.stdout.write(f'   • Categories: {Category.objects.count()}')
        self.stdout.write(f'   • Beers: {Beer.objects.count()}')
        self.stdout.write(f'   • Nyama Choma: {NyamaChoma.objects.count()}')
        self.stdout.write(f'   • Tables: {Table.objects.count()}')
        self.stdout.write(f'   • Room Types: {RoomType.objects.count()}')
        self.stdout.write(f'   • Rooms: {Room.objects.count()}')
        self.stdout.write('')
        self.stdout.write('🎯 Next Steps:')
        self.stdout.write('   1. Go to http://127.0.0.1:8000/admin/')
        self.stdout.write('   2. Login with your superuser account')
        self.stdout.write('   3. Add images to beers, nyama choma, and rooms')
        self.stdout.write('   4. Visit the website to see your content!')
