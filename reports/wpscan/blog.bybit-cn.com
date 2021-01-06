_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.1
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[32m[+][0m URL: https://blog.bybit-cn.com/ [63.151.118.233]
[32m[+][0m Started: Thu Jun  4 17:03:15 2020

Interesting Finding(s):

[32m[+][0m Headers
 | Interesting Entries:
 |  - Server: nginx
 |  - X-Akamai-Transformed: 9 16437 0 pmb=mTOE,1
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[32m[+][0m https://blog.bybit-cn.com/robots.txt
 | Interesting Entries:
 |  - /wp-admin/
 |  - /wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m XML-RPC seems to be enabled: https://blog.bybit-cn.com/xmlrpc.php
 | Found By: Link Tag (Passive Detection)
 | Confidence: 30%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[32m[+][0m https://blog.bybit-cn.com/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[32m[+][0m The external WP-Cron seems to be enabled: https://blog.bybit-cn.com/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[32m[+][0m WordPress version 5.4 identified (Insecure, released on 2020-03-31).
 | Found By: Rss Generator (Passive Detection)
 |  - https://blog.bybit-cn.com/feed/, <generator>https://wordpress.org/?v=5.4</generator>
 |  - https://blog.bybit-cn.com/comments/feed/, <generator>https://wordpress.org/?v=5.4</generator>
 |
 | [31m[!][0m 6 vulnerabilities identified:
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Password Reset Tokens Failed to Be Properly Invalidated
 |     Fixed in: 5.4.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10201
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11027
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47634/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-ww7v-jg8c-q6jw
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Unauthenticated Users View Private Posts
 |     Fixed in: 5.4.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10202
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11028
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47635/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-xhx9-759f-6p2w
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Authenticated Cross-Site Scripting (XSS) in Customizer
 |     Fixed in: 5.4.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10203
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11025
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47633/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-4mhg-j6fx-5g3c
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Authenticated Cross-Site Scripting (XSS) in Search Block
 |     Fixed in: 5.4.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10204
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11030
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47636/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-vccm-6gmc-qhjh
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Cross-Site Scripting (XSS) in wp-object-cache
 |     Fixed in: 5.4.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10205
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11029
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47637/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-568w-8m88-8g2c
 |
 | [31m[!][0m Title: WordPress < 5.4.1 - Authenticated Cross-Site Scripting (XSS) in File Uploads
 |     Fixed in: 5.4.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/10206
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11026
 |      - https://wordpress.org/news/2020/04/wordpress-5-4-1/
 |      - https://core.trac.wordpress.org/changeset/47638/
 |      - https://www.wordfence.com/blog/2020/04/unpacking-the-7-vulnerabilities-fixed-in-todays-wordpress-5-4-1-security-update/
 |      - https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-3gw2-4656-pfr2

[32m[+][0m WordPress theme in use: primer
 | Location: https://blog.bybit-cn.com/wp-content/themes/primer/
 | Last Updated: 2020-05-22T00:00:00.000Z
 | Readme: https://blog.bybit-cn.com/wp-content/themes/primer/readme.txt
 | [33m[!][0m The version is out of date, the latest version is 1.8.9
 | Style URL: https://blog.bybit-cn.com/wp-content/themes/primer/style.css?ver=5.4
 | Style Name: Primer
 | Style URI: https://github.com/godaddy/wp-primer-theme
 | Description: Primer is a powerful theme that brings clarity to your content in a fresh design....
 | Author: GoDaddy
 | Author URI: https://www.godaddy.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 1.8.7 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://blog.bybit-cn.com/wp-content/themes/primer/style.css?ver=5.4, Match: 'Version: 1.8.7'


[34m[i][0m Plugin(s) Identified:

[32m[+][0m all-in-one-seo-pack
 | Location: https://blog.bybit-cn.com/wp-content/plugins/all-in-one-seo-pack/
 | Last Updated: 2020-05-27T15:22:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 3.5.2
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By:
 |  Urls In 404 Page (Passive Detection)
 |  Comment (Passive Detection)
 |
 | Version: 3.4.2 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://blog.bybit-cn.com/wp-content/plugins/all-in-one-seo-pack/readme.txt

[32m[+][0m duracelltomi-google-tag-manager
 | Location: https://blog.bybit-cn.com/wp-content/plugins/duracelltomi-google-tag-manager/
 | Latest Version: 1.11.4 (up to date)
 | Last Updated: 2020-03-20T06:38:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.11.4 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - https://blog.bybit-cn.com/wp-content/plugins/duracelltomi-google-tag-manager/js/gtm4wp-form-move-tracker.js?ver=1.11.4
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://blog.bybit-cn.com/wp-content/plugins/duracelltomi-google-tag-manager/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://blog.bybit-cn.com/wp-content/plugins/duracelltomi-google-tag-manager/readme.txt

[32m[+][0m newsletter
 | Location: https://blog.bybit-cn.com/wp-content/plugins/newsletter/
 | Last Updated: 2020-06-03T08:10:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 6.7.0
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 6.5.9 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - https://blog.bybit-cn.com/wp-content/plugins/newsletter/style.css?ver=6.5.9
 |  - https://blog.bybit-cn.com/wp-content/plugins/newsletter/subscription/validate.js?ver=6.5.9
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - https://blog.bybit-cn.com/wp-content/plugins/newsletter/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - https://blog.bybit-cn.com/wp-content/plugins/newsletter/readme.txt

[32m[+][0m wp-smushit
 | Location: https://blog.bybit-cn.com/wp-content/plugins/wp-smushit/
 | Last Updated: 2020-05-18T01:38:00.000Z
 | [33m[!][0m The version is out of date, the latest version is 3.6.3
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 3.6.1 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://blog.bybit-cn.com/wp-content/plugins/wp-smushit/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://blog.bybit-cn.com/wp-content/plugins/wp-smushit/readme.txt


[34m[i][0m No Config Backups Found.

[32m[+][0m WPVulnDB API OK
 | Plan: free
 | Requests Done (during the scan): 6
 | Requests Remaining: 3

[32m[+][0m Finished: Thu Jun  4 17:03:46 2020
[32m[+][0m Requests Done: 66
[32m[+][0m Cached Requests: 7
[32m[+][0m Data Sent: 46.953 KB
[32m[+][0m Data Received: 607.564 KB
[32m[+][0m Memory used: 215 MB
[32m[+][0m Elapsed time: 00:00:31
