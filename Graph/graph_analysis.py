#!/usr/bin/python
"""
Functions for analysis of data.
"""
import xml.etree.ElementTree as ET
import matplotlib.pyplot as pp

class GraphAnalysis(object):
    """
    Class of methods to analyse the graph.
    """

    def __init__(self, filename):
        """
        Import the tree, ready for some analysis.
        """
        self._filename = filename

        # default gexf namespace
        self.ns0 = "{https://www.gexf.net/1.2draft}"

        self.graph_tree = ET.parse(self._filename)
        self.graph_root = self.graph_tree.getroot()

        self.nodes_root = self.graph_root.find(self.ns0 + "graph")\
            .find(self.ns0 + "nodes")
        self.edges_root = self.graph_root.find(self.ns0 + "graph")\
            .find(self.ns0 + "edges")

        self.journey_times = []
        self.connections_leaving = [0 for _ in range(270)]
        self.connections_arriving = [0 for _ in range(270)]
        for journey in self.edges_root:
            self.journey_times.append(float(journey.get('weight')))
            self.connections_leaving[int(journey.get('source'))] = \
                self.connections_leaving[int(journey.get('source'))] + 1
            self.connections_arriving[int(journey.get('target'))] = \
                self.connections_arriving[int(journey.get('target'))] + 1

    def journey_times_hist(self):
        """
        Draw histogram of journey times.
        Linear x scale, 10 bins.
        """
        pp.hist(self.journey_times, bins=90)
        pp.xlabel('Journey Time (minutes)')
        pp.ylabel('Number of Journeys')
        pp.show()

    def journey_times_hist_log(self):
        """
        Draw histogram of journey times.
        Log x scale - base of 1.57.
        Gives 10 bins in range 1-90 mins.
        """
        self.log_bins = [1.00, 1.57, 2.46, 3.86, 6.05, 9.49,\
                             14.88, 23.33, 36.59, 57.39, 90.00]
        pp.hist(self.journey_times, bins=self.log_bins)
        pp.xlabel('Journey Time (minutes)')
        pp.ylabel('Number of Journeys')
        pp.xscale('log', basex=1.57, nonposx = 'clip')
        pp.show()

    def journey_times_hist_smart(self):
        """
        Draw historgram of journey times.
        Use sensible and useful bin ranges.
        """
        self.smart_bins = [0.0, 5.0, 10.0, 15.0, 20.0, 30.0, 60.0, 90.0]
        pp.hist(self.journey_times, bins=self.smart_bins)
        pp.xlabel('Journey Time (minutes)')
        pp.ylabel('Number of Journeys')
        pp.show()

    def station_connectivity_hist(self):
        """
        Draw histogram of how many connnections leave and enter each station.
        """
        f, (ax1, ax2) = pp.subplots(2, 1, sharex=True)
        ax1.hist(self.connections_leaving, bins=10)
        ax1.set_title('Journeys leaving station')
        ax2.hist(self.connections_arriving, bins=10)
        ax2.set_title('Journeys arriving at station')
        pp.show()
