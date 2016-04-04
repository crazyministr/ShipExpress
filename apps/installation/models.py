# coding=utf-8
from django.db import models
from jsonfield import JSONField


class UrlGen(object):
    @classmethod
    def urlstr(cls):
        if hasattr(cls, '__name__'):
            s = cls.__name__.lower()
            if s.endswith('y'):
                return '%sies' % s[:-1]

            for end in ['sh', 's', 'x', 'z', 'c']:
                if s.endswith(end):
                    return '%ses' % s
            return '%ss' % s

        return cls.__class__.urlstr()


class Port(models.Model, UrlGen):
    name = models.CharField(u'Название порта', max_length=100)
    picture = models.ImageField(null=True, blank=True, upload_to='ports')

    latitude = models.FloatField(u'Широта', default=0)
    longitude = models.FloatField(u'Долгота', default=0)

    location = models.CharField(u'Местоположение', default='', max_length=100, blank=True)
    navigation = models.CharField(u'Навигация', default='', max_length=100, blank=True)
    ice_period = models.CharField(u'Ледовый период', default='', max_length=100, blank=True)
    surrounding_towns = models.CharField(u'Ближайшие населенные пункты', default='', max_length=100, blank=True)
    railway = models.CharField(u'Железная дорога', default='', max_length=100, blank=True)
    airport = models.CharField(u'Аэропорт', default='', max_length=100, blank=True)
    oil_terminals = models.CharField(u'Наличие нефтеналивных терминалов', default='', max_length=100, blank=True)

    @classmethod
    def get_coordinates(cls, name):
        obj = cls.objects.filter(name=name)
        return [obj.first().latitude, obj.first().longitude]

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return '/static/img/default.jpg'

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        app_label = 'installation'
        verbose_name = u'Порт'
        verbose_name_plural = u'Порты'


class Ship(models.Model, UrlGen):
    name = models.CharField(u'Навазние судна', max_length=100)
    picture = models.ImageField(null=True, blank=True, upload_to='ships')

    # тактико-технические характеристики
    displacement = models.FloatField(u'Водоизмещение, т.', default=0, null=True, blank=True)
    load_capacity = models.FloatField(u'Грузоподъёмность чистая, т.', default=0, null=True, blank=True)
    living_space_decks = models.FloatField(u'Полезная площадь палуб, кв. м.', default=0, null=True, blank=True)
    speed_in_ballast = models.FloatField(u'Скорость хода в балласте, узл.', default=0, null=True, blank=True)
    speed_at_full_load = models.FloatField(u'Скорость хода в полном грузу, узл.', default=0, null=True, blank=True)
    length_max = models.FloatField(u'Длина наибольшая, м.', default=0, null=True, blank=True)
    width_max = models.FloatField(u'Ширина наибольшая, м.', default=0, null=True, blank=True)
    draft_ballast = models.FloatField(u'Осадка в балласте, м.', default=0, null=True, blank=True)
    draft_at_full_load = models.FloatField(u'Осадка в полном грузу, м.', default=0, null=True, blank=True)

    # возможности
    staff = models.IntegerField(u'Личный состав, чел.', default=0, null=True, blank=True)
    cars = models.IntegerField(u'Автомобили, ед.', default=0, null=True, blank=True)
    armoured = models.IntegerField(u'Бронетранспортёры, ед.', default=0, null=True, blank=True)
    artillery = models.IntegerField(u'Артиллерия, ед.', default=0, null=True, blank=True)
    tanks = models.IntegerField(u'Танки, ед.', default=0, null=True, blank=True)
    ammunition = models.IntegerField(u'Боеприпасы, т.', default=0, null=True, blank=True)
    food = models.IntegerField(u'Продовольствие, т.', default=0, null=True, blank=True)
    clothing_equipment = models.IntegerField(u'Вещевое имущество, т.', default=0,
                                             null=True, blank=True)
    fuel_in_containers = models.IntegerField(u'Горючее в таре, т.', default=0, null=True, blank=True)

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return '/static/img/default.jpg'

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        app_label = 'installation'
        verbose_name = u'Судно'
        verbose_name_plural = u'Суда'


class Icebreaker(models.Model, UrlGen):
    name = models.CharField(u'Навазние судна', max_length=100)
    picture = models.ImageField(null=True, blank=True, upload_to='icebreakers')

    # тактико-технические характеристики
    building_place = models.CharField(u'Место постройки', max_length=100, null=True, blank=True)
    length_max = models.FloatField(u'Длина наибольшая, м.', default=0, null=True, blank=True)
    width_max = models.FloatField(u'Ширина наибольшая, м.', default=0, null=True, blank=True)
    displacement = models.FloatField(u'Водоизмещение, т.', default=0, null=True, blank=True)
    propulsion_power = models.FloatField(u'Пропульсивная мощность, МВт', default=0, null=True, blank=True)
    type_of_appy = models.CharField(u'Тип АППУ', max_length=100, null=True, blank=True)
    speed = models.FloatField(u'Скорость хода, узл.', default=0, null=True, blank=True)
    endurance = models.FloatField(u'Автономность плавания, мес.', default=0, null=True, blank=True)
    ice_passability = models.FloatField(u'Ледопроходимость, м.', default=0, null=True, blank=True)

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return '/static/img/default.jpg'

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        app_label = 'installation'
        verbose_name = u'Ледокол'
        verbose_name_plural = u'Ледоколы'


class MilitaryEquipment(models.Model, UrlGen):
    name = models.CharField(u'Наименование техники', max_length=100)
    picture = models.ImageField(null=True, blank=True, upload_to='equipment')

    weight = models.FloatField(u'Масса, т.', default=0, null=True, blank=True)
    length = models.FloatField(u'Длина, мм', default=0, null=True, blank=True)
    width = models.FloatField(u'Ширина, мм', default=0, null=True, blank=True)
    height = models.FloatField(u'Высота, мм', default=0, null=True, blank=True)
    truck_chassis = models.CharField(u'Колёсная формула', max_length=13, null=True, blank=True)
    accumulation_factor = models.CharField(u'Норма размещения пл/пв', max_length=13, null=True, blank=True)

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return '/static/img/default.jpg'

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        app_label = 'installation'
        verbose_name = u'Военная техника'
        verbose_name_plural = u'Военная техника'


class Edge(models.Model):
    from_port = models.ForeignKey(Port, related_name='from_port')
    to_port = models.ForeignKey(Port, related_name='to_port')
    dist = models.FloatField(u'Расстояние, км.', default=0)
    path = JSONField(default=[])

    @classmethod
    def get_dist(cls, from_port, to_port):
        obj = cls.objects.filter(from_port=from_port, to_port=to_port)
        if not obj:
            obj = cls.objects.filter(from_port=to_port, to_port=from_port)

        return obj.first().dist

    @classmethod
    def get_path(cls, from_port, to_port):
        obj = cls.objects.filter(from_port=from_port, to_port=to_port)
        if not obj:
            obj = cls.objects.filter(from_port=to_port, to_port=from_port)
            return obj.first().path[::-1]

        return obj.first().path

    def __unicode__(self):
        return u'%s %s to %s = %s km' % ('OK!' if self.path else '',
                                         self.from_port, self.to_port, self.dist)

    class Meta:
        app_label = 'installation'
        verbose_name = u'Расстояние'
        verbose_name_plural = u'Расстояния'
