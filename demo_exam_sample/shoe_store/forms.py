from django import forms
from .models import Orders, Pickup_points, Products, Products_in_orders, Users

# ДЛЯ НАЧАЛА ИМПОРТИРУЕМ ФОРМЫ ИЗ ДЖАНГО
# ПОСЛЕ ИЗ МОДЕЛЕЙ ИМПОРТИРУЕМ САМИ МОДЕЛИ, ТОЛЬКО ТЕ КОТОРЫЕ ИМЕЮТ БОЛЬШЕ ОДНОЙ СТРОКИ (я незнаю как объяснить сами придумайте хз)

# Базовые виджеты

# - TextInput - однострочный текст
# - NumberInput - число
# - EmailInput - email с валидацией
# - URLInput - URL с валидацией
# - PasswordInput - пароль (скрывает ввод)
# - HiddenInput - скрытое поле
# - Textarea - многострочный текст

# - Выбор значений

# - Select - выпадающий список
# - SelectMultiple - множественный выбор
# - RadioSelect - радиокнопки
# - CheckboxSelectMultiple - чекбоксы
# - NullBooleanSelect - выпадающий список для BooleanField с null

# - Дата и время

# - DateInput - дата
# - DateTimeInput - дата и время
# - TimeInput - время
# - SplitDateTimeWidget - раздельный ввод даты и времени
# - SelectDateWidget - три выпадающих списка (год, месяц, день)

# - Файлы и медиа

# - FileInput - загрузка файла
# - ClearableFileInput - загрузка файла с возможностью очистки

# - Специальные

# - CheckboxInput - одиночный чекбокс
# - MultipleHiddenInput - несколько скрытых полей
# - SplitHiddenDateTimeWidget - скрытые поля для даты и времени

class OrdersForm(forms.ModelForm):

    class Meta:
        model = Orders # НАЗВАНИЕ КАК В МОДЕЛИ 
        fields = ['order_date', 'delivery_date', 'pickup_points_id', 'user_id', 'delivery_code', 'status_id'] # В ПОЛЯ МЫ ПЕРЕНОСИМ ВСЕ ПОЛЯ, ЧТО И В МОДЕЛИ
        widgets = { # НУ ВИДЖЕТЫ КАРОЧЕ ОПЯТЬ КАК В МОДЕЛЯХ НИЧЕГО НОВОГО
            'order_date': forms.DateInput(), # КАРОЧЕ ПИШЕМ ПРИМЕРНО ТАКЖЕ КАК В МОДЕЛЯХ, СВЕРХУ ЕСТЬ ВИДЖЕТЫ
            'delivery_date': forms.DateInput(),
            'pickup_points_id': forms.Select(), # ДЛЯ FK ИСПОЛЬЗУЕМ SELECT
            'user_id': forms.Select(),
            'delivery_code': forms.TextInput(),
            'status_id': forms.Select(),
        }

class Pickup_pointsForm(forms.ModelForm):

    class Meta:
        model = Pickup_points
        fields = ['index', 'city', 'street', 'building']
        widgets = {
            'index': forms.NumberInput(),
            'city': forms.TextInput(),
            'street': forms.TextInput(),
            'building': forms.NumberInput(),
        }

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ['article', 'product_name', 'unit_id', 'price', 'provider_id', 'producer_id', 'category_id', 'discount', 'amount', 'description', 'photo']
        widgets = {
            'article': forms.TextInput(),
            'product_name': forms.TextInput(),
            'unit_id': forms.Select(),
            'price': forms.NumberInput(),
            'provider_id': forms.Select(),
            'producer_id': forms.Select(),
            'category_id': forms.Select(),
            'discount': forms.NumberInput(),
            'amount': forms.NumberInput(),
            'description': forms.Textarea(),
            'photo': forms.TextInput(),
        }

class Products_in_ordersForm(forms.ModelForm):

    class Meta:
        model = Products_in_orders
        fields = ['order_id', 'product_id', 'amount']
        widgets = {
            'order_id': forms.Select(),
            'product_id': forms.Select(),
            'amount': forms.NumberInput(),
        }

class UsersForm(forms.ModelForm):
    model = Users
    fields = ['role_id', 'last_name', 'first_name', 'patronymic', 'email'. 'password']
    widgets = {
        'role_id': forms.Select(),
        'last_name': forms.TextInput(),
        'first_name': forms.TextInput(),
        'patronymic': forms.TextInput(),
        'email': forms.EmailInput(),
        'password': forms.PasswordInput(),
    }
# СОЗДАНИЕ ФОРМЫ ДЛЯ ВХОДА
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput().
        label='Email',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password',
    )