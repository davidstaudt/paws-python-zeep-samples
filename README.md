# paws-python-zeep-samples

## Overview

Samples demonstrating how to use the Python Zeep SOAP library to manage Cisco Unified Communications Voice Operating System (VOS) nodes with the Platform Adminstration Web Service (PAWS).

https://developer.cisco.com/site/paws

## Available samples

* `paws_getAPIVersion.py` - Retrieves the current version of the PAWS API service from the VOS
node. ( `<getAPIVersion>`).

* `paws_getMyClusterNode.py` - Retrieves details about the VOS cluster node to which the PAWS request
is made. ( `<getMyClusterNode>`).

## Getting started

* Install Python 3

    On Windows, choose the option to add to PATH environment variable

* If installing on Linux, you may need to install dependencies for `python3-lxml`, see [Installing lxml](https://lxml.de/3.3/installation.html)

  E.g. for Debian/Ubuntu:

  ```bash
  sudo apt build-dep python3-lxml
  ```    

* (Optional) Create/activate a Python virtual environment named `venv`:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* Install needed dependency packages:

    ```bash
    pip install -r requirements.txt
    ```

* Rename `.env.example` to `.env`, and edit it to specify your VOS host address, version, and PAWS user credentials.

* PAWS v15 WSDL files are included in this project.  If you'd like to use a different version, replace with the PAWS WSDL files for your VOS product version.  

  These can be downloaded from the VOS host at:

  ```
  https://<server>/platform-services/services/<Service Name>?wsdl
  ```

* To run a specific sample, in Visual Studio Code open the sample `.py` file you want to run, then press `F5`, or open the Debugging panel and click the green 'Launch' arrow.

## Hints

* You can get a 'dump' of a specific service WSDL to see how Zeep interprets it by running, for example (Mac/Linux):

    ```bash
    python3 -mzeep schema/15/APIVersionService.wsdl > APIVersionService_wsdl.txt
    ```

    This can help with identifying the proper object structure to send to Zeep (see [example](schema_docs/15/APIVersionService_wsdl.txt)).

* Elements which contain a list, such as:

    ```xml
    <members>
        <member>
            <subElement1/>
            <subElement2/>
        </member>
        <member>
            <subElement1/>
            <subElement2/>
        </member>
    </members>
    ```

    are represented a little differently by Zeep than might be expected: note that `<member>` becomes an array, not `<members>`:

    ```python
    {
        'members': {
            'member': [
                {
                    'subElement1': 'value',
                    'subElement2': 'value'
                },
                {
                    'subElement1': 'value',
                    'subElement2': 'value'
                }
            ]
        }
    }
    ```

* Zeep expects elements with attributes and values to be constructed as below:

    To generate this XML...

    ```xml
    <startChangeId queueId='foo'>bar</startChangeId>
    ```

    Define the object like this...

    ```python
    startChangeId = {
        'queueId': 'foo',
        '_value_1': 'bar'
    }
    ```
* **xsd:SkipValue** When building the XML to send to the PAWS host, Zeep may include empty elements that are part of the schema but that you didn't explicity specify.  This may result in PAWS interpreting the empty element as indication to set the value to empty/nil/null.  To force Zeep to skip including an element from the request XML, set its value to `xsd:SkipValue`:

   ```python
   updatePhoneObj = {
    "description": "New Description",
    "lines": xsd:SkipValue
   }
   ```

   Be sure to import the `xsd` module: `from zeep import xsd`

* **Requests Sessions** Creating and using a [requests Session](https://docs.python-requests.org/en/latest/user/advanced/) object [to use with Zeep](https://docs.python-zeep.org/en/master/api.html) allows setting global request parameters like `auth`/`verify`/`headers`.

    In addition, Session retains PAWS API `JSESSION` cookies to bypass expensive backend authentication checks per-request, and HTTP persistent connections to keep network latency and networking CPU usage lower.
    