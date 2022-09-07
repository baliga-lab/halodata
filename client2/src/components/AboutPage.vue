<template>
  <v-container>
    <v-row style="margin: auto; width: 80%">
      <v-col class="mb-4">
        <h2>Table of contents</h2>
        <ul>
          <li><a href="#introduction">Introduction</a></li>
          <li>
            <a href="#portaldesc">Portal Description</a>
            <ul>
              <li><a href="#pd-home">Home</a></li>
              <li><a href="#pd-atlas">Atlas</a></li>
            </ul>
          </li>
          <li>
            <a href="#usage-examples">Usage Examples</a>
            <ul>
              <li><a href="#ue-selectgene">Selecting a gene to open in the genome browser</a></li>
              <li><a href="#ue-browsemobilome">Browsing the mobilome cluster using the interactive heat map</a></li>
              <li><a href="#ue-intheatmapsearch">Using the interactive heatmap search tool</a></li>
              <li><a href="#ue-downloaddata">Downloading data for the gvp gene cluster demonstrated above</a></li>
            </ul>
          </li>
          <li><a href="#download">Data download</a></li>
          <li><a href="#citation">Citation</a></li>
          <li><a href="#support">Bugs and feature requests</a></li>
          <li><a href="#funding">Funding</a></li>
          <li><a href="#team">Team</a></li>
        </ul>
        <hr class="section-sep" />

        <h2 id="introduction">Introduction</h2>
        <p>
          The <i>H. salinarum</i> NRC-1 Atlas is a web resource conceived to support the discovery of potential post-transcriptional regulation mechanisms by observing multi-omics data of a growth curve experiment and miscellaneous features obtained from public data. It debuted as a companion web portal for the manuscript entitled <i>"A genome-scale atlas reveals complex interplay of transcription and translation in an archaeon"</i> (Lorenzetti et al., 2022). Below, we describe each section of this web portal.
        </p>
        <h2 id="portaldesc">Portal description</h2>
        <h3 id="pd-home">Home</h3>
        <p>
          The landing page for this web portal shows three searchable tables that can be activated by clicking on their respective tabs:
        </p>
        <ul>
          <li>
            <b>Locus tag:</b> This table brings an index of the genes you can browse. Each row starts with a non-redundant representative open reading frame (column #1) followed by its symbol (column #2), its protein product (column #3), and a list of locus tags corresponding to (quasi)identical genes within the same annotation effort or coming from other resources (e.g., strain R1). If you need more details on how this non-redundant set of genes was generated, please, refer to <a href="https://github.com/alanlorenzetti/halo_nr_tx" target="_blank"><i>H. salinarum</i> NRC-1 non-redundant transcriptome resource</a>;
          </li>
          <li>
            <b>COG Info:</b> This table brings information retrieved from the <a href="https://www.ncbi.nlm.nih.gov/research/cog/" target="_blank">clusters of orthologous genes (COG)</a> database <a href="https://pubmed.ncbi.nlm.nih.gov/33167031/" target="_blank">(Galperin, et al., 2021)</a>. For each representative open reading frame (column #1), we list the ID (column #2), the enunciate (column #3), the category (column #4), and the functional pathway (column #5);
          </li>
          <li>
            <b>IS Info:</b> This table brings a non-redundant set of insertion sequences (mobile genetic elements). The open reading frames (column #1) are localized within the named insertion sequences (column #2) from various families (column #3) and subgroups (column #4).
          </li>
        </ul>
        <p>&nbsp;</p>
        <p>
          Clicking on the linked locus tags will take you to a page dedicated to the selected gene. It should take about 30 seconds to load the page. There, you will get general information about the gene and a genome browser centering on the region of interest and its neighbors. Notice that you cannot go far right or left because the features will disappear after a few kilobases. That is a consequence of downsizing the data sets to avoid memory-related crashes. If you would like to browse another gene, please, go back to the "Home" section and start your search again.
        </p>
        <p>
          All the genes can be explored using the genome browser, but not all will show miscellaneous information. Below, we list a set of features that can be displayed for a selected gene.
        </p>
        <ul>
          <li>
            <b>Annotations:</b> The location following the format "replicon start end" (column #1); clusters of orthologous genes ID (column #2); possibly deprecated GenBank ID (column #3); gene symbol (column #4); from <a href="http://db.systemsbiology.net/sbeams/">SBEAMS</a>
          </li>
          <li>
            <b>Genome Browser:</b> This subsection displays an embedded genome browser window powered by <a href="https://github.com/igvteam/igv.js/" target="_blank">igv.js</a>. From top to bottom, the tracks are:
            <ul>
              <li><b>The nucleotide sequence</b> and its three-frame translation (only visible when zoomed-in);</li>
              <li>
                <b>Ribo-Seq TP1-4 (+):</b> Normalized read depth tracks for the ribosome profiling experiment (positive strand) sampled from four consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase). Mean of three replicates;
              </li>
              <li>
                <b>RNA-Seq TP1-4 (+):</b> Normalized read depth tracks for the RNA-Seq experiment (positive strand) sampled from four consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase). Mean of three replicates;
              </li>
              <li>
                <b>TPS (+):</b> Transcript processing sites (positive strand) collected from <a href="https://pubmed.ncbi.nlm.nih.gov/34209065/" target="_blank">Ibrahim et al. (2021)</a>;
              </li>
              <li>
                <b>SmAP1 interaction (+):</b> Protein-RNA interaction inferred from a SmAP1-RNA co-immunoprecipitation assay followed by next-generation sequencing (positive strand);
              </li>
              <li>
                <b>Antisense RNAs:</b> Antisense RNA annotation from <a href="https://pubmed.ncbi.nlm.nih.gov/30959844/" target="_blank">de Almeida et al. (2019)</a>;
              </li>
              <li>
                <b>Genes:</b> Gene and coding sequence (CDS) annotation from <a href="https://pubmed.ncbi.nlm.nih.gov/31296677/" target="_blank">Pfeiffer et al. (2019)</a>;
              </li>
              <li>
                <b>IS annotation:</b> Insertion sequence annotation from <a href="https://pubmed.ncbi.nlm.nih.gov/31296677/" target="_blank">Pfeiffer et al. (2019)</a>;
              </li>
              <li>
                <b>SmAP1 interaction (-):</b> Protein-RNA interaction inferred from a SmAP1-RNA co-immunoprecipitation assay followed by next-generation sequencing (negative strand);
              </li>
              <li>
                <b>TPS (-):</b>Transcript processing sites (negative strand) collected from <a href="https://pubmed.ncbi.nlm.nih.gov/34209065/" target="_blank">Ibrahim et al. (2021)</a>;
              </li>
              <li>
                <b>Ribo-Seq TP1-4 (-):</b> Normalized read depth tracks for the ribosome profiling experiment (negative strand) sampled from four consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase). Mean of three replicates;
              </li>
              <li>
                <b>RNA-Seq TP1-4 (-):</b> Normalized read depth tracks for the RNA-Seq experiment (negative strand) sampled from four consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase). Mean of three replicates;
              </li>
              <li>
                The user can choose whether raw or log-transformed read depth is displayed by unchecking/checking the box located at the top of the genome browser window; it is also possible to customize each track by clicking on the right-hand size gear button.
              </li>
            </ul>
          </li>
          <li>
            <b>COG information:</b> Information collected from the <a href="https://www.ncbi.nlm.nih.gov/research/cog/" target="_blank">clusters of orthologous genes (COG)</a> database <a href="https://pubmed.ncbi.nlm.nih.gov/33167031/" target="_blank">(Galperin, et al., 2021)</a>;
          </li>
          <li>
            <b>Gene ontology:</b> Information collected from <a href="https://www.uniprot.org/taxonomy/64091">UniProt</a>
          </li>
          <li>
            <b>Cross References:</b> Links to multiple external resources;
          </li>
          <li>
            <b>Gene Regulatory Network:</b> Links to environmental gene regulatory influence networks (EGRIN) databases;
          </li>
          <li>
            <b>Transcript Structure:</b> Transcript structure for the target gene and its neighbors;
          </li>
          <li>
            <b>Data:</b> Transcriptome levels measured by microarrays in multiple conditions for the selected gene;
          </li>
          <li>
            <b>Sequences:</b> DNA and protein sequences for the selected gene.
          </li>
        </ul>
        <p>&nbsp;</p>
        <h3 id="pd-atlas">Atlas</h3>
        <p>
          This tab displays an interactive heat map powered by <a href="https://jokergoo.github.io/InteractiveComplexHeatmap/" target="_blank">InteractiveComplexHeatmap</a> and Shiny R packages. It should take about 40 seconds to load the tool using the Google Chrome Browser. Once the device is loaded, the user should be able to browse a comprehensive heat map, including 2,579 protein coding entries (rows) of the <i>H. salinarum</i> NRC-1 genome grouped by COG categories. On the left-hand side, we displayed several annotation columns:
        </p>
        <ul>
          <li>
            <b>COG:</b> Category according to the <a href="https://www.ncbi.nlm.nih.gov/research/cog/" target="_blank">clusters of orthologous genes (COG)</a> database <a href="https://pubmed.ncbi.nlm.nih.gov/33167031/" target="_blank">(Galperin et al., 2021)</a>;
          </li>
          <li>
            <b>Chromosome:</b> The representative instance is located within the chromosome (NC_002607.1);
          </li>
          <li>
            <b>pNRC100:</b> The representative instance is located within the plasmid pNRC100 (NC_001869.1);
          </li>
          <li>
            <b>pNRC200:</b> The representative instance is located within the plasmid pNRC200 (NC_002608.1);
          </li>
          <li>
            <b>SmAP1:</b> Whether there is at least one SmAP1 binding site on the same strand for a given gene;
          </li>
          <li>
            <b>asRNA:</b> Whether there is at least one annotated antisense RNA (asRNA) according to <a href="https://pubmed.ncbi.nlm.nih.gov/30959844/" target="_blank">de Almeida et al. (2019)</a>;
          </li>
          <li>
            <b>TPS:</b> Whether there is at least one transcript processing site (TPS) on the same strand for a given gene according to <a href="https://pubmed.ncbi.nlm.nih.gov/34209065/" target="_blank">Ibrahim et al. (2021)</a>;
          </li>
          <li>
            <b>2099:</b> Log<sub>2</sub>-transformed fold change of RNase_2099C knockout vs. the control strain. Data reanalysis of <a href="https://pubmed.ncbi.nlm.nih.gov/24612392/" target="_blank">Wurtmann et al. (2014)</a>;
          </li>
          <li>
            <b>Half-life:</b> Experimentally determined half-life of a transcript according to <a href="https://pubmed.ncbi.nlm.nih.gov/17644597/" target="_blank">Hundt et al. (2007)</a>;
          </li>
          <li>
            <b>CAI:</b> Codon adaptation index computed using the 5% most abundant proteins in this study as the reference set;
          </li>
          <li>
            <b>GC Content:</b> Difference (residue) between GC content for a given gene and the mean GC content considering all the genes.
          </li>
        </ul>
        <p>&nbsp;</p>
        <p>
          Moreover, the tool shows five heatmaps side-by-side, grouped by COG categories and clustered by Protein levels:
        </p>
        <ul>
          <li>
            <b>Protein:</b> Log<sub>10</sub>-transformed proteome quantitative measure (a pseudocount was imputed for missing values) for consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase);
          </li>
          <li>
            <b>mRNA:</b> Log<sub>10</sub>-transformed transcriptome quantitative measure (TPM+1) for consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase);
          </li>
          <li>
            <b>RPF:</b> Log<sub>10</sub>-transformed ribosome mRNA protected fragment quantitative measure (RPF; Ribo-Seq experiment; TPM+1) for consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase);
          </li>
          <li>
            <b>TE:</b> Log<sub>2</sub>-transformed translational efficiency for consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase). Given by Protein divided by mRNA in a time point-wise manner;
          </li>
          <li>
            <b>RO:</b> Log<sub>2</sub>-transformed ribosome occupancy for consecutive time points of a growth curve (TP1: early exponential growth phase; TP2: mid-exponential growth phase; TP3: late exponential growth phase; TP4: stationary phase). Given by RPF divided by mRNA in a time point-wise manner.
          </li>
        </ul>
        <p>&nbsp;</p>
     
        <h2 id="usage-examples">Usage Examples</h2>
        <h3 id="ue-selectgene">Selecting a gene to open in the genome browser</h3>
        <v-img style="width: 75%" alt="select gene" src="@/assets/ue_selectgene.gif" />
        <p>&nbsp;</p>

        <h3 id="ue-browsemobilome">Browsing the mobilome cluster using the interactive heatmap</h3>
        <v-img style="width: 75%" alt="browse mobilome cluster" src="@/assets/ue_browse_mobilome.gif" />
        <p>&nbsp;</p>

        <h3 id="ue-intheatmapsearch">Using the interactive heatmap search tool</h3>
        <p>
          For that, we are going to use a comma-separated set of locus tags for genes comprising the gvp cluster. Only representative locus tags are allowed (see column #1 in the table at the "Home" section for all the possible entries).
        </p>
        <pre>
VNG_7015,VNG_7016,VNG_7017,VNG_7018,VNG_7019,VNG_7020,VNG_7021,VNG_7022,VNG_7023,VNG_7024
VNG_7025,VNG_7026,VNG_7027,VNG_7028
        </pre>
        <v-img style="width: 75%" alt="use interactive heatmap search" src="@/assets/ue_intheatmapsearch.gif" />
        <p>&nbsp;</p>

        <h3 id="ue-downloaddata">Downloading data for the gvp gene cluster demonstrated above</h3>
        <v-img style="width: 75%" alt="download data" src="@/assets/ue_downloaddata.gif" />
        <p>&nbsp;</p>

        <h2 id="download">Data download</h2>
        <p>
          You can download data for the following:
        </p>
        <ul>
          <li>
            <b>Atlas:</b> The entire table used to generate the interactive heatmap is available <a :href="heatmapTableURL" target="_blank">here</a> and as a supplement file in our manuscript (protein levels, RNA-Seq levels, Ribo-Seq levels, translational efficiency, and ribosome occupancy are not log-transformed in this version; the column description is available inside the workbook);
          </li>
          <li>
            <b>Atlas (Static):</b> A PDF file for the static heatmap is available <a :href="heatmapPDFURL" target="_blank">here</a>;
          </li>
          <li>
            <b>Genome browser:</b> A bundle containing all the tracks is available <a :href="dataArchiveURL" target="_blank">here</a>. We identify each file below, and you should be able to get more details about each track in the genome browser description section above:
            <ul>
              <li><b>Hsalinarum.fa:</b> Halobacterium salinarum NRC-1 genome sequence (FASTA format);</li>
              <li>
                <b>Hsalinarum.fa.fai:</b> FASTA index for the genome sequence file;
              </li>
              <li>
                <b>Hsalinarum-gene-annotation-pfeiffer2019-adjusted-names.gff3:</b> Gene annotation file (GFF3);
              </li>
              <li>
                <b>Hsalinarum-846asRNAs-deAlmeida2019.gff3:</b> Antisense RNA annotation (GFF3);
              </li>
              <li>
                <b>Hsalinarum-pfeiffer2019-mobileElements.gff3:</b> Insertion sequence annotation (GFF3);
              </li>
              <li>
                <b>mergedBRs_interaction-regions-entire-genome-[fr][we][dv].gff3:</b> SmAP1 interaction regions (GFF3) for the positive and negative strands (fwd and rev, respectively);
              </li>
              <li>
                <b>TPS_gff_[fr][we][dv].gff3:</b> Transcript processing sites (GFF3) for the positive and negative strands (fwd and rev, respectively);
              </li>
              <li>
                <b>ribosomal_RNA_TP[1234]-[fr][we][dv].bedgraph:</b> Ribo-Seq read depth for samples obtained from consecutive time points of a growth curve (TP1-4). Positive and negative strands are represented by fwd and rev, respectively (BEDGRAPH format);
              </li>
              <li>
                <b>total-RNA-TP[1234]-[fr][we][dv].bedgraph:</b> RNA-Seq read depth for samples obtained from consecutive time points of a growth curve (TP1-4). Positive and negative strands are represented by rev and fwd, respectively (BEDGRAPH format). Notice rev and fwd are inverted here, since the sequencing libraries were prepared using the TruSeq mRNA Stranded kit (Illumina).
              </li>
            </ul>
          </li>
        </ul>
        <p>&nbsp;</p>
        <h2 id="citation">Citation</h2>
        <p>
          If you make use of this web portal or the data we made public, please, cite:
        </p>
        <p>
          Lorenzetti <i>et al.</i> (2022). "A genome-scale atlas reveals complex interplay of transcription and translation in an archaeon*"*. <i>Journ. Nam.</i>, X(n), XX-XX.
        </p>

        <h2 id="support">Bugs and feature requests</h2>
        <p>
          The code for this web portal is publicly available on <a href="https://github.com/baliga-lab/halodata" target="_blank">GitHub</a>. Please, leave your bug reports, suggestions, and feature requests <a href="https://github.com/baliga-lab/halodata/issues" target="_blank">here</a>.
        </p>

        <h2 id="funding">Funding</h2>
        <p>
          The development of the Halo Data Atlas is supported by the following grants
        </p>
        <ul>
          <li>National Science Foundation: MCB-1616955;</li>
          <li>National Science Foundation: MCB-2105570;</li>
          <li>National Science Foundation: DBI-1920268;</li>
          <li>NIH—National Institute of General Medical Sciences: R01GM087221;</li>
          <li>NIH—The Office of the Director: S10OD026936;</li>
          <li>The São Paulo Research Foundation (FAPESP) fellowships #2017/03052-2 and #2019/13440-5;</li>
          <li>FAPESP fellowships #2011/07487-7 and #2013/21522-5;</li>
          <li>FAPESP grants #2009/09532-0 and #2015/21038-1;</li>
          <li>The Coordenação de Aperfeiçoamento de Pessoal de Nível Superior—Brasil (CAPES)—Finance Code 001;</li>
          <li>The Fundação de Apoio ao Ensino, Pesquisa e Assistência do Hospital das Clínicas da Faculdade de Medicina de Ribeirão Preto da Universidade de São Paulo (FAEPA).</li>
        </ul>
        
        <p>&nbsp;</p>
        <h2 id="team">Team</h2>
        <ul>
          <li>Alan P. R. Lorenzetti <sup><a href="#fn1">1</a>,<a href="#fn2">2</a></sup></li>
          <li>Ulrike Kusebauch <sup><a href="#fn2">2</a></sup></li>
          <li>Lívia S. Zaramela <sup><a href="#fn1">1</a></sup></li>
          <li>Wei-Ju Wu <sup><a href="#fn2">2</a></sup></li>
          <li>João P. P. de Almeida <sup><a href="#fn1">1</a>,<a href="#fn3">3</a></sup></li>
          <li>Serdar Turkarslan <sup><a href="#fn2">2</a></sup></li>
          <li>Adrián L. G. de Lomana <sup><a href="#fn2">2</a>,<a href="#fn4">4</a></sup></li>
          <li>José V. Gomes-Filho <sup><a href="#fn1">1</a>,<a href="#fn5">5</a></sup></li>
          <li>Ricardo Z. N. Vêncio <sup><a href="#fn6">6</a></sup></li>
          <li>Robert L. Moritz <sup><a href="#fn2">2</a></sup></li>
          <li>Tie Koide <sup><a href="#fn1">1</a></sup></li>
          <li>Nitin S. Baliga <sup><a href="#fn1">2</a>,<a href="#fn7">7</a>,<a href="#fn8">8</a>,<a href="#fn9">9</a></sup></li>
        </ul>
        <hr style="margin-top: 10pt; margin-bottom: 10pt" />
        <sup id="fn1">1. Department of Biochemistry and Immunology, Ribeirão Preto Medical School, University of São Paulo, Ribeirão Preto, Brazil</sup><br/>
        <sup id="fn2">2. Institute for Systems Biology, Seattle, WA, USA</sup><br/>
        <sup id="fn3">3. Present address: Institute of Biological Sciences, Federal University of Minas Gerais, Belo Horizonte, Brazil</sup><br/>
        <sup id="fn4">4. Present address: Center for Systems Biology, University of Iceland, Reykjavik, Iceland</sup><br/>
        <sup id="fn5">5. Present address: Prokaryotic RNA Biology, Phillips-Universität Marburg, Marburg, Germany</sup><br/>
        <sup id="fn6">6. Department of Computation and Mathematics, Faculty of Philosophy, Sciences and Letters at Ribeirão Preto, University of São Paulo, Ribeirão Preto, Brazil</sup><br/>
        <sup id="fn7">7. Departments of Biology and Microbiology, University of Washington, Seattle, WA, USA</sup><br/>
        <sup id="fn8">8. Molecular and Cellular Biology Program, University of Washington, Seattle, WA, USA</sup><br/>
        <sup id="fn9">9. Lawrence Berkeley National Lab, Berkeley, CA, USA</sup><br/>
      </v-col>
    </v-row>
  </v-container>
</template>
<style>
  .section-sep {
  margin-top: 10pt;
  margin-bottom: 5pt;
  }
</style>
<script>
var STATIC_URL = process.env.VUE_APP_STATIC_URL;

export default {
    name: 'AboutPage',
    data: () => ({
        heatmapTableURL: STATIC_URL + 'File_S1.xlsx',
        heatmapPDFURL: STATIC_URL + 'File_S8.pdf',
        dataArchiveURL: STATIC_URL + 'igv_bundle.tar.gz'
    })
  }
</script>
