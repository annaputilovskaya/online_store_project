from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from catalog.models import Product, ProductVersion

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class StyleFormMixin:
    """
    Миксин для стилизации форм.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    """
    Форма создания/редактирования продукта.
    """

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at", "owner")

    def clean_name(self):
        """
        Проверяет на наличие запрещенных слов
        в названии продукта.
        """
        name = self.cleaned_data["name"]
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError("Запрещенное название продукта")
        return name

    def clean_description(self):
        """
        Проверяет на наличие запрещенных слов
        в описании продукта.
        """
        description = self.cleaned_data["description"]
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError("Запрещенное описание продукта")
        return description


class ProductVersionForm(StyleFormMixin, ModelForm):
    """
    Форма создания версии продукта.
    """

    class Meta:
        model = ProductVersion
        fields = "__all__"


class ProductModeratorForm(StyleFormMixin, ModelForm):
    """
    Форма редактирования продукта для модератора.
    """

    class Meta:
        model = Product
        fields = ["description", "category", "is_published"]

    def clean_description(self):
        """
        Проверяет на наличие запрещенных слов
        в описании продукта.
        """
        description = self.cleaned_data["description"]
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError("Запрещенное описание продукта")
        return description
