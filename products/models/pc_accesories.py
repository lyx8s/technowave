from django.db import models
from django.core.validators import RegexValidator

from product import Product


FORM_FACTORS_MOTHERBOARD = {
        'ATX', 'ATX',
        'Micro-ATX', 'Micro-ATX',
        'Mini-ITX', 'Mini-ITX',
        'E-ATX', 'E-ATX',
        'XL-ATX', 'XL-ATX',
        'LPX', 'LPX',
        'SSI', 'SSI',
        'EBX', 'EBX',
        'EBB', 'EBB'
}

FORM_FACTORS_RAM_TYPE = {
    'DIMM': 'DIMM',
    'SO-DIMM': 'SO-DIMM',
    'RIMM': 'RIMM',
    'SRIMM': 'SRIMM',
    'Micro-DIMM': 'Micro-DIMM',
    'EDO': 'EDO',
    'FPM': 'FPM',
    'EDRAM': 'EDRAM',
    'ECC': 'ECC',
    'LLDRAM': 'LLDRAM',
    'GDRAM': 'GDRAM'
}

FORM_FACTORS_POWERUNIT = {
        "ATX": "ATX",
        "SFX": "SFX",
        "EPS": "EPS",
        "TFX": "TFX",
        "CFX": "CFX",
        "LFX": "LFX",
        "FlexATX": "FlexATX"
}


class GPU(Product):
    """
    Видеокарты
    """

    VIDEO_CARD_CONNECTORS = {
        'DisplayPort': 'DisplayPort',
        'HDMI': 'HDMI',
        'DVI': 'DVI',
        'VGA': 'VGA',
        'DisplayPort-E': 'DisplayPort-E',
        'Multiple DisplayPorts': 'Multiple DisplayPorts',
        'HDMI-E': 'HDMI-E',
        'DVI-E': 'DVI-E',
        'VGA-E': 'VGA-E'
    }
    chipset = models.CharField(
            max_length=100,
            verbose_name="Чипсет"
    )

    clock_rate = models.DecimalField(
        default=0.0,
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Частота графического процессора"
    )
    clock_rate_oc = models.DecimalField(
        default=0.0,
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Максимальная тактовая частота"
    )

    memory_size = models.PositiveIntegerField(
        default=10,
        verbose_name="Объем видеопамяти"
    )
    memory_bus = models.PositiveIntegerField(
        default=10,
        verbose_name="Шина видеопамяти"
    )

    connectors = models.CharField(
        max_length=200,
        verbose_name="Список разъемов для видеокарты"
    )
    interface = models.CharField(
        max_length=50,
        verbose_name="Интерфейс"
    )

    wattage = models.PositiveIntegerField(
        default=0,
        verbose_name="Потребляемая мощность(Вт)"
    )
    power_unit = models.PositiveIntegerField(
        default=150,
        verbose_name="Рекомендуемый блок питания(Вт)"
    )

    class Meta:
        app_label = 'products'
        db_table = "videocarts"
        verbose_name = "Видеокарта"
        verbose_name_plural = "Видеокарты"

    def __str__(self):
        return (f"{self.model_name}: "
                f"{self.manufacturer} {self.code_model} - {self.price}")

    def get_tech_details(self):
        """
        Выводит основную информацию о видеокарте
        """
        main_info = super(GPU, self).get_tech_details()
        extra_details = {
            "Чипсет": self.chipset,
        }
        return {**main_info, **extra_details}

    def get_specification_clock_rate_parameters(self):
        """
        Выводит параметры частоты
        """
        param_clock_rate_data = {
            "Частота": self.clock_rate,
            "Максимальная частота": self.clock_rate_oc
        }
        return {**param_clock_rate_data}

    def get_specifictaion_memory(self):
        """
        Выводит информацию
        о спецификации видеопамяти
        """
        spec_memory_data = {
            "Объем памяти": self.memory_size,
            "Шина видеопамяти": self.memory_bus

        }
        return {**spec_memory_data}

    def get_interface(self):
        """
        Выводит информацию об интерфейсе видеокарты
        """

        interface_data = {
            "Разъемы": self.connectors,
            "Интерфейс": self.interface
        }
        return {**interface_data}

    def get_power_consumption(self):
        """
        Выводит информацию о питание видеокарты
        """

        power_data = {
            "Потребляемая мощность": self.wattage,
            "Рекомендуемый блок питания": self.power_unit
        }
        return {**power_data}


class CPU(Product):
    """
    Процессоры
    """

    socket = models.CharField(
        max_length=100,
        verbose_name="Сокет"
    )
    watts = models.PositiveIntegerField(
        default=0,
        verbose_name="Тепловыделение"
    )

    stock_freq = models.DecimalField(
            default=0.0,
            max_digits=2,
            decimal_places=1,
            blank=True,
            null=True,
            verbose_name="Частота"
    )
    boost_freq = models.DecimalField(
            default=0.0,
            max_digits=2,
            decimal_places=1,
            blank=True,
            null=True,
            verbose_name="Максимальная частота"
    )

    cores_count = models.PositiveIntegerField(
        default=2,
        verbose_name="Кол-во ядер"
    )
    core_type = models.CharField(
        max_length=100,
        default="",
        verbose_name="Тип ядра"
    )
    threads = models.PositiveIntegerField(
        default=4,
        verbose_name="Кол-во потоков"
    )
    integrated_graphics = models.CharField(
        max_length=100,
        null=True,
        verbose_name="Встроенное графическое ядро"
    )

    class Meta:
        app_label = 'products'
        db_table = "proccesors"
        verbose_name = "Процессор"
        verbose_name_plural = "Процессоры"

    def __str__(self):
        return (f"{self.model_name}: "
                f"{self.manufacturer} {self.code_model} - {self.price}")

    def get_tech_details(self):
        """
        Возвращает основновую инфу о процессоре
        """
        main_info = super(CPU, self).get_tech_details()
        extra_detail = {
            "Сокет": self.socket,
            "Тепловыделение": self.watts
        }
        return {**main_info, **extra_detail}

    def get_specification_clock_rate_parameters(self):
        """
        Выводит параметры частоты
        """
        param_clock_rate_data = {
            "Частота": self.stock_freq,
            "Максимальная частота": self.boost_freq
        }
        return {**param_clock_rate_data}

    def get_core_parametres(self):
        """
        Возвращает параметры ядра
        """

        core_param_data = {
            "Ядро": self.core_type,
            "Кол-во ядер": self.cores_count,
            "Максимальное число потоков": self.threads,
            "Встроенное графическое ядро": self.integrated_graphics
        }
        return {**core_param_data}


class Motherboard(Product):
    """
    Материнские платы
    """

    form_factor = models.CharField(
            choices=FORM_FACTORS_MOTHERBOARD,
            default='ATX'
    )
    socket = models.CharField(
        max_length=20,
        verbose_name="Сокет"
    )
    chipset = models.CharField(max_length=40,
                               verbose_name="Чипсет")
    ram_slots = models.PositiveIntegerField(
        default=4,
        verbose_name="Кол-во слотов памяти"
    )

    ram_type = models.CharField(
        choices=FORM_FACTORS_RAM_TYPE,
        default="DIMM",
        verbose_name="Тип поддерживающей памяти"
    )

    class Meta:
        app_label = 'products'
        db_table = "motherboards"
        verbose_name = "Материнская плата"
        verbose_name_plural = "Материнские платы"

    def __str__(self):
        return (f"{self.model_name}: "
                f"{self.manufacturer} {self.code_model} - {self.price}")

    def get_tech_details(self):
        """
        Возвращает основновую инфу об материнской плате
        """
        main_info = super(Motherboard, self).get_tech_details()
        extra_detail = {
            "Форм-фактор": self.form_factor,
            "Сокет": self.socket,
            "Чипсет": self.chipset,
            "Кол-во слотов памяти": self.ram_slots
        }
        return {**main_info, **extra_detail}

    def get_extra_info(self):
        """Возвращает доп инфу об материнской плате"""
        main_info = super(Motherboard, self).get_extra_info()
        extra_info = {
            "Тип поддерживающей памяти": self.ram_type,
        }
        return {**main_info, **extra_info}


class RAM(Product):
    """
    Оперативная память
    """
    form_factor = models.CharField(
            choices=FORM_FACTORS_RAM_TYPE,
            verbose_name="Форм-фактор",
            default='DIMM'
    )
    memory_type = models.CharField(
        max_length=10,
        verbose_name="Тип памяти"
    )
    latency = models.PositiveIntegerField(
        default=16,
        verbose_name="Задержка")
    module_count = models.PositiveIntegerField(
        default=2,
        verbose_name="Кол-во модулей в комплекте"
    )
    size_module = models.CharField(max_length=60,
                                   verbose_name="Объем одного модуля")
    speed = models.CharField(max_length=30,
                             verbose_name="Тактовая частота")

    class Meta:
        app_label = 'products'
        db_table = "ram"
        verbose_name = "Оперативная память"

    def __str__(self):
        return (f"{self.model_name}: "
                f"{self.manufacturer} {self.code_model} - {self.price}")

    def get_tech_details(self):
        main_info = super(RAM, self).get_tech_details()
        extra_detail = {
            "Форм-фактор": self.form_factor,
            "Тип памяти": self.memory_type,
            "Задержка": self.latency,
            "Кол-во модулей": self.module_count,
            "Объем одного модуля": self.size_module,
            "Тактовая частота": self.speed
        }
        return {**main_info, **extra_detail}


class Storage(Product):
    """
    SSD/HDD
    """

    FORM_FACTORS_TYPE_STORAGE = {
        "HDDs": [
            {"3.5-inch": '3.5"'},
            {"2.5-inch": '2.5"'},
            {"1.8-inch": '1.8"'},
            {"1-inch": '1"'}
        ],
        "SSDs": [
            {"2.5-inch": '2.5"'},
            {"mSATA": "mSATA"},
            {"mini-SATA": "mini-SATA"},
            {"M.2": "M.2"}
        ]
    }

    TYPE_CHOICES = [
        ("HDD", "HDD"),
        ("SSD", "SSD"),
    ]

    TYPE_FIEID = models.CharField(
        choices=TYPE_CHOICES
    )

    form_factor = models.CharField(
            max_length=20,
            verbose_name="Форм-фактор"
    )
    hdd_form_factor = models.CharField(
        choices=FORM_FACTORS_TYPE_STORAGE['HDDs'],
        null=True, blank=True)
    ssd_form_factor = models.CharField(
        choices=FORM_FACTORS_TYPE_STORAGE['SSDs'],
        max_length=20, null=True, blank=True)

    capacity = models.PositiveIntegerField()

    speed = models.DecimalField(max_digits=5, decimal_places=2,
                                null=True, blank=True)

    class Meta:
        app_label = 'products'
        db_table = "storages"
        verbose_name = "HDD/SSD"
        verbose_name_plural = "HDDs/SSDs"

    def __str__(self):
        return (f"{self.model_name}: {self.TYPE_FIEID}"
                f"{self.manufacturer} {self.code_model} - {self.price}")

    def save(self, *args, **kwargs):
        if self.TYPE_FIEID == "HDD":
            self.form_factor = self.hdd_form_factor
        elif self.TYPE_FIELD == "SSD":
            self.form_factor = self.ssd_form_factor
        super().save(*args, **kwargs)

    def get_tech_details(self):
        """
        Возвращает информацию об HDD/SSD
        """

        main_info = super(Storage, self).get_tech_details()
        storage_data = {
            "Тип": self.TYPE_FIEID,
            "Форм-фактор": self.form_factor,
            "Объем накопителя": self.capacity,
            "Скорость вращения": self.speed
        }

        return {**main_info, **storage_data}


class PowerUnit(Product):
    """
    Блок питания
    """

    EFFICIENCY_LEVELS = {
        "80P": "80 PLUS",
        "80PB": "80 PLUS Bronze",
        "80PS": "80 PLUS Silver",
        "80PG": "80 PLUS Gold",
        "80PP": "80 PLUS Platinum",
        "80PT": "80 PLUS Titanium"
    }

    form_factor = models.CharField(
        choices=FORM_FACTORS_POWERUNIT,
        default='ATX'
    )
    capability = models.PositiveIntegerField()
    efficiency = models.CharField(choices=EFFICIENCY_LEVELS,
                                  verbose_name='Энергоэффективность')
    power_connect_motherboard = models.CharField(
        validators=RegexValidator(regex=r'\d+\+\d+ pin\s*x(\d+)')
    )
    power_connect_videocart = models.CharField(
        validators=RegexValidator(regex=r'\d+\+\d+ pin\s*x(\d+)')
    )
    power_connect_proccesor = models.CharField(
        validators=RegexValidator(regex=r'\d+\+\d+ pin\s*x(\d+)')
    )

    class Meta:
        app_label = 'products'
        db_table = "power_units"
        verbose_name = "Блок питания"
        verbose_name_plural = "Блоки питания"

    def __str__(self):
        return (f"{self.model_name}: "
                f"{self.manufacturer} {self.code_model} - {self.price}")

    def get_tech_details(self):
        """
        Возвращает информацию о блоке питания
        """
        main_info = super(PowerUnit, self).get_tech_details()

        power_data = {
            "Форм-фактор": self.form_factor,
            "Мощность": self.capability,
            "Сертификация": self.efficiency,
            "Питание для материской платы": self.power_connect_motherboard,
            "Питание для видеокарты": self.power_connect_videocart,
            "Питание для процессора": self.power_connect_proccesor
        }

        return {**main_info, **power_data}


class Case(Product):
    """
    Корпус
    """

    FORM_FACTORS_CASE = {
        "Mini Tower": "Mini Tower",
        "Micro ATX Tower": "Micro ATX Tower",
        "Regular ATX Tower": "Regular ATX Tower",
        "Full Tower": "Full Tower",
        "Super Tower": "Super Tower",
        "Mini PC": "Mini PC"
    }

    form_factor = models.CharField(
        choices=FORM_FACTORS_CASE
    )
    motherboard_form_factor = models.CharField(
        choices=FORM_FACTORS_MOTHERBOARD,
        verbose_name="Форм-фактор для материской платы"
    )
    power_unit_form_factor = models.CharField(
        choices=FORM_FACTORS_POWERUNIT,
        verbose_name="Форм-фактор для блока питания"
    )
    two_five_inch_bays = models.PositiveIntegerField(
        default=1,
        verbose_name='Кол-во отсеков 2.5"')
    three_five_inch_bays = models.PositiveIntegerField(
        default=1,
        verbose_name='Кол-во отсеков 3.5"')

    class Meta:
        app_label = 'products'
        db_table = "cases"
        verbose_name = "Корпус"
        verbose_name_plural = "Корпуса"

    def __str__(self):
        return (f"{self.model_name}: "
                f"{self.manufacturer} {self.code_model} - {self.price}")

    def get_tech_details(self):
        """
        Возвращает информацию о корпусе
        """
        main_info = super(Case, self).get_tech_details()

        power_data = {
            "Форм-фактор": self.form_factor,
            "Форм-фактор для материской платы": self.motherboard_form_factor,
            "Форм-фактор для блока питания": self.power_unit_form_factor,
            'Кол-во отсеков 2.5"': self.two_five_inch_bays,
            'Кол-во отсеков 3.5"': self.three_five_inch_bays
        }

        return {**main_info, **power_data}
