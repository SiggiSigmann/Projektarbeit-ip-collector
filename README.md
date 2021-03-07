<!-----
NEW: Check the "Suppress top comment" option to remove this info from the output.

Conversion time: 3.275 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β29
* Sat Mar 06 2021 23:25:55 GMT-0800 (PST)
* Source doc: Projektarbeit 
* This document has images: check for >>>>>  gd2md-html alert:  inline image link in generated source and store images to your server. NOTE: Images in exported zip file from Google Docs may not appear in  the same order as they do in your doc. Please check the images!

----->


<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 0; WARNINGs: 0; ALERTS: 13.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p><a href="#gdcalert1">alert1</a>
<a href="#gdcalert2">alert2</a>
<a href="#gdcalert3">alert3</a>
<a href="#gdcalert4">alert4</a>
<a href="#gdcalert5">alert5</a>
<a href="#gdcalert6">alert6</a>
<a href="#gdcalert7">alert7</a>
<a href="#gdcalert8">alert8</a>
<a href="#gdcalert9">alert9</a>
<a href="#gdcalert10">alert10</a>
<a href="#gdcalert11">alert11</a>
<a href="#gdcalert12">alert12</a>
<a href="#gdcalert13">alert13</a>

<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>



## IP-Tracking


## Abstrakt

Es wird immer wichtiger ein Benutzer beim Anmelden mit Online-Diensten zu Authentifizieren. Dabei stellt sich die Frage, wie oft der Benutzer sein Passwort oder andere Identifizierungsmerkmale eingeben soll. Diese Projektarbeit untersucht die Verwendung von IP-Tracking und die Daten die daraus gewonnen werden können. Anhand der Daten kann anschließend das Nutzerverhalten verfolgt werden um Anomalien zu erkennen und die Daten des Benutzers zu schützen. Der Fokus dieser Arbeit liegt primär auf das Sammeln von Realistischen Nutzerdaten und der Auswertung dieser Daten. Dazu wurde eine Website entwickelt.


## Einleitung

Als Projektarbeit hatten wir die initiale Aufgabe Nutzer anhand ihrer IP-Adresse mit Hilfe von Machine Learning zu erkennen. Da wir aber noch keine Testdaten hatten, entwickelte sich das Projekt zu einem IP-Collector, mit Schwerpunkt des Sammelns und Auswerten von Daten. Diese könnten dann als Inputdaten für Machine Learning Modelle verwendet werden.

Dazu haben wir im laufe der Projektarbeit einen Webserver mit einer Datenbank entwickelt. Unsere Endgeräte (Handys) haben den Benutzer simuliert und regelmäßig post Nachrichten an den Webserver gesendet. Der Webserver wendet anhand der IP-Adresse der Post-Request Anfrage, einen Reverse Traceroute an und speichert die Daten. Neben dem Sammeln von Testdaten, haben wir im laufe der Arbeit auch Diagramme generiert, um die gesammelten Daten auszuwerten.


## 


### Daten

Folgendes Kapitel beschreibt die Daten die wir mit unserem Projekt Sammeln


#### IP-Adresse


#### Zeit


#### Traceroute


#### ISP


#### Geographische Daten


### Aufbau der Webseite




## Projekt Aufbau

Die Projektarbeit unterteilt sich in drei Teile. Der erste Teil befasst sich mit dem Sammeln von Daten durch einen Python-Server. Anschließend erläutert der zweite Teil, das automatisierte “anpingen” des Servers um IP-Daten zu erhalten. Der dritte Teil befasst sich mit der Auswertung der Daten und den Informationen die daraus gewonnen werden können.


### Server

Für das Bereitstellen einer Website um Daten zu sammeln, wurde ein Python Webserver entwickelt. Dieser Abschnitt beschreibt wie dieser aufgebaut ist.

Der Webserver besteht aus drei Teilen. 



*   flaskServer: Ein Rest Server der auf die Anfragen der Clients Antwortet und die Website zu verfügung Stelltl.
*   database: Eine mysql Datenbank, die die gesammelten Einträge Speichert
*   backup: Automatisierte Skripte, die ein Backup der Datenbank erstellen.


#### Starten des Servers

Für das Bereitstellen und Hosten des Webservices wird Docker sowie Docker Compose verwendet. Für die vereinfachte Nutzung befinden sich im Hauptverzeichnis folgende Scripts: 



*   “setup.sh”: Einrichten der Backup Funktion
*   “start.sh”: neu bauen und starten des servers
*   “clean.sh”: Löschen von veralteteten Dockercontainer und Images


#### Installation:

Zum Hosten des Serves wird eine Linux-Maschine benötigt. Dies ist notwendig, da unter Linux die Docker Container direkten Zugang ins Internet haben. Unter Windows wird hierfür ein Proxy eingerichtet, wodurch die IP-Adresse der Anfrage verloren geht. Somit kann diese hier nicht getrackt werden.

Docker kann mithilfe folgendem Tutorial auf einer Ubuntu-Machine installiert werden: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/). Anschließend sollten noch folgende Befehle ausgeführt werden, um es allen Nutzergruppen auf dem Server das Ausführen von Docker zu ermöglichen:[https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/). 

Für Docker-Compose empfiehlt sich dieses Tutorial: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

Nach dem das GitHub Repository [https://github.com/SiggiSigmann/projektarbeit-iobased-login](https://github.com/SiggiSigmann/projektarbeit-iobased-login) heruntergelden wurde, kann das Script “server/setup.sh” ausgeführt werden. Zuvor sollen aber noch die Pfade in der datei “./server/backup/backup.sh” und “/server/backup/cron.txt” angepasst werden (siehe Kapitel Backup). Das Script installiert zuerst die Backup-Funktion. Anschließend wird das Script server/start.sh ausgeführt. In diesem wird mittels Docker-Compose das Projekt neu gebaut und gestartet. 


#### Backup

Um regelmäßig Backups zu erstellen wird das Programm Crontab (https://linux.die.net/man/5/crontab) verwendet. Dieses ermöglicht es Bash-Kommandos zu definierten Zeitpunkten auszuführen. Hierfür muss die Aufgabe registriert werden. Die Registrierung ist in der Datei “cron.txt” hinterlegt. Da Crontab als _Daemon_ ausgeführt wird ist es notwendig hier Absolute Pfade anzugeben. In dieser Datei wird definiert das jeden Tag um 00:00 das script “./server/backup/backup.sh” ausgeführt werden soll. Somit wird eine automatisches Backup der Datenbank veranlasst.

Um das Backup wieder einzuspielen ist ein Beispiel Befehl in dem Backup Script als Kommentar vorhanden. Hier muss nur noch der Dateiname des Backups eingefügt werden.


#### Datenbank

Als Datenbank zum speichern der IP-Daten der Endgeräte sowie die gesammelten Trace-Route Befehle, wird eine MySQL Datenbank verwendet.

Die Datenbank befindet sich in dem Ordner “./server/database”. Dieser Ordner enthält die Docker-Datei für die DB, eine Notiz-Datei mit hilfreichen SQL-Befehlen und einen Unterordner mit dem namen ”sql”. In diesem befinden sich alle verwendete SQL Scripts.

Die Datenbank wird auf dem Docker-Image “mysql/mysql-server:latest” aufgebaut. Anschließen wird das “init.sql” Script aus dem Ordner “sql” in das Verzeichnis “/docker-entrypoint-initdb.d/” des Docker-Containers kopiert. Dadurch wird dieses automatisch ausgeführt wenn der Container vollständig gestartet ist. 

Mit “init.sql” Script wird eine Datenbank mit dem namen “networkdata” erzeugt. Es werden zwei Tabellen Erzeugt: Measurement und Tracert. Measurement enthält dabei die Daten einer Anfrage, und Tracert alle Traceroute Zwischenstationen.

In der Tabelle Measurement wird jede Anfrage an den Server gespeichert. Hierzu wird automatisch eine “MeasurementID” vergeben, die auch als PRIMARY KEY dient. Die Spalte “PersonName” enthält den übergebenen Benutzernamen. “IpAddress“ enthält die bei der Abfrage verwendeten IP-Adresse. Um den Trace zu dieser IP zu speichern wird die referenz “TraceID” zur Tabelle “Tracert” verwendet. Zusätzlich wird noch der Ort(Land, Bundesland und Ort) und der Zeitpunkt der Anfrage gespeichert.

In “Tracert” werden informationen von dem Trace zur Geräte-IP-Adresse gespeichert. Dabei enthält jeder eintrag ein Hop in Richtung der Geräte-IP.  In der Spalte “IpAdresse” wird die IP-Adresse des Hops abgelegt und in der Spalte “Address Name” der Hostname dieser Adresse.


#### FlaskServer

Der Webserver wurde in dem Verzeichnis “./server/flaskserver/ “entwickelt. In diesem sind alle Dateien, Scripte usw. enthalten die für die Berechnungen, Darstellung der Webseite usw. benötigt werden. 

Die Einstiegsdaten des Flask-Servers ist die setup.py Datei. Hier werden die einzelnen Routen definiert. Die Wichtigen Routen werden hier nochmal genauer erläutert:

Die Route /image/* und /white/image/* werden verwendet um Diagramme zu generieren. Dabei wird die Klasse Plotter verwendet Mehr dazu in dem Unterkapitel plotter.

Um Diagramme für einen Nutzer anzuzeigen  wird die Route /diagram/* verwendet. Hier wird das Template diagram.html verwendet. Zusätzlich werden available_images, person_data ( wer wie viele einträge hat), running_Threads ( zum anzeigen welche Traces gerade erstellt werden) und der actual_user ( beinhaltet für wenn die seite gerendert wird ) benötigt. 

Um Diagramme Nutzer übergreifen vergleichen zu können werden die Pfade /compare/ benötigt. Vergleicht zunächst die Nutzer mit den meisten Einträgen die die Datenbank. Durch auswählen anderer Nutzer in den Dropdown menüs kann dies geändert werden. Die Nutzer werden als Post nachricht an den Server übertragen. Zur generierung der Webseite wird das Template compare.html verwendet. Dieses benötigt im gegensatz diagram.html nicht nur ein Nutzer in actual_user  sonder zwei, daher werden actual_user_1 und actual_user_2 verwendet.

mit /data/* können die Datenbankeinträge eingestehen werden. Hierzu wird data.html als template verwendet. Diese benötigen wie zuvor actual_user, running_Threads, person_data. ZUsätzlich werden die Daten aus der datenbank in der Variable data übergeben. Durch verwendet des pfades /data/json/* können die Daten direkt als json zurückerhalten werden.

Der Root Pfad / wird verwendet im dem nutzer die möglichkeit zu geben eine Anfrage zu senden und so seine IP mit Nutzername in die Datenbank einzutragen. Bei einer GET nachricht wird die Hauptseite angezeigt durch das Template index.html erstellt. Die Variable ip enthält die aktuelle IP adresse des nutzers, die beim aufruf der Seite verwendet wurde. Die Variabel got_proposal speichert ob es eine Vermutung gibt um welchen Nutzer es sich handelt. Falls dies erfolgreich war, steht dieser Name in der Variable username. Zum einfügen einer IP in die Datenbank muss da diese Route Post Nachricht gesendet werden. im Body muss ein Json enthalten sein der die form {“username”:username} entspricht. Wenn die anfrage erfolgreich war, wird erneut das index.html Template gerendert. zusätzlich den zuvor beschriebenen Variablen wird hier noch die Variable result auf 1 gesetzt, Dadurch wird dem Nutzer eine success nachricht angezeigt.

Wichtig bei der entwicklung des Servers ist, das alle Print ausgaben an die datei stderr weitergegeben werden, da diese sonst nicht in dem log des Docker compose auftauchen. dies kann durch print(nachricht, file=sys.stderr) erzielt werden.


##### dbconnector

Die Klasse DBconnector, stellt der Server eine Verbindung zu der in dem anderen Docker-Container befindende Datenbank her. Hierzu wird die IP adresse, der Datenbankname, ein nutzername und ein passwort benötigt. Diese Daten müssen bei der Instanziierung dem Konstruktor übergeben werden. Dieser Teste auch die Verbindung. Sollte die verbindung nicht zustande kommen crasht das Programm. Dies ist mit absicht so, denn dies bewirkt, dass der Docker Container des Sevre neu starten und so der Webserver nur online ist wenn die Datenbank bereit ist. Diese Klasse kann von mehreren Threads aus aufgerufen werden und wurde daher Threadsicher durch einen lock, gestaltet. Dies ist nur zur Sicherheit hinzugefügt worden. Eigentlich sind Datenbank von sich aus Threadsicher. Neben den Privaten connect und _dissconect Methoden enthält diese Klasse viele weitere um bestimmte Daten und Aggregationen der Daten Abzugreifen und um Daten in die Datenbank einzufügen. Siehe untenstehendes UML diagram. UAf die genaue Funktion der Methoden wird hier nicht weiter eingegangen.


##### Trace

Die Trace Klasse ist für das Erstellen eines Trace zum nutzer hin und für das abspeichern dieser zuständig. Hierfür muss dieser Klasse bei der erzeugung eine Datenbankverbindung übergeben werden. Zum erzeugen eines Traces wird die IP und die Trace id an die execute Methode übergeben. DIese erstellt einen neuen Thread in der der Thread erstellt wird. In dem Thread wer denn nun Pakte zum nutzer geschickt mit einer incremntierenden TTL und so der weg des Pakteses nachempfunden. Bei jedem Hop wird die IP adresse und der Name festgestellt und in die Datenbank eingetragen.

über die Funktion get_Threads können alle laufende Threads abgefragt werden. DIe laufenden threads haben immer die nummer der TraceID.


##### evaluator

Die Klasse Evaluator ist vorgesehen um intelligente entscheidungen auf basis des Datenbestand zu treffen. Hierzu benötigt diese Klasse eine Datenbankverbindung die dem Konstruktor übergeben wird. 

Da durch Corona kein aussagekräftiger Datensatz entstehen konnte wird hier nur durch die Methode max_likely_user nur der Nutzer zurückgegeben der eine IP am häufigsten verwendet hat.

Hier könnte allerdings mehr erzielt werden, indem z.B. auch die Wahrscheinlichkeit, dass ein nUtzer auch er ist zurückgegeben wird, usw.

Diese klasse wird bei der erstellung der index.html seite verwendet.


##### subnet

In der Klasse Subnet werden nähere Information zu einer gegeben IP Adresse berechnet. Dies geschieht einerseits auf einer csv Datei in dem verzeichnis ./server/flaskserverv/de.csv, welche [https://www.nirsoft.net/countryip/de.html](https://www.nirsoft.net/countryip/de.html) hier heruntergeladen werden kann. Andereseitz wird ein kostenlos berenzt nutzbarar Dienst [http://ip-api.com](http://ip-api.com) verwendet.

Die csv Datei wird verwendet um nicht alle Daten in der Datenbank speichern zu müssen, da sich die Daten hier nicht veränder. Alle zusatzdaten aus dem ip-api.com müssen zwingen in der Datenbank abgespeichert werden, da sich diese über die Zeit hinweg ändern können. Außerdem ist die Anfrage Anzahl zeitlich begrenzt und so können nicht beliebig viele anfragen gestellt werden.

Bei der instanziierung der Klasse muss der link zu der csv datei angegeben werden. Diese Datei wird anschließend durch die Methode loadFile geladen. Durch die Methode find_Ownder kann nun zu einer gegebenen IP das Subnetz und der Besitzer dieses Subnetzes herausgefunden werden. Da nicht alle Subnetzbereiche in der Datei beschrifted sind wurden zwei manuell hinzugefügt, mit der bemerkung m.e. (manually edited)

Die MEthode get_ip_location leifert geoinformation zu einer ip zurück. Dabei wird der Dienst ip-api.com verwendet, wodurch diese Daten in der Datenbanktabelle Measurements abgelegt werden müssen.


##### plotter

In der klasse Plotter werden aus den Daten grafiken und Auswertungen erstellt. Hierzu benötigt diese Klasse eine Datenbankverbindung und deine instanz der subnet klasse, die der klasse beim Erzeugen übergeben werden muss.

Der klasse kann ein Json entnommen werden in dem alle Informationen zu den möglichen Graphen , über die Methode get_json. Zum anpassen auf einzelne user kann dieser klasse noch ein Nutzernamen übergeben werden. Der json enthält die URL zu dem bild, ein alternativen text und eine Beschreibung. zusätzlich sind die bilder in kategorien unterteilt.

Mit der Methode get_compare_json kann derselbe Json nur für zwei Benutzer erstellt werden. Dies wird für die Compare seite benötigt. Da der get_compare_json  auf dem anderen erstellt wird, muss nur dieser bei änderungen bearbeitet werden.

Wenn der Server ein aufruf eines Bild empfängt wird der name des Bildes an die Funktion create_image weitergeleitet. Diese extrahiert aus dem name des bildes den Nutzername, die Kategorienummer und die numerierung des bildes. Mit diesen Informationen wird nun die passende generierende funktion ausgewählt und aufgerufen

Zur generierung wird Matplotlib verwendet. Hierzu werden erst die benötigten, daten aus der DB abgefragt und vorverarbeitet. Anschließen wird eine geeignete Funktion des Matplotlib verwendet um das diagramm zu generieren.


##### robots.txt

Da auf dieser Webseite Personenbezogene Daten öffentlich einsehbar sind sollte verhindert werden das diese unnötige aufmerksamkeit bekommt. Daher werden alle Webcrawler von suchmaschinen durch die Robots.txt Datei angewiesen diese webseite komplett nicht in den Suchergebnissen anzuzeigen. Die Datei kann durch den Pfade /robots.txt abgefragt werden und befindet sich in dem ./server/flaskserver/static/ verzeichnis


##### Docker

In dem Verzeichnis ./server/flaskserver/  befindet sich die Dockerfile zum Erstellen des Containers, welcher den Webserver (Flask) ausführt. Dieser basiert grundlegend auf dem Python Image python:3.8. Hier werden alle benötigen Bash-Scripte, Python-Scripte, HTML und andere statische Dateien wie CSS in den Container Kopiert. Nachdem der Prot 80 geöffnet wurde wird das script startFlask.sh als entrypoint ausgeführt. In diesem Script werden alle benötigte Pakete installiert und anschließen der Server durch das Pythonscript server.py gestarted.

Da die Installation der Zusatzpakete sehr langsam ist, verwenden wir ein Docker Image, welches schon alle requirements vorinstalliert hat. Um dieses zu nutzen wird der Container nun auf der basis des tobiassigmann/ip_collector:latest Containers aufgebaut. Da hier alle benötigten Pakete bereits installiert sind ist der Zeitaufwand deutlich geringer. 

Das Docker Image tobiassigmann/ip_collector:latest wird in dem Verzeichnis ./server/flaskserver/createDockerContainer/ entwickelt. Die Befehle um das Image zu aktualisieren befinden sich in der requirements.txt


#### Workflow

Um die Continous Deployment Piplene zu verwenden muss auf dem Server ein selbstgehosteter GithubRunner installiert werden, wie hier gezeigt wird: [https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners). Anschließen sollte dieser als Dienst gestartet werden: [https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service](https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service). Nach der installation führt dieser nun die Action in dem ordner “.gitub/workflows/cd.yml” aus, welche unten zu sehen ist. 

In dem “on” bereich wird definiert das dieser Workflow bei jedem push oder pull auf dem “Main” Branch ausgeführt wird. Die schritte sind in dem “jobs” segment definiert. Hier wird als erstes bestimmt das dieser nur auf den selbstgehosteten Runnern ausgeführt werden darf. Anschließen wird das aktuelle Repository heruntergeladen. Nun werden die scripts “setup.sh” und “clean.sh” ausführbar gemacht und un den nächstenbeiden schritten ausgeführt. Dadurch wird der Server sauber gehalten und immer neu aufgesetzt um alle Änderungen zu übernehmen. Nur die in der Datenbank gespeicherten Daten bleiben erhalten, da diese sich außerhalb des Projektverzeichnisses befiden.

Dadurch dass die Datenbank in einem anderen Verzeichnis abgelegt ist, wird auch ein Weiteres Problem umgangen. Da Docker als Root user ausgeführt wird sind alle Ordner die von diesem erzeugt werden auch nur als Root Benutzer bearbeitbar. Der Github Runner läuft jedoch unter Normalen Rechten. Wenn der Datenbankordner in dem Projektverzeichnis abgelegt ist, kann der Runner das Aktuelle Projekt nicht von github klonen da er hierzu den Ordner löschen müsste. Außerdem würden so die Daten verloren gehen.


### Client

Das Ziel ist es Nutzerverhalten anhand der IP Adressen, Metadaten und Verhalten festzustellen und darauf basierend Entscheidungen zu treffen.

Hierzu muss der Nutzer regelmäßig anfragen an den Server senden, damit die IP Adresse festgehalten werden kann. Zum regelmäßigem senden gibt es zwei ansätze: Zeitbasiert und Verhaltensbasiert. Im Zeitbasierten ansatz werden anfragen in einem Gewissen zeitintervall gesendet: z.B. jede Stunde. Beim Verhaltensbasiert Ansatz werden Anfragen immer dann gesendet wenn der Nutzer eine gewisse App oder ein Gewisses Programm benutzt, wodurch das verhalten des Nutzers mit erfasst werden kann. Im folgenden wird der Implementation dieser Ansätze auf Whatsapp und IOS beschrieben.


#### Android

Um automatisch von Android Smartphones Pings an den Server zu senden wird die App Automate ([https://llamalab.com/automate/](https://llamalab.com/automate/)) verwendet. Diese erlaubt es dem Nutzer abläufe und automatisierungen zu erstellen. Zum senden wurden zwei sogenannte Flows (kleine Programme innerhalb der App erstellt. Diese können durch die Community auch von anderen Nutzern heruntergeladen und angepasst werden. Die Flows können hier gefunden werden: [https://llamalab.com/automate/community/flows/38312](https://llamalab.com/automate/community/flows/38312) (WhatsApp basiert) , [https://llamalab.com/automate/community/flows/38310](https://llamalab.com/automate/community/flows/38310) (Stundenbasiert).

Nachdem die FLows in der App heruntergeladen wurden, müssen diese noch bearbeitet werden um einen Nutzername und eine URL oder IP zum server einzugeben. Hierzu muss zuerst der gewünschte workflow geöffnet werden, wie in Bild 1 zu sehen.

Anschließend muss der Knoten “HTTP request” bearbeitet werden, siehe Bild 2.


##### Stündlicher

Im nebenstehenden bild ist der Flow für das absenden einer stündlichen Anfrage zu sehen. Der Flow beginn in Zeile 1. Nach dem start wird direkt in Zeile 2 eine HTTP Post anfrage durch den “HTTP request” Knoten gesendet. Hierbei werden die zuvor definierten Parameter und Optionen verwendet. Anschließend wird in Zeile 3 überprüft ob das senden erfolgreich war. Je nachdem wird in Zeile 4 eine entsprechende nachricht als Toast angezeigt und in Zeile 5 eine Zeit entsprechend dem erfolg des HTTP requests gewartet.


##### WhatsApp

Das nebenstehende Bild zeigt den Flow für das automatische senden jedes mal wenn WhatsApp geöffnet wurde. Wie zuvor auch beginnt der Flow in Zeile 1. In Zeile 2 wird jedes mal wenn eine App geöffnet wird, überprüft ob Whatsapp geöffnet wurde.

Nur wenn WhatsApp erkannt wurde wird ein HTTP request gesendet und der erfolg dieses Requests überprüft. Anschließend wird in Zeile 5 ein Toast angezeigt der den Status des requests wiedergibt, Falls dieser fehlschlägt wird das senden des Requests nach 5 minuten (siehe Zeile 4 und 5) erneut gesendet. 


#### IOS



*   App -> Kurzer überblick
*   Dann Shortcut 


## 


## Auswertung

Auswertung der einzelnen Diagramme


### Measurement


#### Distance Hour


#### Distance Minutes


#### Day


#### Time


### Measurement


#### IP-Addresses distribution


#### IP-Addresses distribution in trace


#### ISP distribution


#### ISP distribution in trace


### Address / Time:


#### IP / Hour:


#### IP in trace / Hour


#### ISP / Hour


#### ISP in trace / Hour


### Changes in Adress:


#### IP Address changes


#### IP Address changes / Hour


#### IP Address changes / Hour / Frequency


#### ISP changes


#### ISP changes graph


#### ISP changes / Hour


### Changes in Adress


#### City distribution


#### City / IP


#### City changes


#### City changes / Time / Frequency


#### City graph


#### City / ISP


## Anwendungen


### Benutzererkennung


#### Authentifizierung und Sicherheit



*   Anomalieerkennung


#### Tracking



*   Vergleich mit Google Analytics? wirklich anders?


#### Advertising


## Ausblick



*   ml zum erkennen ob passt oder net
*   mehr infos auf anfrage (OS, …) wie fingerprinting
*   nginx
*   cache für bilder
*   irgendwas mit dns
*   


## 


## Old Notes



*   Identitätsprüfung anhand Bewegungsdaten
    *   Was ist Bewegung?
*   Zugangspunkt Identität und Mustererkennung


### Problem:

Keine Testdaten vorhanden. Daher erstellen eines Bewegungsdaten Generator, der Fake Daten generiert auf denen der Missbrauch festgestellt werden kann.



*   IP Subnetze
    *   welche sind nebeneinander
    *   VPN
    *   woher wissen wir ob ein anmeldeversuch vorliegt und von wo
    *   
*   IP2Location


### Use Cases:



*   Account Missbrauch
*   Kreditkarten Missbrauch


### Abgabe: 



*   Dokumentation, gleiche Einleitung, jeweils ein Use Case
*   Software
*   Präsentation (10 min pro Person)



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")




<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")




<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image3.png "image_tooltip")
[https://plotly.com/python/parallel-categories-diagram/](https://plotly.com/python/parallel-categories-diagram/)



<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image4.png "image_tooltip")




<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image5.png "image_tooltip")



## Papers



1. [https://ieeexplore.ieee.org/abstract/document/1286872?casa_token=VPp2Z2VKS_wAAAAA:c678_O8m3GNXwZqDgpocXTMDMpcvomiNQI1IstVnRgCa_2S8NrgTJ6v8POAPYE0WTIN1CjxDVYs](https://ieeexplore.ieee.org/abstract/document/1286872?casa_token=VPp2Z2VKS_wAAAAA:c678_O8m3GNXwZqDgpocXTMDMpcvomiNQI1IstVnRgCa_2S8NrgTJ6v8POAPYE0WTIN1CjxDVYs)
2. [https://ieeexplore.ieee.org/abstract/document/8391393](https://ieeexplore.ieee.org/abstract/document/8391393)
3. [https://ieeexplore.ieee.org/abstract/document/6296127](https://ieeexplore.ieee.org/abstract/document/6296127)

Meeting2:



*   Bau von aps bzw servern zur datensammlung
*   Viel grobgranularere tracking (heimnetz mobielnet kawlan) 
    *   könnte schon reichen?

Ideen:



*   diagrame pro nutzer
    *   routen (wo splittet sich der trace)
    *   welche IP / trace zur welcher uhrzeit + tag
    *   verglichen der trace um standort zu definieren


## 17.12.2020:


### Routing Loop:

When a routing loop occurs it stops data from reaching the final destination. Unlike the failed hop, the routing loop simply loops data back and forth between two hops. In the example below, a loop has occurred between 192.168.1.4 and 192.168.1.5. Data will pass back and forth from one to the other until the session times out or, in this particular case, the maximum hop limit is reached.

You will often see this if the end-user has been 'wall gardened'. A 'walled garden' refers to a browsing environment that controls the information and Web sites the user is able to access. This is a popular method used by ISPs in order to keep the user navigating only specific areas of the Web. This is often for the purpose of shielding users from information, such as restricting children's access to unsuitable material.


### Traceroute 


#### Von Cloud gegen User:

Start:

(170, '192.168.112.1', '-', 1)

(170, '193.196.36.1', 'defgw-v1721.scc.kit.edu', 2)

(170, '129.13.55.209', 'defgw-v377.scc.kit.edu', 3)

(170, '141.52.3.6', 'r-border-cs-1-eth3-2.scc.kit.edu', 4)

(170, '193.197.63.6', 'kar-rz-a99-hu0-2-0-7.belwue.net', 5)

(170, '129.143.60.115', 'fra-decix-1-hu0-0-0-0.belwue.net', 6)

(170, '80.157.200.197', '-', 7)

(170, '91.23.232.213', 'p5b17e8d5.dip0.t-ipconnect.de', 8)

(170, '87.163.159.232', 'p57a39fe8.dip0.t-ipconnect.de', 9)


#### Von User gegen Cloud:

fritz.box (192.168.178.1)

p3e9bf51b.dip0.t-ipconnect.de (62.155.245.27)

217.5.113.74 (217.5.113.74)

217.5.113.74 (217.5.113.74)

80.150.169.190 (80.150.169.190) 

cr-erl2-be8.x-win.dfn.de (188.1.144.221)

 * * *

 tr-v1288-rbocs1.scc.kit.edu (141.52.249.170)

 cs-2021-l-1-2-eth1-54.scc.kit.edu (141.52.3.7)

defgw-v774.scc.kit.edu (129.13.70.97)

193.196.38.56 (193.196.38.56)


## Übersichtsgenereirung

Zur Erstellung einer Übersicht pro Person wurden die verschiedenen IP-Adressen abgefragt.

Hierzu wurde aus der Datenbank alle Traces zusammengefasst und die unterschiedlichen 

IP-Adressen herausgefiltert. Zum Schluss wird der Dienst verwendet um nähere informationen der IP-Adressen abfragen. Dadurch ergibt sich ein Stadt Genaues Bewegungsprofil der Benutzer.

Zur abfrage der Adressen wird folgende MySQL abfrage verwendet:

SELECT Tracert.IpAddress, count(Tracert.IpAddress)  FROM   Tracert   

JOIN Measurement ON 


    Measurement.TraceID = Tracert.TraceID 


    where Measurement.PersonName  = "JulianHandy" 


    group by Tracert.IpAddress 


    order by count(Tracert.IpAddress) DESC;

Mittels des Scripts ip.py kann die ausgabe der SQL-Abfrage aus einer Datei eingelesen werden. Dieses Script fragt anschließend automatisch alle relevanten Daten zur IP-Adresse ab.


### Beispiel:


### Nutzer: JulianPC

<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image6.png "image_tooltip")


<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image7.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image7.png "image_tooltip")




<p id="gdcalert8" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image8.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert9">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image8.png "image_tooltip")




<p id="gdcalert9" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image9.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert10">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image9.png "image_tooltip")


Auffällig ist, das die häufigsten 5 Adressen zu Universitäten gehören. Daher kann davon 

ausgegangen werden, dass diese zu dem BW-Cloud Netz gehören. Anhand der Anbieter kann weiter davon ausgegangen werden, dass die restlichen Adressen zu einem oder mehreren Heimnetzwerken gehören.  Diese Heimnetzwerke werden in 

Frankfurt, Karlsruhe und in Bietigheim-Bissingen vermutet.

Die Städte Karlsruhe und Bietigheim-Bissingen lassen sich durch die Mobilität des Benutzers erklären. Das Auftreten der Stadt Frankfurt lässt sich erklären, wenn man berücksichtigt dass hier ein Verteilungszentrum der Telekom AG steht.


### Continue:

Da momentan nur IPAdressen gespeichert werden, ist nicht sicher wie aktuell die Daten zu den Adressen sind. Wurden diese in der Zwischenzeit geändert kann dies einen Nebeneffekt auf spätere Weiterverarbeitung haben. Hier wäre eine direkte Abfrage und Speicherung dieser Werte hilfreich.


## done:



*   MAC vom Accesspoint
    *   Funkzelle, Adresse, Android
*   Aufbereitung:
    *   Subnezte zusammenfassen -> Netzmaske herausfinden ([https://www.nirsoft.net/countryip/de.html](https://www.nirsoft.net/countryip/de.html))=> liste , sanky diagram(done)
    *   Histogramm über Subnetz=> liste , sanky diagram (done)
    *   Zeitliche verlauf der Aufrufe
        *   difference, linechart
        *   tagesübersicht, barchart
        *   
    *   Matrix x zu y, wie oft => matrix(text) oder pointcloud, barchart(jeder stellt ein wwechsel dar
    *   wie häufig an jeden ort
        *   wechseln
    *   alls mit Zeit zusammen (done)
*   Vergleich Zwischen Nutzer
*   Auswertung Diagrame
    *   Häufigkeit für jeden Nuzer pro IP
        *   alle traces vergleichen, wie oft kommt eine ip darin vor
    *   Warscheinlichkeit für Übergänge

Android:



*   Automate APP
*   

<p id="gdcalert10" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image10.jpg). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert11">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image10.jpg "image_tooltip")


<p id="gdcalert11" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image11.jpg). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert12">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image11.jpg "image_tooltip")


<p id="gdcalert12" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image12.jpg). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert13">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image12.jpg "image_tooltip")


<p id="gdcalert13" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image13.jpg). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert14">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image13.jpg "image_tooltip")





