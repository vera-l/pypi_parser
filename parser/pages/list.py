from . import Page


class List(Page):

    def get_list_items(self):
        items = self.selector.css('.package-snippet')
        return [
            self.PYPI_URL_TEMPLATE.format(item.xpath('@href').get()) for item in items
        ]

    def get_next_page_url(self):
        url = self.selector.css('.button-group--pagination').xpath('a[last()]/@href').get()
        return self.PYPI_URL_TEMPLATE.format(url) if url else None
