from django.test import runner


class Channel2TestRunner(runner.DiscoverRunner):

    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        parser.set_defaults(pattern='*_test.py')
