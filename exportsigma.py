from tulip import *
import tulipplugins

class ExportSigma(tlp.ExportModule):
	def __init__(self, context):
		tlp.ExportModule.__init__(self, context)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)
	
	def fileExtension(self):
		return "json"
		
	def exportGraph(self, os):
			
		# edges
		os << '{ "edges": ['
		for edge in self.graph.getEdges():
			if edge.id == 0:
				os << '{ '
			else:
				os << ',{ '
			# edge properties
			os << '"source":"%s", ' % self.graph.source(edge).id
			os << '"target":"%s", ' % self.graph.target(edge).id
			# todo edge prop
			# sigma id
			os << '"id":"%s"' % edge.id
			os << ' }'
		os << '], '
		
		# nodes
		os << '"nodes": ['
		for node in self.graph.getNodes():
			if node.id == 0:
				os << '{ '
			else:
				os << ',{ '
			for prop in self.graph.getObjectProperties():
				# node color
				if prop.getName() == "viewColor":
					colors = prop.getNodeStringValue(node)[1:].split(',')
					os << '"color":"rgb(%s,%s,%s)", ' % (colors[0], colors[1], colors[2])
				# node label
				elif prop.getName() == "viewLabel":
					if prop.getNodeStringValue(node):
						label =  prop.getNodeStringValue(node).replace('"', '\\\"')
						os << '"label":"%s", ' % label
					else:
						os << '"label":"node%s", ' % node.id
				# node size
				elif prop.getName() == "viewSize":
					size = prop.getNodeStringValue(node)[1:-1].split(',')
					size = (int(size[0]) + int(size[1])) / 2
					os << '"size":%s, ' % size
				# node layout
				elif prop.getName() == "viewLayout":
					coord = prop.getNodeStringValue(node)[1:-1].split(',')
					os << '"x":%s, ' % coord[0]
					os << '"y":%s, ' % (float(coord[1]) * (-1))
				# other
				elif prop.getNodeDefaultStringValue() != prop.getNodeStringValue(node) and prop.getNodeStringValue(node):
					value = prop.getNodeStringValue(node).replace('"', '\\\"')
					os << '"%s":"%s", ' % (prop.getName(), value)
				# sigma id
			os << '"id":"%s"' % node.id
			os << ' }'
		os << ']} '
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("ExportSigma", "SIGMA JSON Export", "Norbert Feron", "01/06/2016", "Export to sigma.js JSON format", "1.0")
