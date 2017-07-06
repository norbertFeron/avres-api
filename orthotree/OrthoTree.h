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
#ifndef   	ORTHOTREE_H_
#define   	ORTHOTREE_H_

#include <tulip/LayoutAlgorithm.h>

class OrthoTree : public tlp::LayoutAlgorithm {
 private :
  unsigned int nodeSpacing;
  unsigned int layerSpacing;
  tlp::DoubleProperty *verticalSize;
 public:

PLUGININFORMATION("OrthoTree","Romain Bourqui","20/02/2012","Orthogonal Tree","1.0","Tree")

  OrthoTree(const tlp::PluginContext* context);
  ~OrthoTree();

  bool run();

  void computeVerticalSize(tlp::node n);
  void computeLayout(tlp::node n);
  
};

#endif

