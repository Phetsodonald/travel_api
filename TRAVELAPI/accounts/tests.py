from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User=get_user_model()

class AccountTests(APITestCase):

    def test_register(self):
        r=self.client.post('/api/accounts/register/',{'username':'new','email':'new@example.com','password':'password123','password_confirm':'password123'}); self.assertEqual(r.status_code,201)

    def test_register_password_mismatch(self):
        r=self.client.post('/api/accounts/register/',{'username':'new2','email':'new2@example.com','password':'password123','password_confirm':'different'}); self.assertEqual(r.status_code,400)

    def test_login(self):
        User.objects.create_user(username='tester',email='t@example.com',password='pass12345'); r=self.client.post('/api/accounts/login/',{'username':'tester','password':'pass12345'}); self.assertEqual(r.status_code,200)

    def test_invalid_login(self):
        User.objects.create_user(username='tester2',email='t2@example.com',password='pass12345'); r=self.client.post('/api/accounts/login/',{'username':'tester2','password':'wrong'}); self.assertEqual(r.status_code,401)

    def test_profile_requires_authentication(self): 
        self.assertEqual(self.client.get('/api/accounts/profile/').status_code,401)

    def test_profile_and_password_change(self):
        u=User.objects.create_user(username='profile',email='p@example.com',password='pass12345'); self.client.force_authenticate(u); self.assertEqual(self.client.get('/api/accounts/profile/').status_code,200); self.assertEqual(self.client.patch('/api/accounts/password/change/',{'old_password':'pass12345','new_password':'newpass123'}).status_code,200)

    def test_register_missing_username(self):
        r = self.client.post(
            '/api/accounts/register/',
            {
                'email': 'missing@example.com',
                'password': 'password123',
                'password_confirm': 'password123'
            }
        )

        self.assertEqual(r.status_code, 400)


    def test_register_duplicate_username(self):
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='password123'
        )

        r = self.client.post(
            '/api/accounts/register/',
            {
                'username': 'existing',
                'email': 'new@example.com',
                'password': 'password123',
                'password_confirm': 'password123'
            }
        )

        self.assertEqual(r.status_code, 400)


    def test_login_inactive_user(self):
        user = User.objects.create_user(
            username='inactive',
            email='inactive@example.com',
            password='password123'
        )

        user.is_active = False
        user.save()

        r = self.client.post(
            '/api/accounts/login/',
            {
                'username': 'inactive',
                'password': 'password123'
            }
        )

        self.assertEqual(r.status_code, 401)


    def test_password_change_wrong_old_password(self):
        user = User.objects.create_user(
            username='passwordtest',
            email='password@example.com',
            password='password123'
        )

        self.client.force_authenticate(user)

        r = self.client.patch(
            '/api/accounts/password/change/',
            {
                'old_password': 'wrongpassword',
                'new_password': 'newpass123'
            }
        )

        self.assertEqual(r.status_code, 400)