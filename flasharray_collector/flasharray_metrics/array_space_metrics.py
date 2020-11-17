from prometheus_client.core import GaugeMetricFamily


class ArraySpaceMetrics():
    """
    Base class for FlashArray Prometheus array space metrics
    """
    def __init__(self, fa):
        self.fa = fa
        self.data_reduction = None
        self.capacity = None
        self.provisioned = None
        self.used = None

    def _data_reduction(self):
        """
        Create metrics of gauge type for array data reduction.
        Metrics values can be iterated over.
        """
        self.data_reduction = GaugeMetricFamily(
                                      'purefa_array_space_datareduction_ratio',
                                      'FlashArray overall data reduction',
                                      unit='ratio')
        self.data_reduction.add_metric([], self.fa.get_array_elem('data_reduction'))

    def _capacity(self):
        """
        Create metrics of gauge type for array capacity indicators.
        Metrics values can be iterated over.
        """
        self.capacity = GaugeMetricFamily('purefa_array_space_capacity_bytes',
                                     'FlashArray overall space capacity')
        self.capacity.add_metric([], self.fa.get_array_elem('capacity'))

    def _provisioned(self):
        """
        Create metrics of gauge type for array provisioned space indicators.
        Metrics values can be iterated over.
        """
        self.provisioned = GaugeMetricFamily(
                                        'purefa_array_space_provisioned_bytes',
                                        'FlashArray overall provisioned space')
        self.provisioned.add_metric([], self.fa.get_array_elem('provisioned'))

    def _used(self):
        """
        Create metrics of gauge type for array used space indicators.
        Metrics values can be iterated over.
        """
        self.used = GaugeMetricFamily('purefa_array_space_used_bytes',
                                      'FlashArray overall used space',
                                      labels=['dimension'])
        self.used.add_metric(['shared'], self.fa.get_array_elem('shared_space'))
        self.used.add_metric(['system'], self.fa.get_array_elem('system'))
        self.used.add_metric(['volumes'], self.fa.get_array_elem('volumes'))
        self.used.add_metric(['snapshots'], self.fa.get_array_elem('snapshots'))
        if self.fa.get_array_elem('replication') is not None:
            self.used.add_metric(['replication'], self.fa.get_array_elem('replication'))

    def get_metrics(self):
        self._data_reduction()
        self._capacity()
        self._provisioned()
        self._used()
        yield self.data_reduction
        yield self.capacity
        yield self.provisioned
        yield self.used