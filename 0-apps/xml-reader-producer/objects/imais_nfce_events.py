import xml.etree.ElementTree as ET
import xmltodict
import json
from dotenv import load_dotenv

load_dotenv()


class NFCeEvents(object):
    """
    Class for dividing the event into different streams to facilitate data processing.

    When sending an XML to your builder it is possible to split NF-e by issuer,
    recipient, items etc.

    ...

    Parameters
    -------
    xml: str
        XML containing the NF-e.

    """

    def __init__(self, xml):
        """Creates a Event object

        ...

        Parameters
        -------
        xml: str
            XML containing the NF-e.

        """
        self.xml_file = xml
        # parsing xml and creating object
        tree = ET.ElementTree(ET.fromstring(xml))
        # finding root element
        xml_data = tree.getroot()

        # converting to string using [utf-8]
        xml_to_str = ET.tostring(xml_data, encoding="utf-8", method="xml")

        # converting string to dictionary
        data_dict = dict(xmltodict.parse(xml_to_str))
        get_nfe = data_dict["NFe"]

        # available parameter across the class
        # get key of stream [get id inside of every nfe]
        self.root_nfe = get_nfe
        get_key = get_nfe["infNFe"]["@Id"]
        self.key = get_key
        self.formatted_key = {"key": self.key}

    def xml2json(self):
        """Converts the XML received on the builder in a JSON."""

        # [json] format conversion
        xml2json = json.dumps(self.root_cfe)

        # return in json format
        return xml2json

    def get_nfe_key(self):
        """Returns the CF-E key."""
        return self.key

    def get_nfe_ide(self):
        """Returns NF-E identification information group."""
        return self.root_nfe["infNFe"]["ide"]

    def get_nfe_emit(self):
        """Returns NF-e issuer identification group."""
        return self.root_nfe["infNFe"]["emit"]

    def get_nfe_det(self):
        """Returns TAG det of NF-e."""
        return self.root_nfe["infNfe"]["det"]

    def get_nfe_total(self):
        """Returns TAG Total of NF-e."""
        return self.root_nfe["infNfe"]["total"]

    def get_nfe_transp(self):
        """Returns TAG transp of NF-e."""
        return self.root_nfe["infNfe"]["transp"]

    def get_nfe_pag(self):
        """Returns TAG pag of NF-e."""
        return self.root_nfe["infNfe"]["pag"]

    def get_nfe_infAdic(self):
        """Returns TAG infAdic of NF-e."""
        return self.root_nfe["infNfe"]["infAdic"]