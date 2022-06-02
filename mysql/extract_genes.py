#!/usr/bin/python3

def first_pass():
    added = set()
    with open('Hsalinarum-gene-annotation-pfeiffer2019-adjusted-names.gff3') as infile:
        header = infile.readline()
        out_dict = {}
        for line in infile:
            chrom, l1, typ, start, stop, l2, strand, l3, desc = line.strip().split('\t')
            comps = desc.split(';')
            if typ == 'gene':
                gene = None
                locus_tag = None
                for c in comps:
                    try:
                        """
                        if c.startswith('Name=ID'):
                            c = c.replace('Name=ID', 'Name')
                        """
                        key, value = c.split('=')
                        if key == 'gene':
                            gene = value
                        if key == 'locus_tag':
                            locus_tag = value
                    except:
                        pass

                    if gene is not None and locus_tag is not None:
                        key = '%s:%s' % (gene, locus_tag)
                        out_dict[key] = (gene, locus_tag, chrom, start, stop, strand)
                        added.add(gene)
                        added.add(locus_tag)
    return out_dict, added

def second_pass(out_dict, added):
    with open('Hsalinarum-gene-annotation-pfeiffer2019-adjusted-names.gff3') as infile:
        header = infile.readline()
        for line in infile:
            chrom, l1, typ, start, stop, l2, strand, l3, desc = line.strip().split('\t')
            comps = desc.split(';')
            if typ == 'gene':
                gene = None
                locus_tag = None
                for c in comps:
                    try:
                        """
                        if c.startswith('Name=ID'):
                            c = c.replace('Name=ID', 'Name')
                        """
                        key, value = c.split('=')
                        if key == 'gene':
                            gene = value
                        if key == 'locus_tag':
                            locus_tag = value
                    except:
                        pass

                    if gene is None and locus_tag is not None:
                        # we can otherwise not add this gene like VNG_0051a
                        key = locus_tag
                        gene = locus_tag
                        if not gene in added:
                            print("skipped: ", gene)
                            out_dict[key] = (gene, locus_tag, chrom, start, stop, strand)
                    """
                    elif gene is not None and locus_tag is None:
                        key = gene
                        locus_tag = ''

                    if key is not None:
                        # sometimes the key ends with colon, that means the locus tag is not None, but
                        # empty '', the equivalent of None, which might lead to double entries
                        if key.endswith(':'):
                            key = key[:-1]
                        out_dict[key] = (gene, locus_tag, chrom, start, stop, strand)
                    """
    return out_dict

#print(out_dict.keys())
# step 2: add a quality control step:
# genes can occur twice, the ones that have a locus tag and those that don't
# we need to favor the ones that have a locus tag that is different from the
# gene
# TODO

if __name__ == '__main__':
    out_dict, added = first_pass()
    out_dict = second_pass(out_dict, added)

    with open('genes.tsv', 'w') as outfile:
        for key, value in out_dict.items():
            gene, locus_tag, chrom, start, stop, strand = value
            outfile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (gene, locus_tag, chrom,
                                              start, stop, strand))
