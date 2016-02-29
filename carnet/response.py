from lxml import etree


def parse_tag(tag):
    if tag[0] == '{':
        # strip namespace
        ns_end = tag.index('}')
        ns = tag[1:ns_end]
        tag = tag[ns_end+1:]
    else:
        ns = None
    return ns, tag


def skip_to_children( tag):
    return tag.endswith('List') or tag in (
        'VehicleDetailes',
    )


def xml2dict(xml):
    result = {}
    nodes = list(xml)
    for node in nodes:
        ns, tag = parse_tag(node.tag)
        children = list(node)
        if children:
            if skip_to_children(tag):
                # Skip this element, add directly
                # children to the nodes to process
                nodes.extend(list(node))
                continue
            children = xml2dict(children)
            if tag not in result:
                result[tag] = children
            else:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(children)
        else:
            result[tag] = node.text
    return result


def parse_response(response):
    data = None
    status = 'ERROR'
    # Remove soap wrapping and use directly the response
    # that contains the actual result namespaces:
    root = etree.fromstring(response.content)[0][0][0]
    # print(etree.tostring(root, pretty_print=True))
    for node in root:
        if 'Data' in node.tag:
            data = xml2dict(node)
        if 'Response' in node.tag:
            status = xml2dict(node).get('ResponseStatus', 'ERROR')

    return status, data