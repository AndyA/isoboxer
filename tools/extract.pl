#!/usr/bin/env perl

use strict;
use warnings;

my $nest  = 0;
my $force = 0;
while ( <> ) {
  s/\r//g;
  chomp( my $ln = $_ );
  $force = 1 if $ln =~ /^ \s* (?: aligned \s* \( \s* \d+ \s* \) \s+)?
                              (?: abstract \s+)?
                              class \s+ (\w+) /x;

  if ( $force || $nest ) {
    print "\n" unless $nest;
    $ln =~ s/([{}])(?!\s*$)/$1\n/g;
    for my $frag ( split /\n/, $ln ) {
      my $lnest = $nest;
      for ( grep /[\[\(\{\}\)\]]/, split //, $frag ) {
        $nest += /[\[\(\{]/ ? 1 : -1;
        $force = 0;
      }
      $frag =~ s/^\s+//;
      print '  ' x ( $nest < $lnest ? $nest : $lnest ), "$frag\n";
    }
  }
}

# vim:ts=2:sw=2:sts=2:et:ft=perl
