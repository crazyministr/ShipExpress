# coding=utf-8
from django.http import JsonResponse
from django.template import RequestContext
from django.views.generic import View, TemplateView
from django.shortcuts import render_to_response
from apps.installation.models import Edge, Port, Ship
from apps.calculation.forms import CirculationDataForm
from utils import matrix
from utils.algorithms import dijkstra


class CalculationPageView(TemplateView):
    template_name = None
    form_class = CirculationDataForm

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name,
                                  {'form': self.form_class()},
                                  context_instance=RequestContext(request))


class YMapsPageView(CalculationPageView):
    template_name = 'calculation/yandex.html'


class GooglePageView(CalculationPageView):
    template_name = 'calculation/google.html'


ymaps_calculation_page_view = YMapsPageView.as_view()
google_calculation_page_view = GooglePageView.as_view()


class CalculationView(View):
    MAX_INT = 2 ** 31

    def __init__(self, **kwargs):
        super(CalculationView, self).__init__(**kwargs)
        self.start = None  # start node
        self.finish = None  # finish node
        self.medium = []  # intermediate nodes
        self.ship = None  # ship
        self._name_to_int = {}  # convert names to numbers
        self._int_to_name = {}  # convert numbers to names

        # self.graph[x][y] = dist, from %x% to %y% distance %dist%
        self.graph = None
        # self.add_graph[x][y] = [waterfront[, waterfront]]
        # contain list of waterfronts - way from %x% to %y%
        # which didn't find in the model Distance
        self.add_graph = None
        # %f[mask][node]% it's the minimum distance from %start%
        # if already visited nodes from %mask% and stopped in %node%
        self.f = None

    def compress_data(self, data):
        for i, name in enumerate(data):
            self._name_to_int[name] = i
            self._int_to_name[i] = name

    def name_to_int(self, name):
        return self._name_to_int.get(name)

    def int_to_name(self, num):
        return self._int_to_name.get(num)

    def post(self, request, *args, **kwargs):
        context = {}
        ports = [port.name for port in Port.objects.all()]
        self.start = request.POST['start']
        self.finish = request.POST['finish']
        self.medium = request.POST.getlist('medium', [])
        self.medium.extend([self.start, self.finish])
        self.ship = request.POST.get('ships')

        context['start'] = self.start
        context['finish'] = self.finish
        count_ports = len(ports)

        self.compress_data(ports)
        self.graph = matrix(count_ports, count_ports, self.MAX_INT)
        self.add_graph = matrix(count_ports, count_ports)
        self.f = matrix(2 ** count_ports, count_ports)

        edges = Edge.objects.all()
        for edge in edges:
            x = self.name_to_int(edge.from_port.name)
            y = self.name_to_int(edge.to_port.name)

            self.graph[x][y] = self.graph[y][x] = edge.dist
            self.add_graph[x][y] = self.add_graph[y][x] = {'dist': edge.dist, 'way': []}

        for x in range(count_ports):
            for y in range(count_ports):
                if x == y:
                    continue

                way, best_dist = dijkstra(self.graph, x, y, count_ports)
                self.add_graph[x][y] = {'dist': best_dist, 'way': way[::-1]}
                self.add_graph[y][x] = {'dist': best_dist, 'way': way}

        for x in range(count_ports):
            for y in range(count_ports):
                if x != y and self.add_graph[x][y]['way']:
                    self.graph[x][y] = self.add_graph[x][y]['dist']
                    self.graph[y][x] = self.add_graph[y][x]['dist']

        import time

        start_time = time.time()
        self.dfs(mask=2 ** self.name_to_int(self.start),
                 node=self.name_to_int(self.start),
                 dist=0)
        context['time_of_execution'] = round(time.time() - start_time, 3)

        finish = self.name_to_int(self.finish)
        mask, context['total_dist'] = self.get_min_dist(count_ports, finish)

        if mask == 0:
            return JsonResponse({'status': 'error', 'msg': u'Невозможно построить заданный путь'})

        context['way'] = self.recovery_way(mask, finish)
        if self.ship:
            context['ship_speed'] = self.get_ship_speed(self.ship)
            context['img_name'] = self.get_img_name()
        print self.get_img_name()

        return JsonResponse({'status': 'ok',
                             'data': context})

    def get_img_name(self):
        return str(Port.objects.get(name=self.start).id) + '_' + \
               str(Port.objects.get(name=self.finish).id) + '.png'

    def recovery_way(self, mask, finish):
        way = []
        while finish != -1:
            if way:
                y = self.name_to_int(way[-1]['name'])
                for v in self.add_graph[finish][y]['way']:
                    way.append({'name': self.int_to_name(v),
                                'required': True if self.int_to_name(v) in self.medium else False,
                                'coords': Port.get_coordinates(self.int_to_name(v))})

            way.append({'name': self.int_to_name(finish),
                        'required': True if self.int_to_name(finish) in self.medium else False,
                        'coords': Port.get_coordinates(self.int_to_name(finish))})
            if finish == 0:
                break

            temp_finish = finish
            finish = self.f[mask][finish]['node']
            mask ^= 2 ** temp_finish  # erase byte from temp_finish position

        way = way[::-1]  # reverse
        for i in range(len(way)):
            from_port = Port.objects.filter(name=way[i]['name']).first()
            if i + 1 < len(way):
                to_port = Port.objects.filter(name=way[i + 1]['name']).first()
                way[i]['dist'] = Edge.get_dist(from_port, to_port)
                way[i]['path'] = Edge.get_path(from_port, to_port)

            way[i]['id'] = from_port.id
        return way

    def dfs(self, mask, node, dist, prev_node=-1):
        if isinstance(self.f[mask][node], dict) and self.f[mask][node]['dist'] <= dist:
            return

        self.f[mask][node] = {'node': prev_node,
                              'dist': dist}

        for next_node, next_dist in enumerate(self.graph[node]):
            if next_dist == self.MAX_INT or mask & (2 ** next_node):
                continue

            self.dfs(mask=mask | (2 ** next_node),
                     node=next_node,
                     dist=dist + next_dist,
                     prev_node=node)

    def get_min_dist(self, count_ports, finish):
        min_dist = 1e9
        min_mask = 0

        for i in range(2 ** count_ports):
            if (all([i & (2 ** self.name_to_int(node)) for node in self.medium]) and
                    isinstance(self.f[i][finish], dict) and
                    self.f[i][finish]['dist'] < min_dist):
                min_dist = self.f[i][finish]['dist']
                min_mask = i

        return min_mask, min_dist

    def get_ship_speed(self, ship):
        obj = Ship.objects.filter(name=ship)
        if not obj:
            raise Exception(u'Didnt find ship with name %s' % ship)

        return {'speed_in_ballast': obj.first().speed_in_ballast,
                'speed_at_full_load': obj.first().speed_at_full_load}


calculation_view = CalculationView.as_view()
