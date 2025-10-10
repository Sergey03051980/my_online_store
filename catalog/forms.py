from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                   'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            return name

        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{word}"'
                )
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            return description

        description_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise ValidationError(
                    f'Описание содержит запрещенное слово: "{word}"'
                )
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price
