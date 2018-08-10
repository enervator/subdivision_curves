from bokeh.events import Tap, ButtonClick, PanStart, PanEnd
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select
from bokeh.models.widgets import Button
from bokeh.plotting import figure

from curves.bspline import bspline_curve
from curves.catmull_rom import catmull_rom_curve
from curves.four_point_subdivision import four_point_subdivision
from curves.lagrange import lagrange_curve
from curves.hermite import hermite_curve, hermite_spline_curve

from convex_hull import convex_hull


def get_key(method):
    if method == 'B-Spline':
        return method
    elif method == 'Hermite Interpolation' or method == 'Hermite Spline':
        return 'Hermite'
    elif method == 'Lagrange Interpolation':
        return 'Lagrange'
    elif method == 'Catmull-Rom Spline':
        return 'Catmull-Rom'
    elif method == 'Four Point Subdivision':
        return 'Four-Point'
    raise Exception('Invalid Method Option')


def get_data(method):
    method_data = data[get_key(method)]
    point_data = method_data['data']
    results = []
    control_x = []
    control_y = []
    x = []
    y = []
    drag_x = []
    drag_y = []
    hull_x = []
    hull_y = []
    if point_data:
        if method == 'B-Spline':
            degree = 3
            control_x, control_y = zip(*point_data)
            if len(point_data) > degree:
                results = bspline_curve(degree, point_data)
        elif method == 'Hermite Interpolation':
            control_x, control_y = zip(*map(lambda x: x[0], method_data['data']))
            drag_x = list(map(lambda x: x[0], method_data['drag']))
            drag_y = list(map(lambda x: x[1], method_data['drag']))
            if len(method_data['data']) > 1:
                results = hermite_curve(point_data)
        elif method == 'Hermite Spline':
            control_x, control_y = zip(*map(lambda x: x[0], point_data))
            drag_x = list(map(lambda x: x[0], method_data['drag']))
            drag_y = list(map(lambda x: x[1], method_data['drag']))
            if len(point_data) > 1:
                results = hermite_spline_curve(point_data)
        elif method == 'Lagrange Interpolation':
            control_x, control_y = zip(*point_data)
            if len(point_data) > 1:
                results = lagrange_curve(point_data)
        elif method == 'Catmull-Rom Spline':
            control_x, control_y = zip(*point_data)
            if len(point_data) > 3:
                results = catmull_rom_curve(point_data)
        elif method == 'Four Point Subdivision':
            control_x, control_y = zip(*point_data)
            if len(point_data) > 3:
                results = four_point_subdivision(point_data)
        if len(results) > 0:
            x, y = zip(*results)
        if show_convex_hull and len(point_data) > 2:
            hull_values = convex_hull(point_data)
            hull_x, hull_y = zip(*hull_values)
    return ColumnDataSource({'x': x, 'y': y}), ColumnDataSource({'x': control_x, 'y': control_y}), ColumnDataSource({'x': drag_x, 'y': drag_y}), ColumnDataSource({'x': hull_x, 'y': hull_y})

def make_plot(curve, control, drag, title):
    plot = figure(plot_width=800, plot_height=600, toolbar_location=None, x_range=(0, 10), y_range=(0, 10))
    plot.title.text = title
    plot.toolbar.active_drag = None
    plot.line('x', 'y', source=curve, color='dodgerblue')
    plot.circle('x', 'y', source=control)
    plot.multi_line('x', 'y', source=drag, color='firebrick')
    plot.line('x', 'y', source=hull, color='purple')
    plot.on_event(Tap, mouse_press)
    plot.on_event(PanStart, mouse_drag_start)
    plot.on_event(PanEnd, mouse_drag_end)
    return plot


def update_plot(attr, old, new):
    global method
    method = new
    plot.title.text = method
    new_plot_data, new_control, new_drag, new_hull = get_data(method)
    curve.data.update(new_plot_data.data)
    control.data.update(new_control.data)
    drag.data.update(new_drag.data)
    hull.data.update(new_hull.data)


def mouse_press(event):
    key = get_key(method)
    if key == 'B-Spline' or key == 'Lagrange' or key == 'Catmull-Rom' or key == 'Four-Point':
        data[key]['data'].append([event.x, event.y])
        update_plot(None, method, method)


def mouse_drag_start(event):
    global drag_event
    drag_event = (event.x, event.y)


def mouse_drag_end(event):
    global drag_event
    if get_key(method) == 'Hermite' and drag_event != None:
        point = drag_event
        vector = [event.x - drag_event[0], event.y - drag_event[1]]
        data['Hermite']['data'].append([point, vector])
        data['Hermite']['drag'].append([[drag_event[0], event.x], [drag_event[1], event.y]])
        update_plot(None, method, method)
    drag_event = None


def clear(event):
    key = get_key(method)
    if key == 'Hermite':
        data[key]['data'] = []
        data[key]['drag'] = []
    else:
        data[key]['data'] = []
    update_plot(None, method, method)


def toggle_convex_hull(event):
    global show_convex_hull
    show_convex_hull = not show_convex_hull
    update_plot(None, method, method)


# Set up Initial Data
method = 'B-Spline'

data = {
    'B-Spline': {'data': []},
    'Hermite': {
        'drag': [],
        'data': []
    },
    'Lagrange': {'data': []},
    'Catmull-Rom': {'data': []},
    'Four-Point': {'data': []},
}

show_convex_hull = False
curve, control, drag, hull = get_data(method)
plot = make_plot(curve, control, drag, method)

# Holder variable for Drag Eventz
drag_event = None

# Add Method Selection Dropdown and Handler
options = ['B-Spline', 'Hermite Interpolation', 'Hermite Spline', 'Lagrange Interpolation', 'Catmull-Rom Spline', 'Four Point Subdivision']
method_select = Select(value=method, title='Subdivision Method', options=options)
method_select.on_change('value', update_plot)

# Add Clear Button
clear_button = Button(label='Clear')
clear_button.on_event(ButtonClick, clear)

convex_hull_button = Button(label='Convex Hull')
convex_hull_button.on_event(ButtonClick, toggle_convex_hull)

curdoc().add_root(row(plot, column(method_select, clear_button, convex_hull_button)))
curdoc().title = 'Subdivision Methods Toolbox'
