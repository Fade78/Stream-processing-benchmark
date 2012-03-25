#!/usr/bin/perl

use strict;
use warnings;

my $commentary=0;
my $unknownline=0;

while(<>) {
	s/,//g;
	if(/^(\d+)\s+(\S+)\s+(\S+)\s+(\d+(?:\.\d+)?)/) {
		print "$1,$4,$3,$2\n" 
	} elsif(/^#/) {
		$commentary++;
	} else {
		$unknownline++;
	}
}

sub explicit_version () {
	if($]=~/^(\d+)\.(\d{3})(\d{3})$/) {
		return sprintf("%d.%d.%d",$1,$2,$3);
	} else {
		return "Can't find PERL version";
	}
}

print "#PERL version ".explicit_version()."\nparsed line: $., commentary line: $commentary, unknown line: $unknownline.\n";
