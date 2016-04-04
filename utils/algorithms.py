# -*- coding: utf-8 -*-
def dijkstra(graph, start, finish, n):
    """
    Algorithm dijkstra
    Find the shortest distance and way from start node to finish node
    Algorithm using priority queue for more productivity

    :param graph: adjacency matrix
    :param start: start node
    :param finish: finish node
    :param n: total node
    :return: tuple (way, best_dist), where
                way: way from start to finish except start and finish
                best_dist: the shortest distance from start to finish
    """
    from heapq import heappush, heappop

    dist = [1e9] * n
    dist[start] = 0
    prev = [-1] * n
    heap = []
    for i in xrange(n):
        heappush(heap, (dist[i], i))

    while heap:
        min_dist, u = heappop(heap)
        for v, d in enumerate(graph[u]):
            alt = d + min_dist
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heappush(heap, (alt, v))

    best_dist = dist[finish]
    way = []
    while prev[finish] != -1:
        way.append(finish)
        finish = prev[finish]

    return way[1:][::-1], best_dist
