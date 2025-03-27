from django.core.management.base import BaseCommand
from django.db import connection
from decimal import Decimal
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class Command(BaseCommand):
    help = '加载初始数据'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # 创建测试用户
            test_users = [
                ('测试用户1', 'test1@example.com', '13800138001'),
                ('测试用户2', 'test2@example.com', '13800138002'),
                ('测试用户3', 'test3@example.com', '13800138003'),
            ]
            
            for username, email, phone in test_users:
                cursor.execute("""
                    INSERT INTO users_user (password, username, email, is_staff, is_active, is_superuser, date_joined, phone, is_verified)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE username=username
                """, [
                    make_password('test123'),
                    username,
                    email,
                    False,
                    True,
                    False,
                    timezone.now(),
                    phone,
                    True
                ])

            # 创建测试房源
            test_properties = [
                {
                    'title': '朝阳区三居室精装修房',
                    'description': '位于朝阳区核心地段，交通便利，周边配套设施齐全。',
                    'price': Decimal('8000000.00'),
                    'perprice': 80000,
                    'rooms': '3室2厅',
                    'areas': '100平米',
                    'direction': '南北通透',
                    'zhuangXiu': '精装修',
                    'floor': '15/18层',
                    'Structure': '钢混',
                    'features': '地铁沿线,学区房,精装修',
                    'url': 'https://example.com/property/1',
                },
                {
                    'title': '海淀区两居室刚需房',
                    'description': '位于海淀区学区房地段，紧邻地铁，适合刚需购房。',
                    'price': Decimal('6000000.00'),
                    'perprice': 75000,
                    'rooms': '2室1厅',
                    'areas': '80平米',
                    'direction': '东西向',
                    'zhuangXiu': '简装',
                    'floor': '6/12层',
                    'Structure': '板楼',
                    'features': '地铁沿线,学区房',
                    'url': 'https://example.com/property/2',
                },
                {
                    'title': '西城区四合院整租',
                    'description': '百年老宅，原汁原味四合院，适合追求传统文化的购房者。',
                    'price': Decimal('12000000.00'),
                    'perprice': 100000,
                    'rooms': '4室2厅',
                    'areas': '120平米',
                    'direction': '坐北朝南',
                    'zhuangXiu': '中式装修',
                    'floor': '1/1层',
                    'Structure': '砖木',
                    'features': '文化保护区,四合院',
                    'url': 'https://example.com/property/3',
                }
            ]
            
            for prop in test_properties:
                cursor.execute("""
                    INSERT INTO properties_property 
                    (title, description, price, perprice, rooms, areas, direction, zhuangXiu, floor, Structure, features, url, created_at, updated_at, is_available)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)
                    ON DUPLICATE KEY UPDATE title=title
                """, [
                    prop['title'],
                    prop['description'],
                    prop['price'],
                    prop['perprice'],
                    prop['rooms'],
                    prop['areas'],
                    prop['direction'],
                    prop['zhuangXiu'],
                    prop['floor'],
                    prop['Structure'],
                    prop['features'],
                    prop['url'],
                    True
                ])
                
                # 获取房源ID
                cursor.execute("SELECT id FROM properties_property WHERE title = %s", [prop['title']])
                property_id = cursor.fetchone()[0]

                # 创建房源图片
                cursor.execute("""
                    INSERT INTO properties_propertyimage (image, is_main, property_id)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE image=image
                """, [f'https://example.com/images/{property_id}_1.jpg', True, property_id])

                cursor.execute("""
                    INSERT INTO properties_propertyimage (image, is_main, property_id)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE image=image
                """, [f'https://example.com/images/{property_id}_2.jpg', False, property_id])

            # 创建收藏记录
            cursor.execute("SELECT id FROM users_user WHERE username = '测试用户1'")
            user_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT id FROM properties_property LIMIT 2")
            property_ids = cursor.fetchall()
            
            for property_id in property_ids:
                cursor.execute("""
                    INSERT INTO properties_favorite (user_id, property_id, created_at)
                    VALUES (%s, %s, NOW())
                    ON DUPLICATE KEY UPDATE created_at=created_at
                """, [user_id, property_id[0]])

            self.stdout.write(self.style.SUCCESS('数据加载完成')) 