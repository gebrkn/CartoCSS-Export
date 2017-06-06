from qgis.core import *
import layer
import debug
import error


def layers(prj):
    for la in groups(prj.layerTreeRoot()):
        yield la


def groups(group):
    for tl in group.children():
        if not tl.isVisible():
            continue
        if isinstance(tl, QgsLayerTreeGroup):
            for la in groups(tl):
                yield la
        else:
            yield tl.layer()


def global_metadata(cc, prj):
    return {
        "format": "png24",
        "interactivity": False,
        "minzoom": 0,
        "maxzoom": 22,
        "scale": 1,
        "metatile": 2,
        "name": "test",
        "description": ""
    }


def metadata(cc, prj):
    lp = [layer.metadata(cc, la) for la in layers(prj)]
    lp = [x for x in lp if x]

    if not lp:
        cc.error(error.EMPTY_PROJECT)

    d = {
        'Stylesheet': ['style.mss'],
        'Layer': lp
    }

    d.update(global_metadata(cc, prj))
    return d


def exportQgsProject(cc, prj):
    return [cc.export(la) for la in layers(prj)]