from . import Page


class Item(Page):

    def get_item_data(self):
        package_name = self.selector.css('.package-header__name::text').get().strip().split(' ')[0]
        author = self.selector.css('.sidebar-section').xpath('p[strong/text()="Author:"]/a/text()').get()
        maintainers = [
            item.strip() for item in self.selector.css('.sidebar-section__user-gravatar-text::text').getall()
        ]
        last_deploy = self.selector.css('.package-header__date').xpath('time/@datetime').get()

        result = {
            'package': package_name,
            'author': author,
            'last_deploy': last_deploy,
            'maintainers': maintainers,
        }

        homepage = self.selector.xpath('//i[@class="fas fa-home"]/parent::a/@href').get()
        if homepage and homepage.startswith('https://github.com'):
            result['git_repo'] = homepage
            git_stars = self.selector.xpath('//span[@data-key="stargazers_count"]/text()').get()
            if git_stars:
                result['stars'] = self.get_git_stars_int(git_stars)

        return result

    @staticmethod
    def get_git_starts_int(git_stars):
        if git_stars:
            git_stars = git_stars.replace(',', '')
            try:
                return int(git_stars)
            except ValueError:
                return None
        return None
