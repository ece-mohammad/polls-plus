#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from cats.models import Breed, Cat


# Create your tests here.
class TestCatsLogic(TestCase):
    def test_add_then_remove_breed_expect_zero_breeds(self):
        breed = Breed(name="Test Breed")
        breed.save()
        self.assertEqual(Breed.objects.count(), 1)
        breed.delete()
        self.assertEqual(Breed.objects.count(), 0)

    def test_add_then_remove_cat_expect_zero_cats(self):
        breed = Breed(name="Test Breed")
        breed.save()
        cat = Cat(
            nickname="Test Cat",
            breed=breed,
            weight=1,
            foods="Test Foods"
        )
        cat.save()
        self.assertEqual(Cat.objects.count(), 1)
        cat.delete()
        self.assertEqual(Cat.objects.count(), 0)


class TestCatsViews(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.username = 'test_user'
        cls.password = '1234'
        cls.user: User = User(username=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.assertTrue(
            self.client.login(username=self.username, password=self.password),
            "Login failed"
        )

    def tearDown(self):
        self.client.logout()
        Breed.objects.all().delete()

    def add_breed(self):
        self.breed_name = 'Test Breed'
        self.breed = Breed(name=self.breed_name)
        self.breed.save()

    def add_cat(self):
        self.add_breed()
        self.cat_nickname = 'Test Cat'
        self.cat_weight = 1
        self.cat_foods = 'Test Foods'
        self.cat = Cat(
            nickname=self.cat_nickname,
            breed=self.breed,
            weight=self.cat_weight,
            foods=self.cat_foods
        )
        self.cat.save()

    def test_breeds_list_view_expect_add_breed_message_in_html(self):
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breed_count"], 0)
        self.assertContains(
            response,
            "Please add a breed before you add a cat."
        )

    def test_breeds_list_view_expect_zero_breeds_in_html(self):
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breed_count"], 0)
        self.assertContains(
            response,
            "(0)"
        )

    def test_breeds_list_view_expect_zero_breed_count_in_context(self):
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breed_count"], 0)

    def test_add_breed_expect_one_breed_in_context(self):
        self.add_breed()
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breed_count"], 1)

    def test_add_breed_expect_one_breed_in_hml(self):
        self.add_breed()
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "(1)"
        )

    def test_add_then_remove_breed_expect_zero_breeds_in_context(self):
        self.add_breed()
        self.breed.delete()
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["breed_count"], 0)

    def test_add_then_remove_breed_expect_zero_breeds_in_html(self):
        self.add_breed()
        self.breed.delete()
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "(0)"
        )

    def test_add_then_remove_breed_expect_add_breed_message_in_html(self):
        self.add_breed()
        self.breed.delete()
        response = self.client.get("/cats/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please add a breed before you add a cat."
        )

if __name__ == "__main__":
    TestCase.main()
