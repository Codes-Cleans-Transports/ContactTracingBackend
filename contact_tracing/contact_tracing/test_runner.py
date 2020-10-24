from time import sleep
from subprocess import call

from django.test.runner import DiscoverRunner


class MyTestRunner(DiscoverRunner):
    def setup_databases(self, *args, **kwargs):
        # Stop your development instance
        call("sudo service neo4j-service stop", shell=True)
        # Sleep to ensure the service has completely stopped
        sleep(1)
        # Start your test instance (see section below for more details)
        success = call("neo4j"
                       " start-no-wait", shell=True)
        # Need to sleep to wait for the test instance to completely come up
        sleep(10)
        if success != 0:
            return False
        try:
            # For neo4j 2.2.x you'll need to set a password or deactivate auth
            # Nigel Small's py2neo gives us an easy way to accomplish this
            call("source /path/to/virtualenv/bin/activate && "
                 "/path/to/virtualenv/bin/neoauth "
                 "neo4j neo4j my-p4ssword")
        except OSError:
            pass
        # Don't import neomodel until we get here because we need to wait 
        # for the new db to be spawned
        from neomodel import db
        # Delete all previous entries in the db prior to running tests
        query = "match (n)-[r]-() delete n,r"
        db.cypher_query(query)
        super(MyTestRunner, self).__init__(*args, **kwargs)

    def teardown_databases(self, old_config, **kwargs):
        from neomodel import db
        # Delete all previous entries in the db after running tests
        query = "match (n)-[r]-() delete n,r"
        db.cypher_query(query)
        sleep(1)
        # Shut down test neo4j instance
        success = call("/path/to/test/db/neo4j-community-2.2.2/bin/neo4j"
                       " stop", shell=True)
        if success != 0:
            return False
        sleep(1)
        # start back up development instance
        call("sudo service neo4j-service start", shell=True)