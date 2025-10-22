#!/bin/bash
# Split the remaining oversized test files

# File 1: test_file_quality_qualityanalyzer.py (557 LOC)
# Split into 2 files at line 223 (first 10 tests vs last 9 tests)

head -223 tests/file/test_file_quality_qualityanalyzer.py > tests/file/test_file_quality_analyzer_basic.py
echo "" >> tests/file/test_file_quality_analyzer_basic.py

# Create second file with header + remaining tests
head -27 tests/file/test_file_quality_qualityanalyzer.py > tests/file/test_file_quality_analyzer_metrics.py
tail -n +224 tests/file/test_file_quality_qualityanalyzer.py >> tests/file/test_file_quality_analyzer_metrics.py

# Remove original
rm tests/file/test_file_quality_qualityanalyzer.py

# File 2: test_transport/test_client.py - This needs special handling
# We'll leave it for manual review since it doesn't follow standard patterns

echo "Split complete. Now formatting..."

# Format the new files
ruff check --fix --unsafe-fixes tests/file/test_file_quality_analyzer_*.py
ruff format tests/file/test_file_quality_analyzer_*.py

echo "Done!"
