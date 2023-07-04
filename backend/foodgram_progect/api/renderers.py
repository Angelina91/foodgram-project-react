from rest_framework import renderers


class ShoppingcartRenderer(renderers.BaseRenderer):
    """ Рендер данных для подготовки списка покупок """

    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
