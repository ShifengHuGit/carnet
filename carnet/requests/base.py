from lxml import etree


class BaseRequest(object):

    def __init__(self, endpoint, template, params):
        self.endpoint = endpoint
        self.template = template
        self.params = params

    def render(self, transaction_id):
        xml = etree.fromstring(self.template)

        # Replace transaction ID
        if 'v12' in xml.nsmap:
            self.replace_single(xml, 'v12:TransactionId', transaction_id)
        else:
            self.replace_single(xml, 'v11:TransactionId', transaction_id)

        # Replace params
        for k, v in self.params.items():
            self.replace_single(xml, k, v)
        return etree.tostring(xml)

    def replace_single(self, xml, tag, replacement):
        elements = xml.xpath('.//{}'.format(tag), namespaces=xml.nsmap)
        if len(elements) != 1:
            raise Exception(
                'Error in tag to replace: {}. Found {} tags'.format(
                    tag, len(elements)
                )
            )
        elements[0].text = replacement
