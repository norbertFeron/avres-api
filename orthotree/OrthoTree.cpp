/**
 *
 * This file is part of rNAV
 *
 *
 * rNAV is free software;  you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation, either version 3
 * of the License, or (at your option) any later version.
 *
 * rNAV is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with rNAV.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "OrthoTree.h"
#include <vector>
#include <tulip/SizeProperty.h>
#include <tulip/DoubleProperty.h>

PLUGIN(OrthoTree)

using namespace std;
using namespace tlp;
/*
const int NODESPACING = 5;
const int LEVELSPACING = 10;
*/
//================================================================================
static const char * paramHelp[] = {
  // layer spacing
  HTML_HELP_OPEN() \
  HTML_HELP_DEF( "type", "unsigned int" ) \
  HTML_HELP_BODY() \
  "Define the spacing between two successive layers" \
  HTML_HELP_CLOSE(),
  // node spacing
  HTML_HELP_OPEN() \
  HTML_HELP_DEF( "type", "unsigned int" ) \
  HTML_HELP_BODY() \
  "Define the spacing between two nodes" \
  HTML_HELP_CLOSE(),
};

OrthoTree::OrthoTree(const tlp::PropertyContext &context) : tlp::LayoutAlgorithm(context),nodeSpacing(4),layerSpacing(10),verticalSize(NULL){
  addInParameter<unsigned int>("Layer spacing", paramHelp[0], "10", true);
  addInParameter<unsigned int>("Node spacing", paramHelp[1], "4", true);
}

OrthoTree::~OrthoTree(){}

void OrthoTree::computeVerticalSize(node n){
  if(graph->outdeg(n) == 0){
    SizeProperty * size = graph->getProperty<SizeProperty>("viewSize");
    verticalSize->setNodeValue(n, size->getNodeValue(n)[1]);
  }
  else {
    float s = 0.;
    node u;
    forEach(u, graph->getOutNodes(n)){
      computeVerticalSize(u);
      s += verticalSize->getNodeValue(u);
    }
    if(graph->outdeg(n) > 1){
      s += nodeSpacing * (graph->outdeg(n)-1);
    }
    verticalSize->setNodeValue(n, s);
  }
}

void OrthoTree::computeLayout(node n){
  Coord cn = layoutResult->getNodeValue(n);
  float prev = 0.;
  edge e;
  forEach(e, graph->getOutEdges(n)){
    node u = graph->opposite(e,n);
    Coord c(cn);
    c[0] += layerSpacing;
    c[1] -= prev;

    prev += verticalSize->getNodeValue(u) + nodeSpacing;
    layoutResult->setNodeValue(u, c);
    
    Coord bend(cn[0], c[1], 0);
    vector<Coord> bends(1);
    bends[0] = bend;
    layoutResult->setEdgeValue(e, bends);
    computeLayout(u);
  }
}

bool OrthoTree::run(){
  layerSpacing = 10;
  nodeSpacing = 4;

  if(dataSet != 0){
    if(!dataSet->get("Layer spacing", layerSpacing))
      layerSpacing = 10;
    
    if(!dataSet->get("Node spacing", nodeSpacing))
      nodeSpacing = 4;    
  }

  verticalSize = graph->getProperty<DoubleProperty>("vertical");
  verticalSize->setAllNodeValue(0);

  node root;
  forEach(root, graph->getNodes()){
    if(graph->indeg(root) == 0)
      break;
  }
  assert(root.isValid());

  computeVerticalSize(root);

  layoutResult->setAllNodeValue(Coord(0,0,0));
  layoutResult->setAllEdgeValue(vector<Coord> (0));
  layoutResult->setNodeValue(root, Coord(0,0,0));
  computeLayout(root);

  return true;
}
