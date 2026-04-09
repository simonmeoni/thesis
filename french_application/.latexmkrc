@default_files = ('main.tex');
$out_dir = 'out';
$aux_dir = 'out';
$pdf_mode = 1;
$use_bibtex = 1;
$force_mode = 1;
# bibtex/bst search paths toward parent directory
$ENV{'BIBINPUTS'} = '.:../:';
$ENV{'BSTINPUTS'} = '.:../:../styles/:';
