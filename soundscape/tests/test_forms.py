from django import forms
from soundscape.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.test import TestCase


class LoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="TestPass123!"
        )

    def test_login_form_valid_data(self):
        """Test login form with valid credentials"""
        form_data = {"username": "testuser", "password": "TestPass123!"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        """Test login form with invalid credentials"""
        form_data = {"username": "testuser", "password": "wrongpassword"}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_login_form_missing_fields(self):
        """Test login form with missing fields"""
        form_data = {"username": "testuser"}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_login_form_widget_attrs(self):
        """Test that form widgets have correct attributes"""
        form = LoginForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Your username"
        )
        self.assertEqual(
            form.fields["username"].widget.attrs["class"], "w-full py-4 px-6 rounded-xl"
        )
        self.assertEqual(
            form.fields["password"].widget.attrs["placeholder"], "Your password"
        )
        self.assertEqual(
            form.fields["password"].widget.attrs["class"], "w-full py-4 px-6 rounded-xl"
        )


class SignupFormTest(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        }

    def test_signup_form_valid_data(self):
        """Test signup form with valid data"""
        form = SignupForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_saves_correctly(self):
        """Test that form saves user correctly"""
        form = SignupForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("TestPass123!"))

    def test_signup_form_password_mismatch(self):
        """Test signup form with mismatched passwords"""
        form_data = self.valid_form_data.copy()
        form_data["password2"] = "DifferentPass123!"
        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_signup_form_invalid_email(self):
        """Test signup form with invalid email"""
        form_data = self.valid_form_data.copy()
        form_data["email"] = "invalid-email"
        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_signup_form_duplicate_username(self):
        """Test signup form with existing username"""
        User.objects.create_user(
            username="newuser", email="existing@example.com", password="TestPass123!"
        )
        form = SignupForm(data=self.valid_form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_signup_form_required_fields(self):
        """Test that all fields are required"""
        form = SignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_signup_form_widget_attrs(self):
        """Test that form widgets have correct attributes"""
        form = SignupForm()
        fields = ["username", "email", "password1", "password2"]
        expected_class = "w-full py-4 px-6 rounded-xl"

        for field in fields:
            self.assertEqual(form.fields[field].widget.attrs["class"], expected_class)

        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Your username"
        )
        self.assertEqual(
            form.fields["email"].widget.attrs["placeholder"], "Your email address"
        )
        self.assertEqual(
            form.fields["password1"].widget.attrs["placeholder"], "Your password"
        )
        self.assertEqual(
            form.fields["password2"].widget.attrs["placeholder"], "Repeat password"
        )

    def test_signup_form_email_field_type(self):
        """Test that email field uses EmailInput widget"""
        form = SignupForm()
        self.assertTrue(isinstance(form.fields["email"].widget, forms.EmailInput))
