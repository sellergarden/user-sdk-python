class Component:
    """
    Base class for any injectable. Any service or dependency
    that needs to be injected into the function should extend this class.
    """

    pass


class Label(Component):
    def __init__(self, text, css_class=""):
        self.text = text
        self.css_class = css_class

    def render(self):
        return f'<label class="{self.css_class}">{self.text}</label>'


class SelectBox(Component):
    def __init__(self, options, css_class=""):
        self.options = options
        self.css_class = css_class

    def render(self):
        options_html = "".join(
            [f'<option value="{opt}">{opt}</option>' for opt in self.options]
        )
        return f'<select class="form-select {self.css_class}">{options_html}</select>'


class SubmitButton(Component):
    def __init__(self, text, css_class="btn btn-primary"):
        self.text = text
        self.css_class = css_class

    def render(self):
        return f'<button type="submit" class="{self.css_class}">{self.text}</button>'


class TimePicker(Component):
    def __init__(self, time="", css_class=""):
        self.time = time
        self.css_class = css_class

    def render(self):
        return f'<input type="time" class="form-control {self.css_class}" value="{self.time}">'


class Form(Component):
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def render(self):
        rendered_components = "".join(
            [component.render() for component in self.components]
        )
        return f'<form class="form-group">{rendered_components}</form>'


class WidgetComponent(Component):
    def __init__(self):
        self.components = []

    def add(self, component: Component):
        self.components.append(component)

    def render(self):
        rendered_components = "".join(
            [component.render() for component in self.components]
        )
        return f'<div class="widget">{rendered_components}</div>'
