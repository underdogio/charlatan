from charlatan.utils import copy_docstring_from
from charlatan import FixturesManager
from charlatan.fixtures_manager import make_list


class FixturesManagerMixin(object):

    """Class from which test cases should inherit to use fixtures.

    .. versionchanged:: 0.3.0
        ``use_fixtures_manager`` method renamed ``init_fixtures.``

    .. versionchanged:: 0.3.0
        Extensive change to the function signatures.

    """

    def init_fixtures(self):
        """Initialize the fixtures.

        This function *must* be called before doing anything else.
        """
        self.fixtures_manager.clean_cache()

        if hasattr(self, "fixtures"):
            self.install_fixtures(self.fixtures)

    @copy_docstring_from(FixturesManager)
    def install_fixture(self, fixture_key,
                        attrs=None,
                        do_not_save=False,
                        include_relationships=True
                        ):
        fixture = self.fixtures_manager.install_fixture(
            fixture_key, do_not_save, include_relationships, attrs)
        setattr(self, fixture_key, fixture)
        return fixture

    @copy_docstring_from(FixturesManager)
    def install_fixtures(self, fixtures, do_not_save=False,
                         include_relationships=True):
        installed = []
        for fixture in make_list(fixtures):
            installed.append(
                self.install_fixture(
                    fixture, do_not_save=do_not_save,
                    include_relationships=include_relationships)
            )

        return installed

    @copy_docstring_from(FixturesManager)
    def install_all_fixtures(self, do_not_save=False,
                             include_relationships=True):
        return self.install_fixtures(
            self.fixtures_manager.fixtures.keys(),
            do_not_save=do_not_save,
            include_relationships=include_relationships,
        )

    @copy_docstring_from(FixturesManager)
    def get_fixture(self, fixture_key,
                    include_relationships=True,
                    attrs=None):
        return self.fixtures_manager.get_fixture(
            fixture_key, include_relationships, attrs)

    @copy_docstring_from(FixturesManager)
    def get_fixtures(self, fixtures,
                     include_relationships=True):
        return self.fixtures_manager.get_fixtures(
            fixtures, include_relationships)

    @copy_docstring_from(FixturesManager)
    def uninstall_fixture(self, fixture_key, do_not_delete=False):
        fixture = self.fixtures_manager.uninstall_fixture(
            fixture_key, do_not_delete)

        if fixture:
            delattr(self, fixture_key)

        return fixture

    @copy_docstring_from(FixturesManager)
    def uninstall_fixtures(self, fixtures, do_not_delete=False):
        uninstalled = []
        for fixture in make_list(fixtures):
            instance = self.uninstall_fixture(
                fixture,
                do_not_delete=do_not_delete)
            if instance:
                uninstalled.append(instance)

        return uninstalled

    @copy_docstring_from(FixturesManager)
    def uninstall_all_fixtures(self, do_not_delete=False):
        # copy and reverse the list in order to remove objects with
        # relationships first
        installed_fixtures = list(self.fixtures_manager.installed_keys)
        installed_fixtures.reverse()
        return self.uninstall_fixtures(
            installed_fixtures,
            do_not_delete=do_not_delete
        )
