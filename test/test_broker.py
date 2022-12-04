from simple_print import throw, catch

def test_broker(): 

    uri = "amqp://admin:admin@5.187.4.179:55672/vhost"
    msg = {
        "hello": "world"
    }

    throw({"msg": msg}, uri=uri)
    catch(console=True, uri=uri)

