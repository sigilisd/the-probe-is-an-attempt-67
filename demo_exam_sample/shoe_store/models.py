from django.db import models

# ПОСЛЕ ПОДКЛЮЧЕНИЯ БАЗЫ ДАННЫХ МЫ СОЗДАЕМ МОДЕЛИ ПО ТАБЛИЦА ИЗ НАШЕЙ БД ЭТО ШАГ ДВА!!!

# Шпаргалка по типам полей Django:
# - CharField: строка ограниченной длины (max_length). Для имён/названий/коротких текстов.
# - EmailField: строка с валидацией формата email.
# - ForeignKey: связь "многие-к-одному" (ссылка на запись другой модели/таблицы).
#   on_delete задаёт поведение при удалении связанной записи (например CASCADE — удалить зависимые).
# - DateTimeField: дата и время. auto_now_add=True — проставить при создании; auto_now=True — обновлять при каждом сохранении.
# - BooleanField: логическое True/False (часто с default=...).
# - PositiveIntegerField: целое число >= 0 (удобно для количества/счётчиков).

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        managed = False # ЭТА СТРОКА ЗАПРЕЩАЕТ ДЖАНГО МЕНЯТЬ ТАБЛИЦУ В НАШЕЙ БД
        db_table = 'category' # НАЗВАНИЕ ТАБЛИЦЫ В БД

    def __str__(self) -> str:
        return self.category_name # ЭТА СТРОКА ПОЗВОЛЯЕТ НАМ ВЫВЕСТИ СТРОКУ С НАЗВАНИЕМ КАТЕГОРИИ И Т.Д.

class Order_statuses(models.Model):
    order_statuses_name = models.CharField(max_length=255)

    class Meta:
        managed = False 
        db_table = 'order_statuses'

    def __str__(self) -> str:
        return self.order_statuses_name

class Orders(models.Model):
    order_date = models.DateField()
    delivery_date = models.DateField()
    pickup_points_id = models.ForeignKey('Pickup_points', on_delete=models.CASCADE, related_name='Orders', db_column='pickup_point_id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='Orders', db_column='user_id')
    delivery_code = models.CharField(max_length=255)
    status_id = models.ForeignKey('Order_statuses', on_delete=models.CASCADE, related_name='Orders', db_column='status_id')

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self) -> str:
        return f"{self.order_date}, {self.delivery_date}, {self.delivery_code}"
        
class Pickup_points(models.Model):
    index = models.PositiveIntegerField()
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'pickup_points'

    def __str__(self) -> str:
        return f"{self.index}, {self.city}, {self.street}, {self.building}"

class Producers(models.Model):
    producer_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'producers'

    def _str__(self) -> str:
        return self.producer_name

class Products(models.Model):
    article = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    unit_id = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='Products', db_column='unit_id')
    price = models.PositiveIntegerField()
    provider_id = models.ForeignKey('Provider', on_delete=models.CASCADE, related_name='Products', db_column='provider_id')
    producer_id = models.ForeignKey('Producer', on_delete=models.CASCADE, related_name='Products', db_column='producer_id')
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='Products', db_column='category_id')
    discount = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    description = models.TextField()
    photo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'products'

    def _str__(self) -> str:
        return f"{self.article}, {self.product_name}, {self.price}, {self.discount}, {self.amount}, {self.description}, {self.photo}"

class Products_in_orders(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='Products_in_orders', db_column='order_id')
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='Products_in_orders', db_column='product_id')
    amount = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'products_in_orders'

    def _str__(self) -> str:
        return self.amount

class Providers(models.Model):
    provider_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'providers'

    def _str__(self) -> str:
        return self.provider_name

class Roles(models.Model):
    role_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'roles'

    def _str__(self) -> str:
        return self.role_name

class Units(models.Model):
    unit_name = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'units'

    def _str__(self) -> str:
        return self.unit_name

class Users(models.Model):
    role_id = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='Users', db_column='role_id')
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'

    def _str__(self) -> str:
        return f"{self.last_name}, {self.first_name}, {self.patronymic}"