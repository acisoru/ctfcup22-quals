FROM httpd:2.4.54-bullseye

RUN apt-get update -y && apt-get install -y perl libcgi-session-perl

COPY auth /usr/local/apache2/cgi-bin
RUN chmod +x /usr/local/apache2/cgi-bin/sessvalid.pl && chmod +x /usr/local/apache2/cgi-bin/sessgen.pl
CMD httpd-foreground -c "LoadModule cgid_module modules/mod_cgid.so"
