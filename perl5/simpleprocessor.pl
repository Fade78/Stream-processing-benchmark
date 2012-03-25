#!/usr/bin/perl

use strict;
use warnings;

my $scripttitle="PERL REFERENCE PROCESSOR";

my $commentary=0;
my $unknownline=0;

my %DATA;

print "#$scripttitle\n#TRANSFORMED INPUT\n";

while(<>) {
	s/,//g;
	if(/^(\d+)\s+(\S+)\s+(\S+)\s+(\d+(?:\.\d+)?)/) {
		$DATA{$2}{$3}+=$4;
		printf("$1,%.0f,$3,$2\n",$4);
	} elsif(/^#/) {
		$commentary++;
	} else {
		$unknownline++;
	}
}

my $keystat=0;

print "#DATADUMP\n";

for my $k1 (sort keys %DATA) {
	my $str="$k1:";
	for my $k2 (sort keys %{$DATA{$k1}}) {
		$keystat++;
		$str.=" ($k2:".int($DATA{$k1}{$k2}).")"
	}
	print "$str\n";
}


sub explicit_version () {
	if($]=~/^(\d+)\.(\d{3})(\d{3})$/) {
		return sprintf("%d.%d.%d",$1,$2,$3);
	} else {
		return "Can't find PERL version";
	}
}

my $report="#$scripttitle\n#perl version: ".explicit_version()."\nparsed line: $., commentary line: $commentary, unknown line: $unknownline, keystat: $keystat.\n";
print "#REPORT\n$report";
print STDERR "$report";
