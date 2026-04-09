from simple_print import spprint


def test_spprint():
    """Test spprint.

    Run:
        pytest tests/test_spprint.py -s

    """

    spprint({"hello":"world", "lorem": "ipsum"}, i=20)
    spprint({"hello":"world", "lorem": "ipsum"}, i=0)
    spprint({"hello":"world", "lorem": "ipsum"})
    spprint({"key": "value"})
    spprint({"nested": {"a": 1, "b": 2}}, i=10)
    spprint({})
    spprint({"a": 1, "b": 2, "c": 3, "d": 4, "e": 5})

    spprint({
        "users": [
            {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "roles": ["admin", "editor"],
                "settings": {
                    "theme": "dark",
                    "language": "en",
                    "notifications": {"email": True, "sms": False, "push": True},
                },
            },
            {
                "id": 2,
                "name": "Bob",
                "email": "bob@example.com",
                "roles": ["viewer"],
                "settings": {
                    "theme": "light",
                    "language": "fr",
                    "notifications": {"email": False, "sms": False, "push": False},
                },
            },
        ],
        "metadata": {
            "total": 2,
            "page": 1,
            "per_page": 10,
            "filters": {"active": True, "verified": True, "region": "EU"},
        },
        "api_version": "2.1.0",
    })