# coding=utf-8
import json
from django.core.management import BaseCommand
from apps.installation.models import Port, Edge, Ship
from settings import INSTALLATION_DATA_DIR


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.add_ports()
        self.add_edges()
        self.add_ships()

    def add_ports(self):
        f = open(INSTALLATION_DATA_DIR + 'ports.json', 'r')
        ports = json.loads(f.read())
        f.close()

        for port in ports:
            obj, created = Port.objects.get_or_create(name=port['name'])
            if created:
                obj.latitude = port['latitude']
                obj.longitude = port['longitude']
                obj.location = port['location']
                obj.navigation = port['navigation']
                obj.ice_period = port['ice_period']
                obj.surrounding_towns = port['surrounding_towns']
                obj.railway = port['railway']
                obj.airport = port['airport']
                obj.oil_terminals = port['oil_terminals']

                obj.save()
                self.stdout.write(u'[CREATED] %s port' % port['name'])
            else:
                self.stdout.write(u'[WARNING] %s port already exists' % port['name'])

    def add_edges(self):
        f = open(INSTALLATION_DATA_DIR + 'edges.json', 'r')
        edges = json.loads(f.read())
        f.close()

        for edge in edges:
            from_port = Port.objects.filter(name=edge['from_port'])
            if not from_port:
                self.stderr.write(u'[ERROR] cannot find %s among ports' % edge['from_port'])
                continue

            to_port = Port.objects.filter(name=edge['to_port'])
            if not to_port:
                self.stderr.write(u'[ERROR] cannot find %s among ports' % edge['to_port'])
                continue

            obj, created = Edge.objects.get_or_create(from_port=from_port.first(),
                                                      to_port=to_port.first(),
                                                      dist=edge['dist'])
            if created:
                self.stdout.write(u'[CREATED] edge %s between %s & %s' % (obj.dist,
                                                                          obj.from_port.name,
                                                                          obj.to_port.name))
            else:
                self.stdout.write(u'[WARNING] edge (%s, %s) already exists' % (obj.from_port.name,
                                                                               obj.to_port.name))

    def add_ships(self):
        ships_file = open(INSTALLATION_DATA_DIR + 'ships.json', 'r')
        ships = json.loads(ships_file.read())
        ships_file.close()

        for ship in ships:
            obj, created = Ship.objects.get_or_create(
                name=ship['name'],
                speed_in_ballast=ship['speed_in_ballast'],
                speed_at_full_load=ship['speed_at_full_load'])

            if created:
                self.stdout.write(u'[CREATED] ship %s ' % obj.name)
            else:
                self.stdout.write(u'[WARNING] ship %s already exists' % obj.name)
