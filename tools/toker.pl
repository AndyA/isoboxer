#!/usr/bin/env perl

use strict;
use warnings;

use JSON;

my @keyword = qw(
 abstract aligned bit break case char class const else extends for if
 int optional reserved signed string switch template unsigned
);

my @operator = qw( != == = ++ -- + - * / <= << < >= >> > || && | & );

my $is_kw = join '|', @keyword;
my $is_oper = join '|', map quotemeta, @operator;
my $is_fourcc = "(?:‘|’|')(....)(?:‘|’|')";

sub make_toker {
  my ( $src, $ln ) = @_;
  sub {
    $src =~ /\G\s+/gc;
    my @l = ( $ln, pos $src );
    $src =~ /\G($is_kw)/gc     && return [ KEYWORD => $1, @l ];
    $src =~ /\G([_a-z]\w*)/gci && return [ IDENT   => $1, @l ];
    $src =~ /\G(\d+)/gc        && return [ NUMBER  => $1, @l ];
    $src =~ /\G([\[\{\(])/gc   && return [ OPEN    => $1, @l ];
    $src =~ /\G([\]\}\)])/gc   && return [ CLOSE   => $1, @l ];
    $src =~ /\G\/\/(.*)$/gc    && return [ COMMENT => $1, @l ];
    $src =~ /\G($is_oper)/gc   && return [ OPER    => $1, @l ];
    $src =~ /\G([,;:])/gc      && return [ PUNC    => $1, @l ];
    $src =~ /\G$is_fourcc/gc   && return [ FOURCC  => $1, @l ];
    $src =~ /\G$/gc            && return;
    return [ UNKOWN => substr( $src, pos $src ), @l ];
  };
}

my @doc  = ();
my $lnum = 1;
while ( <> ) {
  chomp( my $ln = $_ );
  my $t = make_toker( $ln, $lnum++ );
  while ( my $tok = $t->() ) {
    die JSON->new->encode( $tok ) if $tok->[0] eq 'UNKOWN';
    push @doc, $tok;
  }
}

print JSON->new->pretty->canonical->encode( \@doc );

# vim:ts=2:sw=2:sts=2:et:ft=perl

