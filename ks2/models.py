from django.db import models


class KS2Form(models.Model):
    """Модель для хранения данных формы КС-2"""
    
    # Данные инвестора
    investor = models.CharField(max_length=255, verbose_name="Инвестор", default="")
    okpo_investor = models.CharField(max_length=20, verbose_name="ОКПО инвестора", blank=True)
    
    # Данные заказчика
    customer = models.CharField(max_length=255, verbose_name="Заказчик", default="АО «МОЭнергоСервис»")
    okpo_customer = models.CharField(max_length=20, verbose_name="ОКПО заказчика", blank=True)
    
    # Данные подрядчика
    contractor = models.CharField(max_length=255, verbose_name="Подрядчик", default="")
    okpo_contractor = models.CharField(max_length=20, verbose_name="ОКПО подрядчика", blank=True)
    
    # Данные о строительстве
    construction = models.CharField(max_length=255, verbose_name="Наименование строительства", default="")
    object_name = models.CharField(max_length=255, verbose_name="Объект", default="")
    okdp = models.CharField(max_length=20, verbose_name="ОКДП", blank=True)
    
    # Данные договора
    document_number = models.CharField(max_length=50, verbose_name="Номер документа", default="")
    contract_number = models.CharField(max_length=50, verbose_name="Номер договора", default="N4")
    contract_date = models.DateField(verbose_name="Дата договора", null=True, blank=True)
    day_contract = models.CharField(max_length=2, verbose_name="День заключения договора", default="04")
    month_contract = models.CharField(max_length=2, verbose_name="Месяц заключения договора", default="09")
    year_contract = models.CharField(max_length=4, verbose_name="Год заключения договора", default="2024")
    
    # Отчетный период
    report_from = models.DateField(verbose_name="Отчет с", null=True, blank=True)
    report_to = models.DateField(verbose_name="Отчет по", null=True, blank=True)
    
    # Смета
    smeta = models.CharField(max_length=100, verbose_name="Стоимость по смете", default="")
    
    # Подписи сдающей стороны
    surrender_position = models.CharField(max_length=255, verbose_name="Должность сдающего", default="")
    surrender_signature = models.CharField(max_length=255, verbose_name="ФИО сдающего", default="")
    
    # Подписи принимающей стороны
    accept_position = models.CharField(max_length=255, verbose_name="Должность принимающего", default="")
    accept_signature = models.CharField(max_length=255, verbose_name="ФИО принимающего", default="")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Форма КС-2"
        verbose_name_plural = "Формы КС-2"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"КС-2 №{self.document_number} от {self.created_at.strftime('%d.%m.%Y')}"


class WorkItem(models.Model):
    """Модель для хранения позиций работ в КС-2"""
    
    ks2_form = models.ForeignKey(KS2Form, on_delete=models.CASCADE, related_name='works', verbose_name="Форма КС-2")
    
    position = models.CharField(max_length=50, verbose_name="№ позиции", default="")
    name = models.CharField(max_length=500, verbose_name="Наименование работы", default="")
    number_pricelist = models.CharField(max_length=50, verbose_name="№ прейскуранта", default="-")
    unit_of_measurement = models.CharField(max_length=50, verbose_name="Ед. измерения", default="")
    quantity = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="Количество", default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Цена за ед.", default=0)
    
    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.position} - {self.name}"
    
    @property
    def total(self):
        """Вычисляет общую стоимость позиции"""
        return self.quantity * self.price


# Модели для КС-3 (заготовка на будущее)
class KS3Form(models.Model):
    """Модель для хранения данных формы КС-3 (справка о стоимости)"""
    
    ks2_form = models.OneToOneField(KS2Form, on_delete=models.CASCADE, related_name='ks3_data', null=True, blank=True, verbose_name="Связанная форма КС-2")
    
    # Здесь будут поля для КС-3, когда вы добавите шаблон
    # Пока оставляем пустым или добавляем базовые поля
    
    notes = models.TextField(verbose_name="Примечания", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Форма КС-3"
        verbose_name_plural = "Формы КС-3"
    
    def __str__(self):
        return f"КС-3 для {self.ks2_form}" if self.ks2_form else "КС-3 (без связи)"

