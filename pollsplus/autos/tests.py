#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from django.contrib.auth.models import User
from django.test import TestCase

from autos.models import Make, Auto


# Create your tests here.


class TestAutosLogic(TestCase):
    def test_add_then_remove_make_expect_zoro_makes(self):
        make = Make.objects.create(name="Test Make")
        self.assertEqual(Make.objects.count(), 1)
        make.delete()
        self.assertEqual(Make.objects.count(), 0)

    def test_add_then_remove_auto_expect_zero_autos(self):
        make = Make.objects.create(name="Test Make")
        auto = Auto.objects.create(make=make, nickname="Test Auto", mileage=1)
        self.assertEqual(Auto.objects.count(), 1)
        auto.delete()
        self.assertEqual(Auto.objects.count(), 0)


class TestAutosViews(TestCase):
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
        Make.objects.all().delete()
        Auto.objects.all().delete()

    def add_make(self):
        self.make_name = "Test Make"
        self.make: Make = Make.objects.create(name=self.make_name)
        self.make.save()

    def make_auto(self):
        self.add_make()
        self.auto_name = "Test Auto"
        self.auto_mileage = 1
        self.auto: Auto = Auto.objects.create(
            make=self.make, nickname=self.auto_name, mileage=self.auto_mileage
        )
        self.auto.save()

    def test_auto_list_view_expect_zero_make_in_context(self):
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["make_count"], 0)

    def test_auto_list_view_expect_zero_makes_in_html(self):
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "(0)"
        )

    def test_auto_list_view_expect_add_make_message_in_html(self):
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please add a make before you add an auto."
        )

    def test_add_make_expect_one_make_in_context(self):
        self.add_make()
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["make_count"], 1)

    def test_add_make_expect_one_make_in_html(self):
        self.add_make()
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "(1)"
        )

    def test_add_make_then_delete_expect_zero_makes_in_context(self):
        self.add_make()
        self.make.delete()
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["make_count"], 0)

    def test_add_make_then_delete_expect_zero_makes_in_html(self):
        self.add_make()
        self.make.delete()
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "(0)"
        )

    def test_add_make_then_delete_expect_add_make_message_in_html(self):
        self.add_make()
        self.make.delete()
        response = self.client.get("/autos/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please add a make before you add an auto."
        )

if __name__ == "__main__":
    TestCase.main()
