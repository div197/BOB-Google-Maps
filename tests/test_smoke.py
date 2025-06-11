def test_import_and_version():
    import bob_core

    assert hasattr(bob_core, "__version__")
    assert bob_core.__version__ == "0.3.0" 