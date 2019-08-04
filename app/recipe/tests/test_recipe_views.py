import tempfile
from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from recipe.models import Recipe

RECIPE_LIST_URL = reverse('recipe:recipe_list')


def crud_url_by_action_and_pk(action, pk=1):
    """Return Recipe URL by Action and PK"""
    return reverse(f'recipe:recipe_{action}', args=[pk])


class PublicRecipeViewsTests(TestCase):
    """Tests for publicly accessed Recipe's Views."""
    def setUp(self):
        self.client = Client()

    def test_recipe_list_redirects_unauthenticated(self):
        """Test that Recipe List view redirects unauthenticated users."""
        response = self.client.get(RECIPE_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_recipe_detail_redirects_unauthenticated(self):
        """Test that Recipe Detail view redirects unauthenticated users."""
        url = crud_url_by_action_and_pk('detail')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_recipe_update_redirects_unauthenticated(self):
        """Test that Recipe Update view redirects unauthenticated users."""
        url = crud_url_by_action_and_pk('update')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_recipe_delete_redirects_unauthenticated(self):
        """Test that Recipe Delete view redirects unauthenticated users."""
        url = crud_url_by_action_and_pk('delete')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class PrivateRecipeViewsTests(TestCase):
    """Test the authorized user Recipes Views"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            'test@domain.com',
            'testpass1'
        )
        self.client.force_login(self.user)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            self.recipe = Recipe.objects.create(title='First Recipe',
                                                price=10.0,
                                                time_minutes=15,
                                                user=self.user)
            self.recipe.refresh_from_db()
            self.recipe.image.save('test.jpg', ntf)
            self.recipe.save()

    def login_as_superuser(self):
        """Utility function to login as superuser"""
        self.superuser = get_user_model().objects.create_superuser(
            'superuser@domain.com',
            'testpass1'
        )
        self.client.force_login(self.superuser)

    def login_as_another_user(self):
        """Utility function to login as another user.
           Which isn't the creator of the Recipe"""
        self.another_user = get_user_model().objects.create_user(
            'another_user@domain.com',
            'testpass1'
        )
        self.client.force_login(self.another_user)

    def test_recipe_list_GET(self):
        """Test retrieving List of Recipes."""
        response = self.client.get(RECIPE_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'recipe/recipe_list.html')

    def test_recipe_detail_GET(self):
        """Test retrieving Detail of Recipe."""
        url = crud_url_by_action_and_pk('detail', self.recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'recipe/recipe_detail.html')

    def test_recipe_update_GET(self):
        """Test retrieving Update of Recipe."""
        url = crud_url_by_action_and_pk('update', self.recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'recipe/recipe_update.html')

    def test_recipe_delete_GET(self):
        """Test retrieving Delete of Recipe."""
        url = crud_url_by_action_and_pk('delete', self.recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'recipe/recipe_delete.html')

    def test_recipe_update_GET_forbidden_for_another_user(self):
        """Test retrieving Update of Recipe is forbidden.
           For user which isn't the creator of the Recipe."""
        self.login_as_another_user()

        url = crud_url_by_action_and_pk('update', self.recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recipe_delete_GET_forbidden_for_another_user(self):
        """Test retrieving Delete of Recipe is forbidden.
           For user which isn't the creator of the Recipe."""
        self.login_as_another_user()

        url = crud_url_by_action_and_pk('delete', self.recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recipe_update_GET_always_accessible_for_superuser(self):
        """Test retrieving Update of Recipe is always accessible
           for superuser."""
        self.login_as_superuser()

        url = crud_url_by_action_and_pk('update', self.recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'recipe/recipe_update.html')

    def test_recipe_delete_GET_always_accessible_for_superuser(self):
        """Test retrieving Delete of Recipe is accessible
           always for superuser."""
        self.login_as_superuser()

        url = crud_url_by_action_and_pk('delete', self.recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'recipe/recipe_delete.html')
