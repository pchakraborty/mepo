def valid_components(specified_comp_names, allcomps):
    allnames = [x.name for x in allcomps]
    for compname in specified_comp_names:
        if compname not in allnames:
            raise Exception('Unknown component name [{}]'.format(compname))
