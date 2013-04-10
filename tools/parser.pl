#!/usr/bin/env perl

use strict;
use warnings;

use JSON;

my $doc = JSON->new->decode(
  do { local $/; <> }
);

my $out = build_tree( '', mk_seq_iter( @$doc ) );
#print JSON->new->pretty->canonical->encode( $out );

my $iter    = mk_seq_iter( @$out );
my @classes = ();
while ( my $class = parse_class( $iter ) ) {
  push @classes, $class;
}
print JSON->new->pretty->canonical->encode( \@classes );

sub parse_class {
  my $iter = shift;
  my $tok  = $iter->();
  return unless $tok;

  my $class = {};

  if ( $tok->[0] eq 'KEYWORD' && $tok->[1] eq 'aligned' ) {
    $class->{aligned} = parse_num_list( $iter );
    $tok = $iter->();
  }

  if ( $tok->[0] eq 'KEYWORD' && $tok->[1] eq 'abstract' ) {
    $class->{abstract}++;
    $tok = $iter->();
  }

  check( $tok, KEYWORD => 'class' );
  $class->{name} = expect( $iter, 'IDENT' )->[1];
  parse_class_body( $iter, $class );

  return $class;
}

sub parse_class_body {
  my ( $iter, $class ) = @_;
  my $tok = $iter->();
  if ( $tok->[0] eq 'OPEN' && $tok->[1] eq '(' ) {
    $class->{args} = $tok->[4];    # for now
    $tok = $iter->();
  }
  if ( $tok->[0] eq 'KEYWORD' && $tok->[1] eq 'extends' ) {
    parse_extends( $iter, $class );
    $tok = $iter->();
  }
  check( $tok, OPEN => '{' );
  $class->{body} = $tok->[4];
}

sub parse_extends {
  my ( $iter, $class ) = @_;
  my $extends = { name => expect( $iter, 'IDENT' )->[1] };
  my $tok = $iter->();
  if ( $tok->[0] eq 'OPEN' && $tok->[1] eq '(' ) {
    $extends->{args} = $tok->[4];
  }
  else {
    $iter->( $tok );
  }
  $class->{extends} = $extends;
}

sub parse_num_list {
  my $iter  = shift;
  my $biter = mk_block_iter( expect( $iter, OPEN => '(' ) );
  my $num   = expect( $biter, 'NUMBER' );
  all_done( $biter );
  return $num->[1];
}

sub all_done {
  my $iter = shift;
  my $tok  = $iter->();
  error( $tok, "Unexpected ", tok_str( @$tok ) ) if $tok;
}

sub check {
  my ( $tok, $type, $value ) = @_;
  error( $tok, "Expected ", tok_str( $type, $value ), ", got ", tok_str( @$tok ) )
   if ( defined $type && $type ne $tok->[0] )
   || ( defined $value && $value ne $tok->[1] );
  return $tok;
}

sub expect {
  my ( $iter, $type, $value ) = @_;
  return check( $iter->(), $type, $value );
}

sub tok_str {
  my @tok = @_;
  my @rep = ();
  push @rep, $tok[0]     if defined $tok[0];
  push @rep, "'$tok[1]'" if defined $tok[1];
  return '<' . join( ':', @rep ) . '>';
}

sub error {
  my ( $tok, @msg ) = @_;
  die "Line ", $tok->[2], ", column ", $tok->[3], ": ", join( '', @msg ), "\n";
}

sub mk_block_iter { mk_seq_iter( @{ shift->[4] || [] } ) }

sub mk_seq_iter {
  my @seq = @_;
  sub {
    if ( @_ ) {    # pushback?
      unshift @seq, @_;
      return;
    }
    return shift @seq;
  };
}

sub build_tree {
  my ( $closer, $iter ) = @_;
  my @block = ();
  while ( my $tok = $iter->() ) {
    if ( $tok->[0] eq 'CLOSE' ) {
      return \@block if $tok->[1] eq $closer;
      die "Unexpected ", JSON->new->encode( $tok ),
       ( $closer ? " (expected $closer)" : '' ), "\n";
    }
    elsif ( $tok->[0] eq 'OPEN' ) {
      ( my $cl = $tok->[1] ) =~ tr <{([><})]>;
      push @$tok, build_tree( $cl, $iter );
    }
    push @block, $tok;
  }
  return \@block;
}

# vim:ts=2:sw=2:sts=2:et:ft=perl

