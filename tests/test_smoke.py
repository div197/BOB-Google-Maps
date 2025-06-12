import bob_core

def test_import_and_version():
    assert hasattr(bob_core, "__version__")
    assert bob_core.__version__ == "0.5.0" 