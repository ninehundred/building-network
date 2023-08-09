import shapely
from shapely import MultiPolygon


def plot_multipolygon(multi_polygon: MultiPolygon, plt):
    for poly in multi_polygon.geoms:
        plot_poly(poly, plt)


def plot_poly(poly, plt):
    x, y = poly.exterior.xy
    plt.plot(x, y)
    for inner in poly.interiors:
        xx, yy = inner.xy
        plt.plot(xx, yy)


def plot_any(poly, plt):
    if isinstance(poly, MultiPolygon):
        plot_multipolygon(poly, plt)
    else:
        plot_poly(poly, plt)


def import_wkt(geometries: list[str]):
    out = []
    for geometry in geometries:
        out.append(shapely.wkt.loads(geometry))
    return out
