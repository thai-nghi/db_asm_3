from cassandra.cluster import Cluster
from app.settings import settings

cluster = Cluster([settings.scylla_url])
session = cluster.connect()