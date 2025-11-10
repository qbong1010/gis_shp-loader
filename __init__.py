# -*- coding: utf-8 -*-
"""
GIS SHP Loader
QGIS Plugin for batch loading shapefiles from multiple folders
"""

__version__ = "0.1.0"
__version_info__ = (0, 1, 0)


def classFactory(iface):
    """QGIS 플러그인 인스턴스를 생성하고 반환합니다.
    
    Args:
        iface: QGIS 인터페이스 객체
        
    Returns:
        GisShpLoader: 플러그인 객체
    """
    from .gis_shp_loader import GisShpLoader
    return GisShpLoader(iface) 