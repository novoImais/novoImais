import xml.etree.ElementTree as ET
import xmltodict
import json
from dotenv import load_dotenv

load_dotenv()


class Events(object):
    """
    Class for dividing the event into different streams to facilitate data processing.

    When sending an XML to your builder it is possible to split CF-e by issuer,
    recipient, items etc.

    ...

    Parameters
    -------
    xml: str
        XML containing the CF-e.

    """

    def __init__(self, xml):
        """Creates a Event object

        ...

        Parameters
        -------
        xml: str
            XML containing the CF-e.

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
        get_cfe = data_dict["CFe"]

        # available parameter across the class
        # get key of stream [get id inside of every nfe]
        self.root_cfe = get_cfe
        get_key = get_cfe["infCFe"]["@Id"]
        self.key = get_key
        self.formatted_key = {"key": self.key}

    def xml2json(self):
        """Converts the XML received on the builder in a JSON."""

        # [json] format conversion
        xml2json = json.dumps(self.root_cfe)

        # return in json format
        return xml2json

    def get_key(self):
        """Returns the CF-E key."""
        return self.key

    def get_ide(self):
        """Returns CF-E identification information group."""
        return self.root_cfe["infCFe"]["ide"]

    def get_emit(self):
        """Returns CF-e issuer identification group."""
        return self.root_cfe["infCFe"]["emit"]

    def get_dest(self):
        """Returns identification group of the recipient of the CF-e."""
        return self.root_cfe["infCFe"]["dest"]

    def get_det(self):
        """Returns Products and Services detailing group of CF-e."""
        return self.root_cfe["infCFe"]["det"]

    def get_total(self):
        """Returns CF-e Total Values Group."""
        return self.root_cfe["infCFe"]["total"]

    def get_pgto(self):
        """Returns CFe Payment Information Group."""
        return self.root_cfe["infCFe"]["pgto"]

    def get_inf_adic(self):
        """Returns Additional Information Group."""
        return self.root_cfe["infCFe"]["infAdic"]
