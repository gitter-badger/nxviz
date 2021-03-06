from .base import BasePlot
from .geometry import node_theta, get_cartesian
import matplotlib.patches as patches

from matplotlib.path import Path


class CircosPlot(BasePlot):
    """docstring for CircosPlot"""
    def __init__(self, nodes, edges,
                 radius, node_radius
                 nodecolor=None, edgecolor=None,
                 nodeprops=None, edgeprops=None,
                 figsize=None):
        BasePlot.__init__()
        # The following attributes are specific to CircosPlot
        self.radius = radius
        self.node_radius = node_radius
        # The rest of these attributes are inherited from BasePlot:
        # self.nodes
        # self.edges
        # self.nodeprops
        # self.edgeprops
        # self.nodecolors
        # self.edgecolors
        # self.figure
        # self.ax
        # self.node_coords
        # self.nodes_and_colors
        # self.edges_and_colors

    def compute_node_positions(self):
        """
        Uses the get_cartesian function to computes the positions of each node
        in the Circos plot.

        Returns `xs` and `ys`, lists of x- and y-coordinates.
        """
        xs =[]
        ys = []
        for node in self.nodes:
            theta = node_theta(self.nodelist, node)
            x, y = get_cartesian(self.radius, theta)
            xs.append(x)
            ys.append(y)
        self.node_coords = {'x':xs, 'y':ys}

    def draw_nodes(self):
        """
        Renders nodes to the figure.
        """
        node_r = self.node_radius
        for i, node in enumerate(self.nodes):
            x = self.node_coords[x][i]
            y = self.node_coords[y][i]
            self.nodeprops['facecolor'] = self.nodes_and_colors[i]
            node_patch = patches.Ellipse((x, y), node_r, node_r,
                                         lw=0, **self.nodeprops)
            self.ax.add_patch(node_patch)

    def draw_edges(self):
        """
        Draws edges to screen.
        """
        for start, end in self.edges:
            start_theta = node_theta(self.nodelist, start)
            end_theta = node_theta(self.nodelist, end)
            verts = [get_cartesian(self.radius, start_theta),
                     (0, 0),
                     get_cartesian(self.radius, end_theta)]
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

            path = Path(verts, codes)
            self.edgeprops['facecolor'] = 'none'
            self.edgeprops['edgecolor'] = self.edgecolor
            patch = patches.PathPatch(path, lw=1, **self.edgeprops)
            self.ax.add_patch(patch)
