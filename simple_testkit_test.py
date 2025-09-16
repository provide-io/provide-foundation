from provide.testkit import temp_directory

def test_simple_testkit_usage(temp_directory):
    """Simple test using testkit to trigger header/footer."""
    test_file = temp_directory / "test.txt"
    test_file.write_text("Hello from foundation!")
    assert test_file.read_text() == "Hello from foundation!"

