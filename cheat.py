text = r"""
'DIGITAL GARDEN', 'SYSE' (MX && SPF)

mx1.pub.mailpod1-osl1.one.com
mx2.pub.mailpod1-osl1.one.com
mx3.pub.mailpod1-osl1.one.com

x.tornado.email
y.tornado.email
z.tornado.email
 
v=spf1 include:_spf.uniweb.no ~all
v=spf1 include:_spf.fastname.no ~all
v=spf1 include:tornado.email ~all
v=spf1 a include:_custspf.one.com ~all



HUSK Å ENDER FQDN OG CLUSTER
ed1._domainkey.$FQDN 300 IN CNAME ed1.dkim.$CLUSTER.service.one
ed2._domainkey.$FQDN 300 IN CNAME ed2.dkim.$CLUSTER.service.one
rsa1._domainkey.$FQDN 300 IN CNAME rsa1.dkim.$CLUSTER.service.one
rsa2._domainkey.$FQDN 300 IN CNAME rsa2.dkim.$CLUSTER.service.one


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'DIGITAL GARDEN', 'SYSE' (KONTROLLPANEL)

"https://www.fastname.no/controlpanel"
"https://www.uniweb.no/controlpanel"
"https://www.syse.no/controlpanel"
"https://www.proisp.no/controlpanel"

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Server for innkommende epost: mail.fastname.no / mail.uniweb.no / tornado.email /imap.proisp.no
IMAP-Port: 143
Krypteringsmetode: StartTLS
Krever passordgodkjenning. Brukernavn: Hele epostadressen (din@epostadresse.no)

Server for utgående epost: mail.fastname.no / mail.uniweb.no / tornado.email / smtp.proisp.no
SMTP-Port: 587
Krypteringsmetode: StartTLS
Krever passordgodkjenning. Samme brukernavn og passord som for innkommende server.

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
WEBFORWARD

dns.tld IN A 104.37.39.71
www.dns.tld IN CNAME dns.tld
_redir.dns.tld IN TXT "301 https://web.site"

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'FIKSE RETTIGHETER' (KJØRES FRA ROOT)

find -type d -exec chmod 755 {} \;
find -type f -exec chmod 644 {} \;

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'SYSE' (EXIM LOGS)

ssh support@syslog.syse.no
cd /var/log/syslog/mailsys-exim
grep epost@epost.domene år-måned-dag.log
grep id år-måned-dag.log

* = erstatter resten av linjen, feks grep ID-NUMMER 2023-01-1*

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'DIGITAL GARDEN' (VIDERESENDING MED SSL)

bb11.org		3600	A		104.37.39.71	
www.bb11.org		3600	CNAME		bb11.org
_redir.bb11.org		3600	TXT		"307 https://nettside.no"

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

---------------------------------------------------
'KORT RESERVASJON' > (HUSKEREGEL)
---------------------------------------------------
Stripe er satt opp slik at vi kan bare holde en kortreservasjon i 7 dager. 
Dersom det er over 7 dager siden vi reserverte beløpet på kontoen til kunden og vi ikke har trukket beløpet blir reservasjonen automatisk frigjort.
Når belaste kort tasken ikke er lukket kan man som regel benytte valget "Cancel Authorization" om man høyreklikker på "Stripe Kortbetaling".

('templates', 'templates', 'templates', 'templates', 'templates',)

---------------------------------------------------
'WEBROOTS' > (INSTALLERE WORDPRESS TIL NY ROOT)
---------------------------------------------------

For å installere en Wordpress til en ny katalog gjør dere følgende i kontrollpanel:

- Logg inn her: https://www.syse.no/controlpanel/
- I menyen til venstre trykk på Webhosting > Webhotell > Trykk på webhotellet.
- Trykk på Domener og rotmapper og velg Ny rotmappe > Denne kan hete hva som helst, feks www2.
- Trykk deretter på Wordpress > Nå kan du trykke Installere Wordpress til den nye rotmappen.
- Følg instruksjonene på skjermen for å opprette en bruker i Wordpress.zkun
- Når den nye siden er ferdig og klar til bruk kan domene kobles fra den gamle siden og kobles til den nye på denne måten:
- Trykk på Domener og rotmapper > I den første rotmappen kan du trykke på X for å koble fra domene
- Deretter kan du trykke på Koble til domene på den andre rotmappen.

---------------------------------------------------
'EPOST' > (OPPSETT AV NY EPOSTKONTO)
---------------------------------------------------

En liten guide på hvordan du setter opp ny epostkonto:

- Logg inn på kontrollpanelet ditt her: https://www.syse.no/controlpanel/
- I menyen til venstre trykk på Mail > Administrer kontoer
- På høyre side kan du se Ny e-postkonto, trykk på den.
- I dette bilde velger du hva adressen skal være ved å skrive inn i Adresse-feltet (feks kontakt)
- Under Navn skriver du det du vil det skal stå når du sender noen epost (feks *********)
- Så trykker du Legg til

Nå må du opprette passord på kontoen: Du kan sette passord ved å trykke Nytt passord på høyre side av skjermen.

Håper dette er oppklarende, om ikke tar du bare kontakt igjen!

---------------------------------------------------
'EPOST' > (SPAMFILTER)
---------------------------------------------------

Her er en oppskrift på hvordan du kan hviteliste individuelle eposter eller fullstendige domener:

- Logg inn på kontrollpanel her: https://uniweb.no/controlpanel/
- I menyen til venstre velger du Mail > Spamfilter
- På høyre side finner du Blokkert/godkjentliste, trykk der

Her kan du legge til en enkelt epost som feks: 

epost@domene.no

Eller så kan du legge til et helt domene som feks:

@domene.no

Når du har skrevet inn epost/domenenavn velger du Godkjent og trykker Legg til.

---------------------------------------------------
EIERSKIFTE BARE DOMENE
---------------------------------------------------

I Syse Console bruk enten Custom .no owner change eller Custom .no owner change bulk.

Kopier: var domains = ['dintrikker.no', 'ge1.no', 'gjerbergelektriker1.no']; inn i Notepad og kopier inn alle domenene som skal flyttes.

Kopier tilbake i konsollen og endre til nytt kundenummer.

Trykk 'Execute'.

Eierskifte for .no domener utført, send epost til kunde ang. videre instruksjoner og be om svar tilbake når OK.

----------------------------------------------------
KOMMANDOER I TERMINAL/SHELL
----------------------------------------------------

whois [domenenavn] = viser hvor domenet er registrert

dig [domenenavn] = viser hvor navnetjenere er registrert og IP-adresser

dig ns [domenenavn] = viser hva navnetjenerne heter

dig mx [domenenavn] = viser hvor MX tjeneren er registrert

dig txt [domenenavn] = viser hvilke txt-poster som er registrert

-----------------------------------------------------
BACKUP OG GJENOPPRETTING
-----------------------------------------------------

Avklar om både webhotell og database skal gjenopprettes og fra hvilken dato.

Informer om pris (600kr eks. MVA).

Opprett CA og spesifiser hva som skal taes restore og dato, samt legg til pris der også.

-----------------------------------------------------
WORDPRESS KOMMANDOER I TERMINAL
-----------------------------------------------------



-----------------------------------------------------
WEBHOTELL, WEB SERVER OG VPS SERVER
-----------------------------------------------------

Public Key / RSA nøkkel: kunde oppretter selv til sin VPS server

FTP: kunde installerer dette selv på sin VPS server før det kan benyttes

-----------------------------------------------------
SFTP / FTP PÅLOGGING
-----------------------------------------------------

Host: det som står bak SSH/SFTP
Username:dette står under Domener og rotmapper, SSH brukernavn
Password:egendefinert av bruker
Port: 22

-----------------------------------------------------
PHP OPPGRADERING / NEDGRADERING
-----------------------------------------------------

1. Gå til nettside for utsendt epost angående PHP oppgradering
2. Kopier alt som står bak slashen i lenken for å sette tidspunkt
3. t: i KS og lim inn alt som ble kopier fra bak slashen
4. Dersom tasken er lukket, dobbeltklikk på datoen og fjern dette.
   Sjekk dato for oppfølging, bør endres dersom det bare er 1 dag igjen osv.
5. Høyreklikk på "Oppgradere runtime for w...."
   Trykk Set Progress og kjør denne igjennom med PendingUpgrade
6. Lagre i KS
7. Trykk på lenken igjen og kjør oppgradering og nedgradering etter hverandre.

------------------------------------------------------
WORDPRESS DEBUGGING
------------------------------------------------------

Ved feil som forekommer av PHP oppgradering i WordPress kan kunde gå frem for å feilsøke på ulike 3 måter:
1. Benytte WP Debugging plugin: https://wordpress.org/plugins/wp-debugging/
2. Slå av alle plugins og slå på 1 og 1 for å sjekke hvilke som knekker nettsiden.
3. Kontakte webutvikler.

------------------------------------------------------
DNS OPPFØRINGER
------------------------------------------------------

A = peker til en IP adresse med IPv4 format
CNAME = et alias for et navn til et annet
MX = mail exchange servere som godtar epost for et domene
TXT = brukt til SPF, DKIM, DMARC etc.
SRV = brukt til nyere protokoller istedetfor feks MX
AAAA = peker til en IP adresse med IPv6 format

-------------------------------------------------------
EIERSKIFTE
-------------------------------------------------------

DG = Kunde oppretter kundekonto som må være tom, vi ordner resten.
SYSE = Kunden kan flytte domener selv via syse.no, må gi beskjed når gjennomført så kan vi flytte webhotell, web server osv.

------------------------------------------------------
TILBAKEBETALING AV DOBBELTBETALT FAKTURA/KREDITNOTA
------------------------------------------------------

Syse: blir automatisk tilbakeført av PayEx til samme konto betaling kom fra
DG: gjøres manuelt av fakturaavdeling LK/Wilhelm/Max

-----------------------------------------------------	
EPOSTBEGRENSNINGER
-----------------------------------------------------

Per konto: 
25 eposter / 5 min
250 mottakere / 5 min
1000 mottakere / 24 timer
5000 mottakere / 30 dager

------------------------------------------------------
FORHANDLER AVTALER / RABATTER
------------------------------------------------------

DG KUNDER: Lars Kristian
SYSE KUNDER: Max

Ved kreditering av faktura kan dette utføres, og summen vil bli trukket av neste faktura som forhandler får av oss.

-----------------------------------------------------
EKSTERN DNS FOR DOMENER
-----------------------------------------------------

DIG NS gir ns01.no.brand.one.com: dette er DG NS

-----------------------------------------------------
TEAMVIEWER FOR MAC
-----------------------------------------------------

systemvalg - personvern/sikkerhet - skjermopptak - teamviewer
systemvalg - personvern/sikkerhet - tilgjengelighet

-----------------------------------------------------
WORDPRESS DATABASE FEIL
-----------------------------------------------------

Sjekk domenet med /wp-admin og dersom feilmeldingen viser til ERROR DATABASE = Databasefeil

-----------------------------------------------------
PRINCIPAL FOR DG/SYSE
-----------------------------------------------------

https://fastname.no/controlpanel/register/principal/
https://uniweb.no/controlpanel/register/principal/
https://www.syse.no/controlpanel/principal/
https://www.proisp.no/controlpanel/register/principal/

-----------------------------------------------------
SSL ERROR PORT 80/443
-----------------------------------------------------

CNAME oppføring: _acme-challenge.domene.no IN CNAME domene.no.acme.webpod1-osl1.one.com
Husk å bytt ut "domene.no" med det aktuelle domene på begge punkter

-----------------------------------------------------
LEGGE TIL SONEFIL FØR DOMENET ER FLYTTET/REG
-----------------------------------------------------

Søk opp domenet i KS
Dobbeltklikk på domenetnavnet under Abonnementer
'Konverter til ...domene'
Oppdater KS
'Konverter til Drift av DNS'
Sonefil kan nå lastes opp i kontrollpanel

------------------------------------------------------
NYE KONTONUMMER
------------------------------------------------------

Syse: 8101.35.55222
Uniweb: 8101.58.48766
Fastname: 8101.58.48758

------------------------------------------------------
WORDPRESS INSTALLASJON FEILET PÅ HOSTING (FEILMELDING FINNER IKKE DATABASE)
------------------------------------------------------

Logg på hosting med SSH
CMD ls -al
CMD cd www
CMD 

------------------------------------------------------
WORDPRESS INSTALL SSH
------------------------------------------------------

wget https://wordpress.org/latest.tar.gz
tar -zxf latest.tar.gz --strip-components=1
find -type d -exec chmod 755 {} \;
find -type f -exec chmod 644 {} \;

------------------------------------------------------
SUBDOMENE TIL WEBHOSTING
------------------------------------------------------

Opprett subdomene i kontrollpanel
Koble subdomene til hostingtjeneste under Domener og rotmapper
Oppretter A og AAAA for subdomene automatisk

-----------------------------------------------------
KONKURSRAMMEDE FORHANDLER VED BOSTYRER OG EIERSKIFTER
-----------------------------------------------------

- Kunde tar kontakt med bostyrer først med kontaktinfo fra BRREG

-----------------------------------------------------
GJENOPPRETTE DOMENE
-----------------------------------------------------

- Sjekk eierskap, fornyelse, cluster etc.
- CA 
- Domene gjenopprettes til samme kundekonto/cluster via KS
- Sørg for at DNSSEC er slått av

----------------------------------------------------
OPPRETTE WP BRUKER FOR KUNDESERVICE
----------------------------------------------------
- Kommando på root: wp user create syse le@syse.no --role=administrator --user_pass=Passw0rd!
- Slette på root: wp user delete syse le@syse.no --role=administrator --user_pass=Passw0rd!

---------------------------------------------------
REFUNDERING AV KORTBETALING
---------------------------------------------------
- Kreditere beløp og kjøre ut kreditnota i KS
- Kopiere ut EXT.ID. under opprinnelig faktura i KS
- Sende dette med hvilket brand til Karen på Slack

--------------------------------------------------
PAYEX BANKINFORMASJON
--------------------------------------------------

Bankens navn: Danske Bank Sverige
Bankens adresse og landskode: Norrmalmstorg 1, Box 7523, 103 92 Stockholm
Bankens tlf. nr.: +46 752-48 49 30 SE

--------------------------------------------------
SSL kommandoer i terminal fra Moen
--------------------------------------------------

check domene.navn <-- denne vil du bruke mest
checkcert domene.navn <-- denne inkluderer litt mer cert info
checkssl domene.navn <-- denne bruker openssl til å vise cert-chain

whoisreg = registrar whois
drift = ssh le@drift.syse.no

forkortet whois = whs domene.navn

-----------------------------------------------------
KOMMANDO FOR Å SJEKKE CERT KRYPTERING
-----------------------------------------------------
vim domenenavn.crt i terminal (bytt ut domenenavn med domene det gjelder) - oppretter en fil
Kopier CA info fra KP til SSL
Shift + insert i terminal + enter
openssl x509 -noout -text -in domenenavn.crt | grep 'Signature Algorithm' 
Sjekker kryptering av SSL

-----------------------------------------------------
LOGG PÅ MED SSH PÅ TWS/OWS
-----------------------------------------------------
ssh brukernavn på tws/ows @IP adresse -p 22

-----------------------------------------------------
KONTAKTINFO PAYEX NORGE
-----------------------------------------------------
22 03 61 81 eller epost post.collection@payex.com

-----------------------------------------------------
KONTAKTINFO COLLECTIA AS
-----------------------------------------------------
24 07 63 00 eller epost eq@collectiagroup.no

-----------------------------------------------------
SYSE PARTNER API
-----------------------------------------------------
https://www.syse.no/api/partner

-----------------------------------------------------
SITEBUILDER ENDRE URL
-----------------------------------------------------
- Koble fra domenenavn
- Gå til Redigeringsverktøy -> Rediger nettsted
- Trykk 'Publish' for å pushe App-URL
- koble til domenenavn som skal endres til
- Inn i Redigeringsverktøy -> trykk publish for å koble til nytt domenenavn
(NB! det kan bare være ett domene koblet til SiteBuilder)
"""

def cheat_sheet(search_word):
    search_word = search_word.lower()
    matching_lines = []
    for line in text.splitlines():
        if search_word in line.lower():
            matching_lines.append(line)
            matching_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return matching_lines