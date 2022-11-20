#!/usr/bin/perl
use Digest::SHA;

sub HttpError {
    my $error = @_[0];

    print "Content-Type: application/json\r\n\r\n";
    print "{\"status\": \"error\", \"error\": \"$error\"}";
}

use CGI;
my $cgi = CGI->new();

my $session  = $cgi->cookie('lsession');
my $secretKey = $ENV{'HTTP_SECRETKEY'};

if ($session eq "") {
    HttpError("No session cookie found.");
    exit;
}

if ($secretKey eq "") {
    HttpError("No secret key found.");
    exit;
}


my @sessionPld = split(/\./, $session);

my $sessionLength = @sessionPld;

if ($sessionLength != 2) {
    HttpError("Invalid session.");
    exit;
}

my $sha1 = Digest::SHA->new(1);
$sha1->add($secretKey);
$sha1->add("|");
$sha1->add($sessionPld[0]);
$sha1->add("|");
$sha1->add($secretKey);

my $digest = $sha1->hexdigest;

if ($digest eq $sessionPld[1]) {
    print "Content-Type: application/json\r\n\r\n";
    print "{\"status\": \"ok\", \"user\": \"$sessionPld[0]\"}"
} else {
    HttpError("Invalid signature.")
}
