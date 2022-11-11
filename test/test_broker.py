from simple_print import throw, catch

def test_broker(): 

    uri = "amqp://admin:pass@0.0.0.0:5672/vhost"

    msg = {
        "hello": "world"
    }
    throw({"msg": msg}, uri=uri)
    catch(console=True, uri=uri)

    print(throw.__doc__)
    print(catch.__doc__)