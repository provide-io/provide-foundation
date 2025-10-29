# provide/foundation/file/quality/analyzer.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Quality analyzer for file operation detection."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import time
from typing import Any

try:
    from provide.foundation.file.operations import OperationDetector

    HAS_OPERATIONS_MODULE = True
except ImportError:
    HAS_OPERATIONS_MODULE = False

from provide.foundation.file.quality.metrics import AnalysisMetric, QualityResult
from provide.foundation.file.quality.operation_scenarios import OperationScenario
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class QualityAnalyzer:
    """Analyzer for measuring file operation detection quality."""

    def xǁQualityAnalyzerǁ__init____mutmut_orig(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("File operations module not available")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_1(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if HAS_OPERATIONS_MODULE:
            raise ImportError("File operations module not available")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_2(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError(None)

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_3(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("XXFile operations module not availableXX")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_4(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("file operations module not available")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_5(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("FILE OPERATIONS MODULE NOT AVAILABLE")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_6(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("File operations module not available")

        self.detector = None
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_7(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("File operations module not available")

        self.detector = detector and OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_8(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("File operations module not available")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = None
        self.results: list[QualityResult] = []

    def xǁQualityAnalyzerǁ__init____mutmut_9(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("File operations module not available")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = None

    xǁQualityAnalyzerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ__init____mutmut_1": xǁQualityAnalyzerǁ__init____mutmut_1,
        "xǁQualityAnalyzerǁ__init____mutmut_2": xǁQualityAnalyzerǁ__init____mutmut_2,
        "xǁQualityAnalyzerǁ__init____mutmut_3": xǁQualityAnalyzerǁ__init____mutmut_3,
        "xǁQualityAnalyzerǁ__init____mutmut_4": xǁQualityAnalyzerǁ__init____mutmut_4,
        "xǁQualityAnalyzerǁ__init____mutmut_5": xǁQualityAnalyzerǁ__init____mutmut_5,
        "xǁQualityAnalyzerǁ__init____mutmut_6": xǁQualityAnalyzerǁ__init____mutmut_6,
        "xǁQualityAnalyzerǁ__init____mutmut_7": xǁQualityAnalyzerǁ__init____mutmut_7,
        "xǁQualityAnalyzerǁ__init____mutmut_8": xǁQualityAnalyzerǁ__init____mutmut_8,
        "xǁQualityAnalyzerǁ__init____mutmut_9": xǁQualityAnalyzerǁ__init____mutmut_9,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁ__init____mutmut_orig)
    xǁQualityAnalyzerǁ__init____mutmut_orig.__name__ = "xǁQualityAnalyzerǁ__init__"

    def xǁQualityAnalyzerǁadd_scenario__mutmut_orig(self, scenario: OperationScenario) -> None:
        """Add a scenario for analysis.

        Args:
            scenario: Scenario to add
        """
        self.scenarios.append(scenario)

    def xǁQualityAnalyzerǁadd_scenario__mutmut_1(self, scenario: OperationScenario) -> None:
        """Add a scenario for analysis.

        Args:
            scenario: Scenario to add
        """
        self.scenarios.append(None)

    xǁQualityAnalyzerǁadd_scenario__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁadd_scenario__mutmut_1": xǁQualityAnalyzerǁadd_scenario__mutmut_1
    }

    def add_scenario(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁadd_scenario__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁadd_scenario__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    add_scenario.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁadd_scenario__mutmut_orig)
    xǁQualityAnalyzerǁadd_scenario__mutmut_orig.__name__ = "xǁQualityAnalyzerǁadd_scenario"

    def xǁQualityAnalyzerǁrun_analysis__mutmut_orig(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_1(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_2(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError(None)

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_3(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("XXNo scenarios available for analysisXX")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_4(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("no scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_5(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("NO SCENARIOS AVAILABLE FOR ANALYSIS")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_6(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is not None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_7(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = None

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_8(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(None)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_9(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = None

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_10(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = None

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_11(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(None, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_12(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, None, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_13(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, None)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_14(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_15(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, timing_results)

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_16(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(
            metrics,
            detection_results,
        )

        self.results.extend(results.values())
        return results

    def xǁQualityAnalyzerǁrun_analysis__mutmut_17(
        self, metrics: list[AnalysisMetric] | None = None
    ) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(None)
        return results

    xǁQualityAnalyzerǁrun_analysis__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁrun_analysis__mutmut_1": xǁQualityAnalyzerǁrun_analysis__mutmut_1,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_2": xǁQualityAnalyzerǁrun_analysis__mutmut_2,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_3": xǁQualityAnalyzerǁrun_analysis__mutmut_3,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_4": xǁQualityAnalyzerǁrun_analysis__mutmut_4,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_5": xǁQualityAnalyzerǁrun_analysis__mutmut_5,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_6": xǁQualityAnalyzerǁrun_analysis__mutmut_6,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_7": xǁQualityAnalyzerǁrun_analysis__mutmut_7,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_8": xǁQualityAnalyzerǁrun_analysis__mutmut_8,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_9": xǁQualityAnalyzerǁrun_analysis__mutmut_9,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_10": xǁQualityAnalyzerǁrun_analysis__mutmut_10,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_11": xǁQualityAnalyzerǁrun_analysis__mutmut_11,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_12": xǁQualityAnalyzerǁrun_analysis__mutmut_12,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_13": xǁQualityAnalyzerǁrun_analysis__mutmut_13,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_14": xǁQualityAnalyzerǁrun_analysis__mutmut_14,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_15": xǁQualityAnalyzerǁrun_analysis__mutmut_15,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_16": xǁQualityAnalyzerǁrun_analysis__mutmut_16,
        "xǁQualityAnalyzerǁrun_analysis__mutmut_17": xǁQualityAnalyzerǁrun_analysis__mutmut_17,
    }

    def run_analysis(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁrun_analysis__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁrun_analysis__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    run_analysis.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁrun_analysis__mutmut_orig)
    xǁQualityAnalyzerǁrun_analysis__mutmut_orig.__name__ = "xǁQualityAnalyzerǁrun_analysis"

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_orig(
        self,
    ) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_1(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = None
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_2(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = None

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_3(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = None
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_4(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = None
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_5(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(None)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_6(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = None

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_7(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = None  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_8(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) / 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_9(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time + start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_10(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1001  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_11(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(None)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_12(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(None)

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_13(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "XXscenarioXX": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_14(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "SCENARIO": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_15(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "XXdetectedXX": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_16(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "DETECTED": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_17(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "XXdetection_timeXX": detection_time,
                }
            )

        return detection_results, timing_results

    def xǁQualityAnalyzerǁ_collect_detection_data__mutmut_18(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "DETECTION_TIME": detection_time,
                }
            )

        return detection_results, timing_results

    xǁQualityAnalyzerǁ_collect_detection_data__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_1": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_1,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_2": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_2,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_3": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_3,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_4": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_4,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_5": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_5,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_6": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_6,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_7": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_7,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_8": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_8,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_9": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_9,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_10": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_10,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_11": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_11,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_12": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_12,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_13": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_13,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_14": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_14,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_15": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_15,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_16": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_16,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_17": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_17,
        "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_18": xǁQualityAnalyzerǁ_collect_detection_data__mutmut_18,
    }

    def _collect_detection_data(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_collect_detection_data__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _collect_detection_data.__signature__ = _mutmut_signature(
        xǁQualityAnalyzerǁ_collect_detection_data__mutmut_orig
    )
    xǁQualityAnalyzerǁ_collect_detection_data__mutmut_orig.__name__ = (
        "xǁQualityAnalyzerǁ_collect_detection_data"
    )

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_orig(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_1(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = None

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_2(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric != AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_3(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = None
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_4(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(None)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_5(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric != AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_6(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = None
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_7(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(None)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_8(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric != AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_9(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = None
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_10(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(None)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_11(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric != AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_12(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = None
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_13(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(None)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_14(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = None
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_15(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(None)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_16(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = None
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_17(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(None, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_18(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, None)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_19(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_20(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(
                    precision.value,
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_21(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric != AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_22(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = None
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_23(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(None)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_24(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric != AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_25(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = None
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_26(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(None)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_27(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric != AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_28(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = None
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_29(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(None)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_30(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric != AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_31(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = None

        return results

    def xǁQualityAnalyzerǁ_calculate_metrics__mutmut_32(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(None)

        return results

    xǁQualityAnalyzerǁ_calculate_metrics__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_1": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_1,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_2": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_2,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_3": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_3,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_4": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_4,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_5": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_5,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_6": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_6,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_7": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_7,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_8": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_8,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_9": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_9,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_10": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_10,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_11": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_11,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_12": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_12,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_13": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_13,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_14": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_14,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_15": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_15,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_16": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_16,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_17": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_17,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_18": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_18,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_19": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_19,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_20": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_20,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_21": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_21,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_22": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_22,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_23": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_23,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_24": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_24,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_25": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_25,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_26": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_26,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_27": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_27,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_28": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_28,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_29": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_29,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_30": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_30,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_31": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_31,
        "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_32": xǁQualityAnalyzerǁ_calculate_metrics__mutmut_32,
    }

    def _calculate_metrics(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_metrics__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _calculate_metrics.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁ_calculate_metrics__mutmut_orig)
    xǁQualityAnalyzerǁ_calculate_metrics__mutmut_orig.__name__ = "xǁQualityAnalyzerǁ_calculate_metrics"

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_orig(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_1(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = None
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_2(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 1
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_3(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = None

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_4(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 1

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_5(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = None
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_6(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["XXscenarioXX"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_7(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["SCENARIO"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_8(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = None
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_9(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["XXdetectedXX"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_10(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["DETECTED"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_11(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = None

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_12(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = None
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_13(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = None

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_14(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["XXtypeXX"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_15(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["TYPE"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_16(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = None
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_17(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(None)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_18(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = None

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_19(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(None)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_20(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = None
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_21(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(None, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_22(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, None)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_23(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_24(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(
                    op_type,
                )
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_25(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 1)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_26(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections = min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_27(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections -= min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_28(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(None, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_29(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, None)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_30(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_31(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(
                    expected_count,
                )

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_32(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections = max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_33(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections -= max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_34(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(None, len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_35(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), None)

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_36(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_37(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(
                len(detected_types),
            )

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_38(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = None

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_39(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections * total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_40(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections >= 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_41(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 1 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_42(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 1.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_43(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=None,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_44(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=None,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_45(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details=None,
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_46(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_47(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_48(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_49(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "XXcorrect_detectionsXX": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_50(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "CORRECT_DETECTIONS": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_51(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "XXtotal_detectionsXX": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_52(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "TOTAL_DETECTIONS": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_53(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "XXpercentageXX": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_54(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "PERCENTAGE": accuracy * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_55(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy / 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_56(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 101,
            },
        )

    xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_1": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_1,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_2": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_2,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_3": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_3,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_4": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_4,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_5": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_5,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_6": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_6,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_7": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_7,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_8": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_8,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_9": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_9,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_10": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_10,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_11": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_11,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_12": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_12,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_13": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_13,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_14": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_14,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_15": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_15,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_16": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_16,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_17": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_17,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_18": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_18,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_19": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_19,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_20": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_20,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_21": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_21,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_22": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_22,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_23": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_23,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_24": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_24,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_25": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_25,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_26": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_26,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_27": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_27,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_28": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_28,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_29": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_29,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_30": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_30,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_31": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_31,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_32": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_32,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_33": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_33,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_34": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_34,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_35": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_35,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_36": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_36,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_37": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_37,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_38": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_38,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_39": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_39,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_40": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_40,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_41": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_41,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_42": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_42,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_43": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_43,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_44": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_44,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_45": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_45,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_46": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_46,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_47": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_47,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_48": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_48,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_49": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_49,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_50": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_50,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_51": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_51,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_52": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_52,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_53": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_53,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_54": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_54,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_55": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_55,
        "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_56": xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_56,
    }

    def _calculate_accuracy(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _calculate_accuracy.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_orig)
    xǁQualityAnalyzerǁ_calculate_accuracy__mutmut_orig.__name__ = "xǁQualityAnalyzerǁ_calculate_accuracy"

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_orig(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_1(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = None
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_2(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 1
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_3(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = None

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_4(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 1

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_5(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = None
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_6(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["XXscenarioXX"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_7(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["SCENARIO"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_8(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = None
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_9(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["XXdetectedXX"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_10(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["DETECTED"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_11(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = None

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_12(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = None
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_13(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = None

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_14(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["XXtypeXX"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_15(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["TYPE"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_16(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = None

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_17(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(None)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_18(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(None, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_19(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, None) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_20(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_21(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if (
                    expected_counter.get(
                        detected_type,
                    )
                    > 0
                ):
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_22(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 1) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_23(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) >= 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_24(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 1:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_25(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives = 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_26(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives -= 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_27(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 2
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_28(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] = 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_29(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] += 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_30(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 2
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_31(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives = 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_32(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives -= 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_33(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 2

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_34(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = None

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_35(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives * (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_36(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives - false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_37(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives - false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_38(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) >= 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_39(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 1
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_40(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 1.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_41(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=None,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_42(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=None,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_43(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details=None,
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_44(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_45(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_46(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_47(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "XXtrue_positivesXX": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_48(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "TRUE_POSITIVES": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_49(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "XXfalse_positivesXX": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_50(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "FALSE_POSITIVES": false_positives,
                "percentage": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_51(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "XXpercentageXX": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_52(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "PERCENTAGE": precision * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_53(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision / 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_precision__mutmut_54(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 101,
            },
        )

    xǁQualityAnalyzerǁ_calculate_precision__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_1": xǁQualityAnalyzerǁ_calculate_precision__mutmut_1,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_2": xǁQualityAnalyzerǁ_calculate_precision__mutmut_2,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_3": xǁQualityAnalyzerǁ_calculate_precision__mutmut_3,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_4": xǁQualityAnalyzerǁ_calculate_precision__mutmut_4,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_5": xǁQualityAnalyzerǁ_calculate_precision__mutmut_5,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_6": xǁQualityAnalyzerǁ_calculate_precision__mutmut_6,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_7": xǁQualityAnalyzerǁ_calculate_precision__mutmut_7,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_8": xǁQualityAnalyzerǁ_calculate_precision__mutmut_8,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_9": xǁQualityAnalyzerǁ_calculate_precision__mutmut_9,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_10": xǁQualityAnalyzerǁ_calculate_precision__mutmut_10,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_11": xǁQualityAnalyzerǁ_calculate_precision__mutmut_11,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_12": xǁQualityAnalyzerǁ_calculate_precision__mutmut_12,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_13": xǁQualityAnalyzerǁ_calculate_precision__mutmut_13,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_14": xǁQualityAnalyzerǁ_calculate_precision__mutmut_14,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_15": xǁQualityAnalyzerǁ_calculate_precision__mutmut_15,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_16": xǁQualityAnalyzerǁ_calculate_precision__mutmut_16,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_17": xǁQualityAnalyzerǁ_calculate_precision__mutmut_17,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_18": xǁQualityAnalyzerǁ_calculate_precision__mutmut_18,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_19": xǁQualityAnalyzerǁ_calculate_precision__mutmut_19,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_20": xǁQualityAnalyzerǁ_calculate_precision__mutmut_20,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_21": xǁQualityAnalyzerǁ_calculate_precision__mutmut_21,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_22": xǁQualityAnalyzerǁ_calculate_precision__mutmut_22,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_23": xǁQualityAnalyzerǁ_calculate_precision__mutmut_23,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_24": xǁQualityAnalyzerǁ_calculate_precision__mutmut_24,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_25": xǁQualityAnalyzerǁ_calculate_precision__mutmut_25,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_26": xǁQualityAnalyzerǁ_calculate_precision__mutmut_26,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_27": xǁQualityAnalyzerǁ_calculate_precision__mutmut_27,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_28": xǁQualityAnalyzerǁ_calculate_precision__mutmut_28,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_29": xǁQualityAnalyzerǁ_calculate_precision__mutmut_29,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_30": xǁQualityAnalyzerǁ_calculate_precision__mutmut_30,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_31": xǁQualityAnalyzerǁ_calculate_precision__mutmut_31,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_32": xǁQualityAnalyzerǁ_calculate_precision__mutmut_32,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_33": xǁQualityAnalyzerǁ_calculate_precision__mutmut_33,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_34": xǁQualityAnalyzerǁ_calculate_precision__mutmut_34,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_35": xǁQualityAnalyzerǁ_calculate_precision__mutmut_35,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_36": xǁQualityAnalyzerǁ_calculate_precision__mutmut_36,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_37": xǁQualityAnalyzerǁ_calculate_precision__mutmut_37,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_38": xǁQualityAnalyzerǁ_calculate_precision__mutmut_38,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_39": xǁQualityAnalyzerǁ_calculate_precision__mutmut_39,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_40": xǁQualityAnalyzerǁ_calculate_precision__mutmut_40,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_41": xǁQualityAnalyzerǁ_calculate_precision__mutmut_41,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_42": xǁQualityAnalyzerǁ_calculate_precision__mutmut_42,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_43": xǁQualityAnalyzerǁ_calculate_precision__mutmut_43,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_44": xǁQualityAnalyzerǁ_calculate_precision__mutmut_44,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_45": xǁQualityAnalyzerǁ_calculate_precision__mutmut_45,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_46": xǁQualityAnalyzerǁ_calculate_precision__mutmut_46,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_47": xǁQualityAnalyzerǁ_calculate_precision__mutmut_47,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_48": xǁQualityAnalyzerǁ_calculate_precision__mutmut_48,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_49": xǁQualityAnalyzerǁ_calculate_precision__mutmut_49,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_50": xǁQualityAnalyzerǁ_calculate_precision__mutmut_50,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_51": xǁQualityAnalyzerǁ_calculate_precision__mutmut_51,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_52": xǁQualityAnalyzerǁ_calculate_precision__mutmut_52,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_53": xǁQualityAnalyzerǁ_calculate_precision__mutmut_53,
        "xǁQualityAnalyzerǁ_calculate_precision__mutmut_54": xǁQualityAnalyzerǁ_calculate_precision__mutmut_54,
    }

    def _calculate_precision(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_precision__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_precision__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _calculate_precision.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁ_calculate_precision__mutmut_orig)
    xǁQualityAnalyzerǁ_calculate_precision__mutmut_orig.__name__ = "xǁQualityAnalyzerǁ_calculate_precision"

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_orig(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_1(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = None
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_2(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 1
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_3(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = None

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_4(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 1

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_5(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = None
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_6(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["XXscenarioXX"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_7(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["SCENARIO"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_8(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = None
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_9(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["XXdetectedXX"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_10(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["DETECTED"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_11(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = None

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_12(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = None
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_13(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = None

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_14(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["XXtypeXX"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_15(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["TYPE"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_16(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = None

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_17(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(None)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_18(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(None, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_19(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, None) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_20(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_21(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if (
                    detected_counter.get(
                        expected_type,
                    )
                    > 0
                ):
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_22(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 1) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_23(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) >= 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_24(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 1:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_25(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives = 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_26(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives -= 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_27(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 2
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_28(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] = 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_29(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] += 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_30(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 2
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_31(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives = 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_32(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives -= 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_33(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 2

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_34(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = None

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_35(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives * (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_36(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives - false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_37(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives - false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_38(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) >= 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_39(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 1
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_40(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 1.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_41(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=None,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_42(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=None,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_43(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details=None,
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_44(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_45(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_46(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_47(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "XXtrue_positivesXX": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_48(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "TRUE_POSITIVES": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_49(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "XXfalse_negativesXX": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_50(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "FALSE_NEGATIVES": false_negatives,
                "percentage": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_51(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "XXpercentageXX": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_52(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "PERCENTAGE": recall * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_53(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall / 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_recall__mutmut_54(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 101,
            },
        )

    xǁQualityAnalyzerǁ_calculate_recall__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_1": xǁQualityAnalyzerǁ_calculate_recall__mutmut_1,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_2": xǁQualityAnalyzerǁ_calculate_recall__mutmut_2,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_3": xǁQualityAnalyzerǁ_calculate_recall__mutmut_3,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_4": xǁQualityAnalyzerǁ_calculate_recall__mutmut_4,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_5": xǁQualityAnalyzerǁ_calculate_recall__mutmut_5,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_6": xǁQualityAnalyzerǁ_calculate_recall__mutmut_6,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_7": xǁQualityAnalyzerǁ_calculate_recall__mutmut_7,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_8": xǁQualityAnalyzerǁ_calculate_recall__mutmut_8,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_9": xǁQualityAnalyzerǁ_calculate_recall__mutmut_9,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_10": xǁQualityAnalyzerǁ_calculate_recall__mutmut_10,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_11": xǁQualityAnalyzerǁ_calculate_recall__mutmut_11,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_12": xǁQualityAnalyzerǁ_calculate_recall__mutmut_12,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_13": xǁQualityAnalyzerǁ_calculate_recall__mutmut_13,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_14": xǁQualityAnalyzerǁ_calculate_recall__mutmut_14,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_15": xǁQualityAnalyzerǁ_calculate_recall__mutmut_15,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_16": xǁQualityAnalyzerǁ_calculate_recall__mutmut_16,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_17": xǁQualityAnalyzerǁ_calculate_recall__mutmut_17,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_18": xǁQualityAnalyzerǁ_calculate_recall__mutmut_18,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_19": xǁQualityAnalyzerǁ_calculate_recall__mutmut_19,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_20": xǁQualityAnalyzerǁ_calculate_recall__mutmut_20,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_21": xǁQualityAnalyzerǁ_calculate_recall__mutmut_21,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_22": xǁQualityAnalyzerǁ_calculate_recall__mutmut_22,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_23": xǁQualityAnalyzerǁ_calculate_recall__mutmut_23,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_24": xǁQualityAnalyzerǁ_calculate_recall__mutmut_24,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_25": xǁQualityAnalyzerǁ_calculate_recall__mutmut_25,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_26": xǁQualityAnalyzerǁ_calculate_recall__mutmut_26,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_27": xǁQualityAnalyzerǁ_calculate_recall__mutmut_27,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_28": xǁQualityAnalyzerǁ_calculate_recall__mutmut_28,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_29": xǁQualityAnalyzerǁ_calculate_recall__mutmut_29,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_30": xǁQualityAnalyzerǁ_calculate_recall__mutmut_30,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_31": xǁQualityAnalyzerǁ_calculate_recall__mutmut_31,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_32": xǁQualityAnalyzerǁ_calculate_recall__mutmut_32,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_33": xǁQualityAnalyzerǁ_calculate_recall__mutmut_33,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_34": xǁQualityAnalyzerǁ_calculate_recall__mutmut_34,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_35": xǁQualityAnalyzerǁ_calculate_recall__mutmut_35,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_36": xǁQualityAnalyzerǁ_calculate_recall__mutmut_36,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_37": xǁQualityAnalyzerǁ_calculate_recall__mutmut_37,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_38": xǁQualityAnalyzerǁ_calculate_recall__mutmut_38,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_39": xǁQualityAnalyzerǁ_calculate_recall__mutmut_39,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_40": xǁQualityAnalyzerǁ_calculate_recall__mutmut_40,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_41": xǁQualityAnalyzerǁ_calculate_recall__mutmut_41,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_42": xǁQualityAnalyzerǁ_calculate_recall__mutmut_42,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_43": xǁQualityAnalyzerǁ_calculate_recall__mutmut_43,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_44": xǁQualityAnalyzerǁ_calculate_recall__mutmut_44,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_45": xǁQualityAnalyzerǁ_calculate_recall__mutmut_45,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_46": xǁQualityAnalyzerǁ_calculate_recall__mutmut_46,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_47": xǁQualityAnalyzerǁ_calculate_recall__mutmut_47,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_48": xǁQualityAnalyzerǁ_calculate_recall__mutmut_48,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_49": xǁQualityAnalyzerǁ_calculate_recall__mutmut_49,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_50": xǁQualityAnalyzerǁ_calculate_recall__mutmut_50,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_51": xǁQualityAnalyzerǁ_calculate_recall__mutmut_51,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_52": xǁQualityAnalyzerǁ_calculate_recall__mutmut_52,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_53": xǁQualityAnalyzerǁ_calculate_recall__mutmut_53,
        "xǁQualityAnalyzerǁ_calculate_recall__mutmut_54": xǁQualityAnalyzerǁ_calculate_recall__mutmut_54,
    }

    def _calculate_recall(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_recall__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_recall__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _calculate_recall.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁ_calculate_recall__mutmut_orig)
    xǁQualityAnalyzerǁ_calculate_recall__mutmut_orig.__name__ = "xǁQualityAnalyzerǁ_calculate_recall"

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_orig(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_1(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = None

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_2(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) * (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_3(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 / (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_4(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 3 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_5(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision / recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_6(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision - recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_7(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision - recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_8(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) >= 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_9(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 1 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_10(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 1.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_11(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=None,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_12(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=None,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_13(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details=None,
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_14(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_15(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_16(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_17(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "XXprecisionXX": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_18(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "PRECISION": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_19(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "XXrecallXX": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_20(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "RECALL": recall,
                "percentage": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_21(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "XXpercentageXX": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_22(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "PERCENTAGE": f1 * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_23(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 / 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_24(
        self, precision: float, recall: float
    ) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 101,
            },
        )

    xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_1": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_1,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_2": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_2,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_3": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_3,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_4": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_4,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_5": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_5,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_6": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_6,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_7": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_7,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_8": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_8,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_9": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_9,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_10": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_10,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_11": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_11,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_12": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_12,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_13": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_13,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_14": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_14,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_15": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_15,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_16": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_16,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_17": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_17,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_18": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_18,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_19": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_19,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_20": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_20,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_21": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_21,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_22": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_22,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_23": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_23,
        "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_24": xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_24,
    }

    def _calculate_f1_score(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _calculate_f1_score.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_orig)
    xǁQualityAnalyzerǁ_calculate_f1_score__mutmut_orig.__name__ = "xǁQualityAnalyzerǁ_calculate_f1_score"

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_orig(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_1(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = None
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_2(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = None

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_3(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(None)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_4(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = None

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_5(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["XXdetectedXX"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_6(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["DETECTED"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_7(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = None
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_8(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(None)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_9(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(None)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_10(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_11(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=None,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_12(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=None,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_13(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details=None,
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_14(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_15(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_16(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_17(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=1.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_18(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"XXerrorXX": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_19(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"ERROR": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_20(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "XXNo confidence scores availableXX"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_21(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "no confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_22(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "NO CONFIDENCE SCORES AVAILABLE"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_23(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = None
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_24(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) * len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_25(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(None) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_26(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = None
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_27(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(None)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_28(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = None

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_29(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(None)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_30(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = None
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_31(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = None

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_32(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "XXcountXX": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_33(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "COUNT": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_34(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "XXaverageXX": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_35(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "AVERAGE": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_36(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) * len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_37(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(None) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_38(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "XXminXX": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_39(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "MIN": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_40(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(None),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_41(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "XXmaxXX": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_42(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "MAX": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_43(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(None),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_44(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=None,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_45(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=None,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_46(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details=None,
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_47(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_48(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_49(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_50(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "XXtotal_operationsXX": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_51(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "TOTAL_OPERATIONS": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_52(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "XXaverageXX": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_53(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "AVERAGE": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_54(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "XXminXX": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_55(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "MIN": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_56(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "XXmaxXX": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_57(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "MAX": max_confidence,
                "by_type": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_58(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "XXby_typeXX": type_stats,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_59(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "BY_TYPE": type_stats,
            },
        )

    xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_1": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_1,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_2": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_2,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_3": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_3,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_4": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_4,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_5": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_5,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_6": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_6,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_7": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_7,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_8": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_8,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_9": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_9,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_10": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_10,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_11": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_11,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_12": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_12,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_13": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_13,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_14": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_14,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_15": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_15,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_16": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_16,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_17": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_17,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_18": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_18,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_19": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_19,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_20": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_20,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_21": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_21,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_22": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_22,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_23": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_23,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_24": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_24,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_25": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_25,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_26": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_26,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_27": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_27,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_28": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_28,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_29": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_29,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_30": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_30,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_31": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_31,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_32": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_32,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_33": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_33,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_34": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_34,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_35": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_35,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_36": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_36,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_37": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_37,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_38": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_38,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_39": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_39,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_40": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_40,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_41": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_41,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_42": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_42,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_43": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_43,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_44": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_44,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_45": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_45,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_46": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_46,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_47": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_47,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_48": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_48,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_49": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_49,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_50": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_50,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_51": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_51,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_52": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_52,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_53": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_53,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_54": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_54,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_55": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_55,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_56": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_56,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_57": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_57,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_58": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_58,
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_59": xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_59,
    }

    def _analyze_confidence_distribution(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_orig"),
            object.__getattribute__(
                self, "xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    _analyze_confidence_distribution.__signature__ = _mutmut_signature(
        xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_orig
    )
    xǁQualityAnalyzerǁ_analyze_confidence_distribution__mutmut_orig.__name__ = (
        "xǁQualityAnalyzerǁ_analyze_confidence_distribution"
    )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_orig(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_1(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_2(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(metric=None, value=0.0, details={"error": "No timing data available"})

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_3(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=None, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_4(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(metric=AnalysisMetric.DETECTION_TIME, value=0.0, details=None)

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_5(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(value=0.0, details={"error": "No timing data available"})

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_6(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_7(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME,
                value=0.0,
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_8(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=1.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_9(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME,
                value=0.0,
                details={"XXerrorXX": "No timing data available"},
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_10(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"ERROR": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_11(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME,
                value=0.0,
                details={"error": "XXNo timing data availableXX"},
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_12(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "no timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_13(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "NO TIMING DATA AVAILABLE"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_14(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = None
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_15(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) * len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_16(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(None) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_17(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = None
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_18(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(None)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_19(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = None

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_20(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(None)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_21(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = None
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_22(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(None)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_23(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = None
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_24(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = None
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_25(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n / 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_26(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 3]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_27(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = None
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_28(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(None)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_29(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n / 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_30(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 1.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_31(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = None

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_32(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(None)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_33(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n / 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_34(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 1.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_35(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=None,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_36(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=None,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_37(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details=None,
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_38(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_39(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_40(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_41(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "XXtotal_testsXX": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_42(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "TOTAL_TESTS": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_43(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "XXaverage_msXX": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_44(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "AVERAGE_MS": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_45(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "XXmin_msXX": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_46(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "MIN_MS": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_47(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "XXmax_msXX": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_48(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "MAX_MS": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_49(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "XXp50_msXX": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_50(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "P50_MS": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_51(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "XXp95_msXX": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_52(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "P95_MS": p95,
                "p99_ms": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_53(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "XXp99_msXX": p99,
            },
        )

    def xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_54(
        self, timing_results: list[float]
    ) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "P99_MS": p99,
            },
        )

    xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_1": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_1,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_2": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_2,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_3": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_3,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_4": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_4,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_5": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_5,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_6": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_6,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_7": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_7,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_8": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_8,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_9": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_9,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_10": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_10,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_11": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_11,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_12": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_12,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_13": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_13,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_14": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_14,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_15": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_15,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_16": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_16,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_17": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_17,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_18": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_18,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_19": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_19,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_20": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_20,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_21": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_21,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_22": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_22,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_23": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_23,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_24": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_24,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_25": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_25,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_26": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_26,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_27": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_27,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_28": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_28,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_29": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_29,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_30": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_30,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_31": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_31,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_32": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_32,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_33": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_33,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_34": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_34,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_35": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_35,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_36": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_36,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_37": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_37,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_38": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_38,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_39": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_39,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_40": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_40,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_41": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_41,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_42": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_42,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_43": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_43,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_44": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_44,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_45": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_45,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_46": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_46,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_47": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_47,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_48": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_48,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_49": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_49,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_50": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_50,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_51": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_51,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_52": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_52,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_53": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_53,
        "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_54": xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_54,
    }

    def _analyze_detection_time(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _analyze_detection_time.__signature__ = _mutmut_signature(
        xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_orig
    )
    xǁQualityAnalyzerǁ_analyze_detection_time__mutmut_orig.__name__ = (
        "xǁQualityAnalyzerǁ_analyze_detection_time"
    )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_orig(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_1(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = None
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_2(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 1
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_3(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = None

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_4(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 1

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_5(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = None
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_6(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["XXscenarioXX"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_7(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["SCENARIO"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_8(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = None
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_9(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["XXdetectedXX"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_10(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["DETECTED"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_11(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = None

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_12(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected or detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_13(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_14(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives = len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_15(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives -= len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_16(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases = 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_17(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases -= 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_18(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 2
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_19(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_20(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases = 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_21(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases -= 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_22(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 2

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_23(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = None

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_24(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives * total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_25(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases >= 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_26(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 1 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_27(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 1.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_28(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=None,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_29(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=None,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_30(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details=None,
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_31(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_32(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_33(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_34(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "XXfalse_positivesXX": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_35(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "FALSE_POSITIVES": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_36(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "XXtotal_negative_casesXX": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_37(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "TOTAL_NEGATIVE_CASES": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_38(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "XXpercentageXX": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_39(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "PERCENTAGE": fpr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_40(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr / 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_41(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 101,
            },
        )

    xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_1": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_1,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_2": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_2,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_3": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_3,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_4": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_4,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_5": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_5,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_6": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_6,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_7": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_7,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_8": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_8,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_9": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_9,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_10": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_10,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_11": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_11,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_12": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_12,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_13": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_13,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_14": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_14,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_15": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_15,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_16": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_16,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_17": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_17,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_18": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_18,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_19": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_19,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_20": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_20,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_21": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_21,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_22": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_22,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_23": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_23,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_24": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_24,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_25": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_25,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_26": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_26,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_27": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_27,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_28": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_28,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_29": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_29,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_30": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_30,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_31": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_31,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_32": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_32,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_33": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_33,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_34": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_34,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_35": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_35,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_36": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_36,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_37": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_37,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_38": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_38,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_39": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_39,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_40": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_40,
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_41": xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_41,
    }

    def _calculate_false_positive_rate(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _calculate_false_positive_rate.__signature__ = _mutmut_signature(
        xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_orig
    )
    xǁQualityAnalyzerǁ_calculate_false_positive_rate__mutmut_orig.__name__ = (
        "xǁQualityAnalyzerǁ_calculate_false_positive_rate"
    )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_orig(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_1(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = None
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_2(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 1
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_3(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = None

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_4(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 1

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_5(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = None
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_6(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["XXscenarioXX"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_7(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["SCENARIO"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_8(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = None
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_9(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["XXdetectedXX"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_10(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["DETECTED"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_11(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = None

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_12(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases = len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_13(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases -= len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_14(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = None
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_15(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = None

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_16(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["XXtypeXX"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_17(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["TYPE"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_18(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = None

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_19(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(None)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_20(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(None, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_21(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, None) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_22(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_23(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if (
                        detected_counter.get(
                            expected_type,
                        )
                        > 0
                    ):
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_24(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 1) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_25(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) >= 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_26(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 1:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_27(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] = 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_28(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] += 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_29(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 2
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_30(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives = 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_31(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives -= 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_32(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 2

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_33(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = None

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_34(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives * total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_35(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases >= 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_36(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 1 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_37(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 1.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_38(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=None,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_39(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=None,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_40(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details=None,
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_41(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_42(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_43(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_44(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "XXfalse_negativesXX": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_45(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "FALSE_NEGATIVES": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_46(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "XXtotal_positive_casesXX": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_47(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "TOTAL_POSITIVE_CASES": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_48(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "XXpercentageXX": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_49(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "PERCENTAGE": fnr * 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_50(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr / 100,
            },
        )

    def xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_51(
        self, detection_results: list[dict[str, Any]]
    ) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 101,
            },
        )

    xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_1": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_1,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_2": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_2,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_3": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_3,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_4": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_4,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_5": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_5,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_6": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_6,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_7": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_7,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_8": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_8,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_9": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_9,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_10": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_10,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_11": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_11,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_12": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_12,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_13": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_13,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_14": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_14,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_15": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_15,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_16": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_16,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_17": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_17,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_18": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_18,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_19": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_19,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_20": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_20,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_21": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_21,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_22": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_22,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_23": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_23,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_24": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_24,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_25": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_25,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_26": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_26,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_27": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_27,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_28": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_28,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_29": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_29,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_30": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_30,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_31": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_31,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_32": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_32,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_33": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_33,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_34": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_34,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_35": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_35,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_36": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_36,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_37": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_37,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_38": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_38,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_39": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_39,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_40": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_40,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_41": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_41,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_42": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_42,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_43": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_43,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_44": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_44,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_45": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_45,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_46": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_46,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_47": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_47,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_48": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_48,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_49": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_49,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_50": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_50,
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_51": xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_51,
    }

    def _calculate_false_negative_rate(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _calculate_false_negative_rate.__signature__ = _mutmut_signature(
        xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_orig
    )
    xǁQualityAnalyzerǁ_calculate_false_negative_rate__mutmut_orig.__name__ = (
        "xǁQualityAnalyzerǁ_calculate_false_negative_rate"
    )

    def xǁQualityAnalyzerǁgenerate_report__mutmut_orig(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_1(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is not None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_2(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = None
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_3(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(None):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_4(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_5(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = None
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_6(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = None

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_7(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_8(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "XXNo analysis results available.XX"

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_9(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "no analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_10(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "NO ANALYSIS RESULTS AVAILABLE."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_11(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = None

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_12(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "XXFile Operation Detection Quality ReportXX",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_13(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "file operation detection quality report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_14(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "FILE OPERATION DETECTION QUALITY REPORT",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_15(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" / 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_16(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "XX=XX" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_17(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 46,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_18(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime(None)}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_19(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('XX%Y-%m-%d %H:%M:%SXX')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_20(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%y-%m-%d %h:%m:%s')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_21(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%M-%D %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_22(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "XXXX",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_23(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "XXMetrics:XX",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_24(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_25(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "METRICS:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_26(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(None)

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_27(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace(None, ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_28(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', None).title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_29(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace(' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_30(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_31(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('XX_XX', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_32(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', 'XX XX').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_33(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY or "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_34(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric != AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_35(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "XXpercentageXX" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_36(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "PERCENTAGE" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_37(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" not in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_38(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(None)
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_39(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['XXpercentageXX']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_40(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['PERCENTAGE']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_41(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME or "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_42(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric != AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_43(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "XXaverage_msXX" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_44(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "AVERAGE_MS" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_45(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" not in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_46(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(None)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_47(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['XXaverage_msXX']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_48(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['AVERAGE_MS']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_49(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get(None, 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_50(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', None):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_51(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get(0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_52(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms'):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_53(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('XXp95_msXX', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_54(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('P95_MS', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_55(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 1):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_56(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION or "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_57(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric != AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_58(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "XXby_typeXX" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_59(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "BY_TYPE" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_60(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" not in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_61(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append(None)
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_62(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("XX    By operation type:XX")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_63(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    by operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_64(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    BY OPERATION TYPE:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_65(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["XXby_typeXX"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_66(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["BY_TYPE"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_67(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(None)

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_68(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(
                        f"      {op_type}: {stats['XXaverageXX']:.3f} (count: {stats['count']})"
                    )

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_69(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['AVERAGE']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_70(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(
                        f"      {op_type}: {stats['average']:.3f} (count: {stats['XXcountXX']})"
                    )

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_71(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['COUNT']})")

        return "\n".join(report_lines)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_72(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(None)

    def xǁQualityAnalyzerǁgenerate_report__mutmut_73(
        self, results: dict[AnalysisMetric, QualityResult] | None = None
    ) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "XX\nXX".join(report_lines)

    xǁQualityAnalyzerǁgenerate_report__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁQualityAnalyzerǁgenerate_report__mutmut_1": xǁQualityAnalyzerǁgenerate_report__mutmut_1,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_2": xǁQualityAnalyzerǁgenerate_report__mutmut_2,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_3": xǁQualityAnalyzerǁgenerate_report__mutmut_3,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_4": xǁQualityAnalyzerǁgenerate_report__mutmut_4,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_5": xǁQualityAnalyzerǁgenerate_report__mutmut_5,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_6": xǁQualityAnalyzerǁgenerate_report__mutmut_6,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_7": xǁQualityAnalyzerǁgenerate_report__mutmut_7,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_8": xǁQualityAnalyzerǁgenerate_report__mutmut_8,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_9": xǁQualityAnalyzerǁgenerate_report__mutmut_9,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_10": xǁQualityAnalyzerǁgenerate_report__mutmut_10,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_11": xǁQualityAnalyzerǁgenerate_report__mutmut_11,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_12": xǁQualityAnalyzerǁgenerate_report__mutmut_12,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_13": xǁQualityAnalyzerǁgenerate_report__mutmut_13,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_14": xǁQualityAnalyzerǁgenerate_report__mutmut_14,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_15": xǁQualityAnalyzerǁgenerate_report__mutmut_15,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_16": xǁQualityAnalyzerǁgenerate_report__mutmut_16,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_17": xǁQualityAnalyzerǁgenerate_report__mutmut_17,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_18": xǁQualityAnalyzerǁgenerate_report__mutmut_18,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_19": xǁQualityAnalyzerǁgenerate_report__mutmut_19,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_20": xǁQualityAnalyzerǁgenerate_report__mutmut_20,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_21": xǁQualityAnalyzerǁgenerate_report__mutmut_21,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_22": xǁQualityAnalyzerǁgenerate_report__mutmut_22,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_23": xǁQualityAnalyzerǁgenerate_report__mutmut_23,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_24": xǁQualityAnalyzerǁgenerate_report__mutmut_24,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_25": xǁQualityAnalyzerǁgenerate_report__mutmut_25,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_26": xǁQualityAnalyzerǁgenerate_report__mutmut_26,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_27": xǁQualityAnalyzerǁgenerate_report__mutmut_27,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_28": xǁQualityAnalyzerǁgenerate_report__mutmut_28,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_29": xǁQualityAnalyzerǁgenerate_report__mutmut_29,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_30": xǁQualityAnalyzerǁgenerate_report__mutmut_30,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_31": xǁQualityAnalyzerǁgenerate_report__mutmut_31,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_32": xǁQualityAnalyzerǁgenerate_report__mutmut_32,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_33": xǁQualityAnalyzerǁgenerate_report__mutmut_33,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_34": xǁQualityAnalyzerǁgenerate_report__mutmut_34,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_35": xǁQualityAnalyzerǁgenerate_report__mutmut_35,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_36": xǁQualityAnalyzerǁgenerate_report__mutmut_36,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_37": xǁQualityAnalyzerǁgenerate_report__mutmut_37,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_38": xǁQualityAnalyzerǁgenerate_report__mutmut_38,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_39": xǁQualityAnalyzerǁgenerate_report__mutmut_39,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_40": xǁQualityAnalyzerǁgenerate_report__mutmut_40,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_41": xǁQualityAnalyzerǁgenerate_report__mutmut_41,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_42": xǁQualityAnalyzerǁgenerate_report__mutmut_42,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_43": xǁQualityAnalyzerǁgenerate_report__mutmut_43,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_44": xǁQualityAnalyzerǁgenerate_report__mutmut_44,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_45": xǁQualityAnalyzerǁgenerate_report__mutmut_45,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_46": xǁQualityAnalyzerǁgenerate_report__mutmut_46,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_47": xǁQualityAnalyzerǁgenerate_report__mutmut_47,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_48": xǁQualityAnalyzerǁgenerate_report__mutmut_48,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_49": xǁQualityAnalyzerǁgenerate_report__mutmut_49,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_50": xǁQualityAnalyzerǁgenerate_report__mutmut_50,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_51": xǁQualityAnalyzerǁgenerate_report__mutmut_51,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_52": xǁQualityAnalyzerǁgenerate_report__mutmut_52,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_53": xǁQualityAnalyzerǁgenerate_report__mutmut_53,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_54": xǁQualityAnalyzerǁgenerate_report__mutmut_54,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_55": xǁQualityAnalyzerǁgenerate_report__mutmut_55,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_56": xǁQualityAnalyzerǁgenerate_report__mutmut_56,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_57": xǁQualityAnalyzerǁgenerate_report__mutmut_57,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_58": xǁQualityAnalyzerǁgenerate_report__mutmut_58,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_59": xǁQualityAnalyzerǁgenerate_report__mutmut_59,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_60": xǁQualityAnalyzerǁgenerate_report__mutmut_60,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_61": xǁQualityAnalyzerǁgenerate_report__mutmut_61,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_62": xǁQualityAnalyzerǁgenerate_report__mutmut_62,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_63": xǁQualityAnalyzerǁgenerate_report__mutmut_63,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_64": xǁQualityAnalyzerǁgenerate_report__mutmut_64,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_65": xǁQualityAnalyzerǁgenerate_report__mutmut_65,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_66": xǁQualityAnalyzerǁgenerate_report__mutmut_66,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_67": xǁQualityAnalyzerǁgenerate_report__mutmut_67,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_68": xǁQualityAnalyzerǁgenerate_report__mutmut_68,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_69": xǁQualityAnalyzerǁgenerate_report__mutmut_69,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_70": xǁQualityAnalyzerǁgenerate_report__mutmut_70,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_71": xǁQualityAnalyzerǁgenerate_report__mutmut_71,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_72": xǁQualityAnalyzerǁgenerate_report__mutmut_72,
        "xǁQualityAnalyzerǁgenerate_report__mutmut_73": xǁQualityAnalyzerǁgenerate_report__mutmut_73,
    }

    def generate_report(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁQualityAnalyzerǁgenerate_report__mutmut_orig"),
            object.__getattribute__(self, "xǁQualityAnalyzerǁgenerate_report__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    generate_report.__signature__ = _mutmut_signature(xǁQualityAnalyzerǁgenerate_report__mutmut_orig)
    xǁQualityAnalyzerǁgenerate_report__mutmut_orig.__name__ = "xǁQualityAnalyzerǁgenerate_report"


# <3 🧱🤝📄🪄
