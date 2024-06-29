from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify

from blog.models import Post


class PostListView(ListView):
    """
    Контроллер списка статей.
    """

    model = Post

    def get_queryset(self):
        """
        В зависимости от прав доступа пользователя возвращает все или только опубликованные статьи.
        :return: queryset статей
        """
        if self.request.user.has_perm("blog.add_post") and self.request.user.has_perm(
            "blog.change_post"
        ):
            return super().get_queryset().order_by("-created_at")
        return super().get_queryset().filter(is_published=True).order_by("-created_at")


class PostDetailView(DetailView):
    """
    Контроллер детального просмотра статьи.
    """

    model = Post

    def get_object(self, queryset=None):
        """
        Прибавляет к счетчику просмотров 1.
        Если счетчик просмотров достиг 100, отправляет письмо на электронную почту.
        :return: объект статьи
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        if self.object.views_count == 100:
            send_mail(
                subject="Поздравляем!",
                message=f'Количество просмотров поста "{self.object.title}" достигло 100',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["putilovskayaa@gmail.com", "putilovskayaa@mail.ru"],
            )
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    """
    Контроллер создания новой статьи.
    """

    model = Post
    fields = "__all__"
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        """
        Привязывает к новой статье slug.
        """
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """
    Контроллер редактирования статьи.
    """

    model = Post
    fields = "__all__"

    def form_valid(self, form):
        """
        Привязывает к редактируемой статье slug.
        """
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает URL страницы списка статей после успешного редактирования.
        """
        return reverse("blog:view", args=[self.kwargs.get("slug")])


class PostDeleteView(DeleteView):
    """
    Контроллер удаления статьи.
    """

    model = Post
    success_url = reverse_lazy("blog:post_list")
