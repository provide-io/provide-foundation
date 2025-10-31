#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenObserve metrics data models.

These models represent metrics data from OpenObserve's Prometheus-compatible API."""

from __future__ import annotations

from typing import Any

from attrs import define, field


@define(slots=True)
class MetricMetadata:
    """Metadata for a metric.

    Attributes:
        name: Metric name
        type: Metric type (counter, gauge, histogram, summary, etc.)
        help: Help text describing the metric
        unit: Unit of measurement
    """

    name: str
    type: str
    help: str = ""
    unit: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MetricMetadata:
        """Create from dictionary.

        Args:
            data: Dictionary with metric metadata

        Returns:
            MetricMetadata instance
        """
        return cls(
            name=data.get("name", ""),
            type=data.get("type", ""),
            help=data.get("help", ""),
            unit=data.get("unit", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "type": self.type,
            "help": self.help,
            "unit": self.unit,
        }


@define(slots=True)
class MetricSample:
    """A single metric sample with labels and value.

    Attributes:
        metric: Label name-value pairs
        value: Metric value (single value for instant queries)
        values: List of [timestamp, value] pairs for range queries
    """

    metric: dict[str, str] = field(factory=dict)
    value: tuple[float, str] | None = None  # (timestamp, value)
    values: list[tuple[float, str]] = field(factory=list)  # [(timestamp, value), ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MetricSample:
        """Create from dictionary.

        Args:
            data: Dictionary with sample data from Prometheus API

        Returns:
            MetricSample instance
        """
        metric = data.get("metric", {})
        value = data.get("value")
        values = data.get("values", [])

        # Convert value to tuple if present
        value_tuple = None
        if value and isinstance(value, list) and len(value) == 2:
            value_tuple = (float(value[0]), str(value[1]))

        # Convert values list
        values_list = []
        if values:
            for v in values:
                if isinstance(v, list) and len(v) == 2:
                    values_list.append((float(v[0]), str(v[1])))

        return cls(
            metric=metric,
            value=value_tuple,
            values=values_list,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        result: dict[str, Any] = {"metric": self.metric}

        if self.value:
            result["value"] = list(self.value)

        if self.values:
            result["values"] = [list(v) for v in self.values]

        return result


@define(slots=True)
class MetricQueryResult:
    """Result from a Prometheus query.

    Attributes:
        result_type: Type of result (vector, matrix, scalar, string)
        result: List of metric samples
        status: Query status (success, error)
        error_type: Error type if query failed
        error: Error message if query failed
        warnings: List of warnings
    """

    result_type: str
    result: list[MetricSample] = field(factory=list)
    status: str = "success"
    error_type: str = ""
    error: str = ""
    warnings: list[str] = field(factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MetricQueryResult:
        """Create from dictionary.

        Args:
            data: Dictionary with query result from Prometheus API

        Returns:
            MetricQueryResult instance
        """
        # Handle OpenObserve/Prometheus API response format
        if "data" in data:
            data_section = data["data"]
            status = data.get("status", "success")
            warnings = data.get("warnings", [])
            error_type = data.get("errorType", "")
            error = data.get("error", "")

            result_type = data_section.get("resultType", "")
            result_data = data_section.get("result", [])

            samples = [MetricSample.from_dict(sample) for sample in result_data]

            return cls(
                result_type=result_type,
                result=samples,
                status=status,
                error_type=error_type,
                error=error,
                warnings=warnings,
            )

        # Fallback for other formats (e.g., error responses without data section)
        return cls(
            result_type=data.get("resultType", ""),
            result=[],
            status=data.get("status", "success"),
            error_type=data.get("errorType", ""),
            error=data.get("error", ""),
            warnings=data.get("warnings", []),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        result: dict[str, Any] = {
            "status": self.status,
            "data": {
                "resultType": self.result_type,
                "result": [sample.to_dict() for sample in self.result],
            },
        }

        if self.warnings:
            result["warnings"] = self.warnings

        if self.error:
            result["errorType"] = self.error_type
            result["error"] = self.error

        return result

    @property
    def is_success(self) -> bool:
        """Check if query was successful.

        Returns:
            True if status is "success"
        """
        return self.status == "success"

    @property
    def sample_count(self) -> int:
        """Get number of metric samples.

        Returns:
            Number of samples in result
        """
        return len(self.result)


@define(slots=True)
class MetricLabels:
    """Label names and values for a metric.

    Attributes:
        label_names: List of label names
        label_values: Dictionary mapping label names to list of values
    """

    label_names: list[str] = field(factory=list)
    label_values: dict[str, list[str]] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MetricLabels:
        """Create from dictionary.

        Args:
            data: Dictionary with label information

        Returns:
            MetricLabels instance
        """
        return cls(
            label_names=data.get("label_names", []),
            label_values=data.get("label_values", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "label_names": self.label_names,
            "label_values": self.label_values,
        }


# 🧱🏗️🔚
