from artificial_life import main


def test_package_entrypoint_prints_greeting(capsys):
    main()

    assert "Hello from artificial-life!" in capsys.readouterr().out
