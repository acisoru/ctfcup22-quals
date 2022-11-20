#!/usr/bin/perl
use Digest::SHA;

sub HttpError {
    my $error = @_[0];

    print "Content-Type: application/json\r\n\r\n";
    print "{\"status\": \"error\", \"error\": \"$error\"}";
}
use CGI;
my $cgi = CGI->new();

$cgi->http();

my $user = $cgi->param('user');
my $secretKey = $ENV{'HTTP_SECRETKEY'};

if ($user eq "") {
    HttpError("No user provided.");
    exit;
}

if ($secretKey eq "") {
    HttpError("No secret key found.");
    exit;
}

my $sha1 = Digest::SHA->new(1);
$sha1->add($secretKey);
$sha1->add("|");
$sha1->add($user);
$sha1->add("|");
$sha1->add($secretKey);

my $digest = $sha1->hexdigest;

print "Set-Cookie: lsession=$user.$digest\r\n";
print "Content-Type: application/json\r\n\r\n";
print "{\"status\": \"ok\"}"
