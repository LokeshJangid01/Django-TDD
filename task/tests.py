from django.test import TestCase
from .models import Task
from .forms import NewTaskForm,UpdateTaskForm


#Create your tests here.

class taskModelTest(TestCase):
    def test_task_model_exist(self):
        task = Task.objects.count()

        self.assertEqual(task,0)

    def test_model_has_string_represenetation(self):
        task = Task.objects.create(title = "First task")
        self.assertEqual(str(task), task.title)

class IndexPageTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title = "First task")

    def test_index_page_test(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'task/index.html')
        self.assertEqual(response.status_code, 200)

    def test_index_page_has_task(self):
        
        response = self.client.get('/')
        

        self.assertContains(response, self.task.title)

class DetailPageTest(TestCase):

    def setUp(self):
        self.task = Task.objects.create(title = "First task",dscription = "This dscription for task.")
        self.task2 = Task.objects.create(title = "Second task",dscription = "This dscription for Second task.")

    def test_detail_page_has_task(self):
        response = self.client.get(f'/{self.task.id}')
        self.assertTemplateUsed(response, 'task/detail.html')
        # self.assertEqual(response.status_code, 200)

    def test_detail_page_has_correct_content(self):
        response = self.client.get(f'/{self.task.id}')
        
        
        self.assertContains(response, self.task.title)
        self.assertContains(response, self.task.dscription)
        self.assertNotContains(response, self.task2.title)

class NewPageTest(TestCase):
    def setUp(self):
        self.form = NewTaskForm

    def test_new_page_return_correct_response(self):
        response = self.client.get('/new/')

        self.assertTemplateUsed(response, 'task/new.html')
        self.assertEqual(response.status_code, 200)

    def test_form_can_be_valid (self):
        self.assertTrue (issubclass(self.form, NewTaskForm))
        self.assertTrue ('title' in self.form.Meta.fields)
        self.assertTrue ('dscription' in self.form.Meta.fields)

        form = self.form({
            'title':"The Title",
            'dscription':"The Description"
        })

        self.assertTrue(form.is_valid())

        


    def test_new_page_form_rendering (self):
        response = self.client.get('/new/')
        self.assertContains (response, '<form')
        self.assertContains (response, 'csrfmiddlewaretoken')
        self.assertContains (response, '<label for')


        # Test invalid form
        response = self.client.post("/new/", {
        'title': '',
        'description': 'The description'
        })
        self.assertContains(response, '<ul class="errorlist">')
        self.assertContains(response, 'This field is required.')

        # Test valid form
        response = self.client.post("/new/", {
        'title': 'The Title',
        'description': 'The description'
        })
        self.assertRedirects(response,expected_url='/')
        self.assertEqual(Task.objects.count(),1)

class UpdatePageTest(TestCase):
    def setUp(self):
        self.form = UpdateTaskForm
        self.task = Task.objects.create(title = 'First Task')


    def test_update_page_returns_correct_response (self):
        response = self.client.get(f'/{self.task.id}/update/')

        self.assertTemplateUsed (response, 'task/update.html')
        self.assertEqual (response.status_code, 200)


    def test_form_can_be_valid(self):
        self.assertTrue(issubclass(self.form, UpdateTaskForm))
        self.assertTrue('title' in self.form.Meta.fields)
        # self.assertTrue ('description' in self.form.Meta.fields)
        form = self.form({
        'title': 'The title',
        'description': 'The description'
        }, instance = self.task)

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(self.task.title,'The title')

    def test_form_can_be_invalid (self):
        form = self.form({
        'title':'',
        'description': 'The description'
        }, instance=self.task)
        self.assertFalse(form.is_valid())