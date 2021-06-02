from am_adapters.am_adapter_abc import AMAdapter


class AMAdapterMock(AMAdapter):
    """
    This class is a mock version of the AMAdapter.
    """
    def activate_microscope(self):
        pass

    def parse_regions(self):
        pass

    def event_handle(self, coords):
        pass
