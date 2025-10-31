#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Formatters for OpenObserve metrics output.

Provides various output formats for metrics data including tables, JSON, CSV,
ASCII charts, and statistical summaries."""

from __future__ import annotations

import json
from typing import Any

from provide.foundation.integrations.openobserve.metrics_models import (
    MetricQueryResult,
)


def format_metrics_list(metrics: list[str], show_count: bool = True) -> str:
    """Format list of metrics as a simple list.

    Args:
        metrics: List of metric names
        show_count: Whether to show count at the end

    Returns:
        Formatted string
    """
    if not metrics:
        return "No metrics found."

    lines = []
    for metric in sorted(metrics):
        lines.append(f"  {metric}")

    output = "\n".join(lines)

    if show_count:
        output += f"\n\nTotal: {len(metrics)} metrics"

    return output


def format_metric_metadata(metadata: dict[str, list[dict[str, Any]]]) -> str:
    """Format metric metadata as a table.

    Args:
        metadata: Dictionary mapping metric names to metadata list

    Returns:
        Formatted string
    """
    if not metadata:
        return "No metadata found."

    lines = []
    for metric_name, meta_list in sorted(metadata.items()):
        lines.append(f"\n{metric_name}:")
        for meta in meta_list:
            metric_type = meta.get("type", "unknown")
            help_text = meta.get("help", "")
            unit = meta.get("unit", "")

            lines.append(f"  Type: {metric_type}")
            if help_text:
                lines.append(f"  Help: {help_text}")
            if unit:
                lines.append(f"  Unit: {unit}")

    return "\n".join(lines)


def format_labels(labels: list[str]) -> str:
    """Format list of labels.

    Args:
        labels: List of label names

    Returns:
        Formatted string
    """
    if not labels:
        return "No labels found."

    lines = []
    for label in sorted(labels):
        lines.append(f"  {label}")

    return "\n".join(lines) + f"\n\nTotal: {len(labels)} labels"


def format_label_values(label_name: str, values: list[str]) -> str:
    """Format label values.

    Args:
        label_name: Name of the label
        values: List of values

    Returns:
        Formatted string
    """
    if not values:
        return f"No values found for label: {label_name}"

    lines = [f"Values for label '{label_name}':"]
    for value in sorted(values):
        lines.append(f"  {value}")

    return "\n".join(lines) + f"\n\nTotal: {len(values)} values"


def _format_sample_labels(labels: dict[str, str]) -> str:
    """Format sample labels as a compact string.

    Args:
        labels: Label dictionary

    Returns:
        Formatted label string
    """
    if not labels:
        return ""

    label_pairs = [f'{k}="{v}"' for k, v in sorted(labels.items())]
    return "{" + ", ".join(label_pairs) + "}"


def format_query_result_table(result: MetricQueryResult) -> str:
    """Format query result as a table.

    Args:
        result: Query result to format

    Returns:
        Formatted table string
    """
    if not result.is_success:
        return f"Query failed: {result.error}"

    if not result.result:
        return "No data returned."

    lines = []
    lines.append("Metric                                    Labels                          Value")
    lines.append("-" * 80)

    for sample in result.result:
        # Get metric name from labels
        metric_name = sample.metric.get("__name__", "unknown")

        # Get other labels
        other_labels = {k: v for k, v in sample.metric.items() if k != "__name__"}
        labels_str = _format_sample_labels(other_labels)

        # Get value
        if sample.value:
            _timestamp, value = sample.value
            value_str = value
        elif sample.values and len(sample.values) > 0:
            # For range queries, show the latest value
            _timestamp, value = sample.values[-1]
            value_str = f"{value} (latest of {len(sample.values)} points)"
        else:
            value_str = "N/A"

        # Truncate strings if too long
        metric_name = metric_name[:40]
        labels_str = labels_str[:30]

        lines.append(f"{metric_name:<40}  {labels_str:<30}  {value_str}")

    lines.append("-" * 80)
    lines.append(f"Total: {len(result.result)} samples")

    return "\n".join(lines)


def format_query_result_json(result: MetricQueryResult, pretty: bool = False) -> str:
    """Format query result as JSON.

    Args:
        result: Query result to format
        pretty: Whether to pretty-print JSON

    Returns:
        JSON string
    """
    data = result.to_dict()

    if pretty:
        return json.dumps(data, indent=2)

    return json.dumps(data)


def format_query_result_csv(result: MetricQueryResult) -> str:
    """Format query result as CSV.

    Args:
        result: Query result to format

    Returns:
        CSV string
    """
    if not result.is_success or not result.result:
        return "metric,labels,timestamp,value\n"

    lines = ["metric,labels,timestamp,value"]

    for sample in result.result:
        metric_name = sample.metric.get("__name__", "unknown")
        labels_str = _format_sample_labels(sample.metric)

        if sample.value:
            timestamp, value = sample.value
            lines.append(f'{metric_name},"{labels_str}",{timestamp},{value}')
        elif sample.values:
            for timestamp, value in sample.values:
                lines.append(f'{metric_name},"{labels_str}",{timestamp},{value}')

    return "\n".join(lines)


def format_time_series_chart(result: MetricQueryResult, width: int = 60, height: int = 20) -> str:  # noqa: C901
    """Format time series as ASCII chart.

    Args:
        result: Query result with time series data
        width: Chart width in characters
        height: Chart height in lines

    Returns:
        ASCII chart string
    """
    if not result.is_success or not result.result:
        return "No data for chart."

    # This is a simple ASCII chart implementation
    # For production, consider using a library like asciichartpy

    lines = [f"Time Series Chart (approx {width}x{height})"]
    lines.append("=" * width)

    # Collect all values across all series
    all_values: list[float] = []
    for sample in result.result:
        if sample.values:
            for _, value_str in sample.values:
                try:
                    all_values.append(float(value_str))
                except ValueError:
                    continue

    if not all_values:
        return "No numeric values for chart."

    # Calculate min/max for scaling
    min_val = min(all_values)
    max_val = max(all_values)
    value_range = max_val - min_val if max_val != min_val else 1

    # Simple representation
    lines.append(f"Max: {max_val:.2f}")
    lines.append("|" + "-" * (width - 2) + "|")

    # Plot each series
    for sample in result.result[:5]:  # Limit to first 5 series
        if not sample.values:
            continue

        metric_name = sample.metric.get("__name__", "unknown")
        lines.append(f"{metric_name}:")

        # Simple bar chart of values
        for _timestamp, value_str in sample.values[:width]:  # Limit points to chart width
            try:
                value = float(value_str)
                # Scale to height
                bar_height = int(((value - min_val) / value_range) * (height - 4))
                bar = "#" * max(1, bar_height)
                lines.append(f"  {bar} {value:.2f}")
            except ValueError:
                continue

    lines.append("|" + "-" * (width - 2) + "|")
    lines.append(f"Min: {min_val:.2f}")
    lines.append("=" * width)

    return "\n".join(lines)


def format_metric_summary(result: MetricQueryResult) -> str:  # noqa: C901
    """Format query result as statistical summary.

    Args:
        result: Query result to summarize

    Returns:
        Summary string with statistics
    """
    if not result.is_success:
        return f"Query failed: {result.error}"

    if not result.result:
        return "No data returned."

    # Collect all numeric values
    all_values: list[float] = []
    for sample in result.result:
        if sample.value:
            _, value_str = sample.value
            try:
                all_values.append(float(value_str))
            except ValueError:
                continue
        elif sample.values:
            for _, value_str in sample.values:
                try:
                    all_values.append(float(value_str))
                except ValueError:
                    continue

    if not all_values:
        return "No numeric values to summarize."

    # Calculate statistics
    count = len(all_values)
    total = sum(all_values)
    avg = total / count
    min_val = min(all_values)
    max_val = max(all_values)

    # Calculate median
    sorted_values = sorted(all_values)
    mid = count // 2
    median = (sorted_values[mid - 1] + sorted_values[mid]) / 2 if count % 2 == 0 else sorted_values[mid]

    lines = [
        "Metric Summary:",
        f"  Samples: {count}",
        f"  Min:     {min_val:.4f}",
        f"  Max:     {max_val:.4f}",
        f"  Average: {avg:.4f}",
        f"  Median:  {median:.4f}",
        f"  Total:   {total:.4f}",
    ]

    # Show series count
    if result.result:
        lines.append(f"  Series:  {len(result.result)}")

    return "\n".join(lines)


def format_metric_output(
    result: MetricQueryResult | list[str] | dict[str, Any],
    format_type: str = "table",
    pretty: bool = False,
) -> str:
    """Format metrics output in specified format.

    Args:
        result: Data to format (query result, list of metrics, or metadata)
        format_type: Output format ("table", "json", "csv", "chart", "summary")
        pretty: Whether to pretty-print (for JSON)

    Returns:
        Formatted string
    """
    # Handle different input types
    if isinstance(result, list):
        # List of metric names
        return format_metrics_list(result)

    if isinstance(result, dict) and not isinstance(result, MetricQueryResult):
        # Metadata dictionary
        return format_metric_metadata(result)

    if not isinstance(result, MetricQueryResult):
        return str(result)

    # Format query result based on type
    if format_type == "json":
        return format_query_result_json(result, pretty=pretty)
    if format_type == "csv":
        return format_query_result_csv(result)
    if format_type == "chart":
        return format_time_series_chart(result)
    if format_type == "summary":
        return format_metric_summary(result)

    # Default to table
    return format_query_result_table(result)


# 🧱🏗️🔚
