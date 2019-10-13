from application import Application


class ObjectsApp(Application):

    def _add_arguments(self, parser):
        parser.add_argument('-g', '--global', type=int, nargs='*', dest='glob', help='global threshold value')
        parser.add_argument('-m', '--method', type=int, nargs='*', choices=[0, 1, 2, 3, 4, 5, 6],
                            help='threshold method')
        parser.add_argument('-v', '--inv', '--invert', type=int, nargs='*', choices=[0, 1], dest='invert',
                            help='invert color mode')

    def _get_default_file_fullname(self, filename): pass

    def _execute(self, paths, args): pass


if __name__ == '__main__':
    ObjectsApp().start()
