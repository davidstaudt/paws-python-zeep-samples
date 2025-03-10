"""PAWS <getMyClusterNode> sample script, using the Zeep SOAP library.

Retrieves details about the VOS cluster node to which the PAWS request
is made.

"""

from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth
import sys
import urllib3

from zeep import Client, Settings, Plugin
from zeep.transports import Transport
from zeep.exceptions import Fault

# Edit .env file to specify your VoS server and PAWS user details
import os
from dotenv import load_dotenv

load_dotenv()

# Change to True to enable output of request/response headers and XML
DEBUG = os.getenv("DEBUG")

# Path to find required PAWS WSDL files
WSDL_PATH = f"schema/{os.getenv('VOS_VERSION')}/"

# This class lets you view the incoming and outgoing http headers and XML


class MyLoggingPlugin(Plugin):
    def egress(self, envelope, http_headers, operation, binding_options):
        # Format the request body as pretty printed XML
        xml = etree.tostring(envelope, pretty_print=True, encoding="unicode")

        print(f"\nRequest\n-------\nHeaders:\n{http_headers}\n\nBody:\n{xml}")

    def ingress(self, envelope, http_headers, operation):
        # Format the response body as pretty printed XML
        xml = etree.tostring(envelope, pretty_print=True, encoding="unicode")

        print(f"\nResponse\n-------\nHeaders:\n{http_headers}\n\nBody:\n{xml}")


# The first step is to create a SOAP client session
session = Session()

# We avoid certificate verification by default
# And disable insecure request warnings to keep the output clear
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# To enable SSL cert checking (recommended for production)
# place the VOS host's Tomcat cert .pem file in the root of the project
# and uncomment the two lines below

# CERT = 'changeme.pem'
# session.verify = CERT

session.auth = HTTPBasicAuth(os.getenv("PAWS_USERNAME"), os.getenv("PAWS_PASSWORD"))

transport = Transport(session=session, timeout=10)

# strict=False is not always necessary, but it allows Zeep to parse imperfect XML
settings = Settings(strict=False, xml_huge_tree=True)

# If debug output is requested, add the MyLoggingPlugin callback
plugin = [MyLoggingPlugin()] if DEBUG else []

# Create the Zeep client with the specified settings
ClusterNodesServiceClient = Client(
    f"{WSDL_PATH}/ClusterNodesService.wsdl",
    settings=settings,
    transport=transport,
    plugins=plugin,
)

# Create the Zeep service binding to PAWS at the specified VOS host
ClusterNodesService = ClusterNodesServiceClient.create_service(
    "{http://services.api.platform.vos.cisco.com}ClusterNodesServiceSoap11Binding",
    f'https://{os.getenv("VOS_ADDRESS")}/platform-services/services/ClusterNodesService.ClusterNodesServiceHttpsSoap11Endpoint/',
)

node = ClusterNodesServiceClient.create_message(ClusterNodesService, "getMyClusterNode")

# Execute the getAPIVersion request
try:
    resp = ClusterNodesService.getMyClusterNode()
except Exception as err:
    print(f"\nZeep error: getMyClusterNode: { err }")
    sys.exit(1)

print(f"\nMy Cluster Node: {resp.clusterNodes[0]}")
