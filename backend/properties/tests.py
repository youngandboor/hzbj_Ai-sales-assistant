from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from users.models import User
from .models import Property, PropertyImage, Favorite

class PropertyAPITests(APITestCase):
    def setUp(self):
        """测试前的准备工作"""
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone='13800138000'
        )
        
        # 创建测试房源
        self.property = Property.objects.create(
            title='测试房源',
            description='这是一个测试房源',
            price=1000000,
            perprice=50000,
            rooms='3室2厅',
            areas='100',
            direction='南',
            zhuangXiu='精装',
            floor='18层',
            Structure='板楼',
            features='地铁房',
            url='http://example.com/property/1',
            is_available=True
        )
        
        # 创建测试图片
        self.image = PropertyImage.objects.create(
            property=self.property,
            image='test.jpg',
            is_main=True
        )
        
        # 设置API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # 设置测试URL
        self.list_url = reverse('properties:properties-list')
        self.detail_url = reverse('properties:properties-detail', kwargs={'pk': self.property.id})
        self.favorite_url = reverse('properties:properties-favorite', kwargs={'pk': self.property.id})
        self.my_favorites_url = reverse('properties:favorite-list')

    def test_property_list(self):
        """测试获取房源列表"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)
        self.assertTrue(any(p['title'] == '测试房源' for p in response.data['results']))

    def test_property_detail(self):
        """测试获取房源详情"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '测试房源')

    def test_property_create(self):
        """测试创建房源"""
        data = {
            'title': '新测试房源',
            'description': '这是一个新的测试房源',
            'price': 2000000,
            'perprice': 20000,
            'rooms': '4室2厅',
            'areas': '150',
            'direction': '南',
            'zhuangXiu': '精装',
            'floor': '18层',
            'Structure': '板楼',
            'features': '地铁房',
            'url': 'http://example.com/property/2'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 2)

    def test_property_update(self):
        """测试更新房源"""
        data = {
            'title': '更新后的测试房源',
            'price': 1500000
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.property.refresh_from_db()
        self.assertEqual(self.property.title, '更新后的测试房源')
        self.assertEqual(float(self.property.price), 1500000)

    def test_property_delete(self):
        """测试删除房源"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 0)

    def test_toggle_favorite(self):
        """测试收藏/取消收藏"""
        # 创建一个房源
        property = Property.objects.create(
            title='测试房源',
            description='这是一个测试房源',
            price=1000000.00,
            perprice=10000,
            rooms='3室2厅',
            areas='120平米',
            direction='朝南',
            floor='18楼',
            Structure='板楼',
            features='精装修',
            url='http://example.com/property/1'
        )
        
        # 收藏房源
        favorite_url = reverse('properties:properties-favorite', args=[property.id])
        response = self.client.post(favorite_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '收藏成功')
        
        # 再次收藏同一个房源应该返回错误
        response = self.client.post(favorite_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], '已经收藏过了')
        
        # 取消收藏
        response = self.client.delete(favorite_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '取消收藏成功')
        
        # 再次取消收藏应该返回错误
        response = self.client.delete(favorite_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], '未收藏该房源')

    def test_my_favorites(self):
        """测试获取收藏列表"""
        # 创建两个房源
        property1 = Property.objects.create(
            title='测试房源1',
            description='这是测试房源1',
            price=1000000.00,
            perprice=10000,
            rooms='3室2厅',
            areas='120平米',
            direction='朝南',
            floor='18楼',
            Structure='板楼',
            features='精装修',
            url='http://example.com/property/1'
        )
        
        property2 = Property.objects.create(
            title='测试房源2',
            description='这是测试房源2',
            price=2000000.00,
            perprice=20000,
            rooms='4室2厅',
            areas='150平米',
            direction='朝南',
            floor='20楼',
            Structure='板楼',
            features='豪华装修',
            url='http://example.com/property/2'
        )
        
        # 收藏第一个房源
        favorite_url = reverse('properties:properties-favorite', kwargs={'pk': property1.id})
        self.client.post(favorite_url)
        
        # 获取收藏列表
        response = self.client.get(self.my_favorites_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '测试房源1')

    def test_property_detail_by_url(self):
        """测试通过 URL 获取房源详情"""
        response = self.client.get(f'{self.list_url}?url={self.property.url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)
        self.assertTrue(any(p['title'] == '测试房源' and p['url'] == 'http://example.com/property/1' for p in response.data['results']))

    def test_property_detail_by_url_not_found(self):
        """测试通过不存在的 URL 获取房源详情"""
        response = self.client.get(f'{self.list_url}?url=http://example.com/property/999')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_property_search(self):
        """测试房源搜索功能"""
        # 删除所有现有房源
        Property.objects.all().delete()
        
        # 创建测试房源
        property1 = Property.objects.create(
            title="豪华别墅",
            description="这是一个豪华别墅",
            price=1000000,
            perprice=10000,
            rooms="3室2厅",
            areas=150,
            features="游泳池"
        )
        
        property2 = Property.objects.create(
            title="普通公寓",
            description="这是一个普通公寓",
            price=500000,
            perprice=5000,
            rooms="2室1厅",
            areas=80,
            features="地铁房"
        )
        
        # 测试关键词搜索
        response = self.client.get(f"{self.list_url}?search=豪华")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], "豪华别墅")
        
        # 测试价格过滤
        response = self.client.get(f"{self.list_url}?min_price=400000&max_price=600000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], "普通公寓")
        
        # 测试户型过滤
        response = self.client.get(f"{self.list_url}?rooms=3室2厅")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], "豪华别墅")
        
        # 测试面积过滤
        response = self.client.get(f"{self.list_url}?min_area=100&max_area=120")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        
        # 测试排序
        response = self.client.get(f"{self.list_url}?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], "普通公寓")
        
        response = self.client.get(f"{self.list_url}?ordering=-price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], "豪华别墅")
        
        # 测试分页
        response = self.client.get(f"{self.list_url}?page_size=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue('next' in response.data)
        self.assertTrue('previous' in response.data)

    def test_get_property_image(self):
        """测试获取房源图片"""
        url = reverse('property-image', kwargs={'pk': self.property.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['image'], "http://example.com/test-image.jpg")
        self.assertEqual(response.data['property_id'], self.property.id)

    def test_get_nonexistent_property_image(self):
        """测试获取不存在的房源图片"""
        url = reverse('property-image', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
