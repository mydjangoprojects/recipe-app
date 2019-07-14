from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from recipe.models import Ingredient

INGREDIENT_LIST_URL = reverse('recipe:ingredient_list')


def url_by_action_and_pk(action, pk=1):
    """Return Ingredient URL by Action and PK"""
    return reverse(f'recipe:ingredient_{action}', args=[pk])


class PublicIngredientViewsTests(TestCase):
    """Tests for publicly accessed Ingredient's Views."""
    def setUp(self):
        self.client = Client()

    def test_ingredient_list_redirects_unauthenticated(self):
        """Test that Ingredient List view redirects unauthenticated users."""
        response = self.client.get(INGREDIENT_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_ingredient_detail_redirects_unauthenticated(self):
        """Test that Ingredient Detail view redirects unauthenticated users."""
        url = url_by_action_and_pk('detail')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_ingredient_update_redirects_unauthenticated(self):
        """Test that Ingredient Update view redirects unauthenticated users."""
        url = url_by_action_and_pk('update')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_ingredient_delete_redirects_unauthenticated(self):
        """Test that Ingredient Delete view redirects unauthenticated users."""
        url = url_by_action_and_pk('delete')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class PrivateIngredientViewsTests(TestCase):
    """Test the authorized user Ingredients Views"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            'test@domain.com',
            'testpass1'
        )
        self.client.force_login(self.user)

        self.ingredient = Ingredient.objects.create(name='First Ingredient',
                                                    user=self.user)

    def test_ingredient_list_GET(self):
        """Test retrieving List of Ingredients."""
        response = self.client.get(INGREDIENT_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'ingredient/ingredient_list.html')

    def test_ingredient_detail_GET(self):
        """Test retrieving Detail of Ingredient."""
        url = url_by_action_and_pk('detail', self.ingredient.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'ingredient/ingredient_detail.html')

    def test_ingredient_update_GET(self):
        """Test retrieving Update of Ingredient."""
        url = url_by_action_and_pk('update', self.ingredient.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'ingredient/ingredient_update.html')

    def test_ingredient_delete_GET(self):
        """Test retrieving Delete of Ingredient."""
        url = url_by_action_and_pk('delete', self.ingredient.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'ingredient/ingredient_delete.html')
